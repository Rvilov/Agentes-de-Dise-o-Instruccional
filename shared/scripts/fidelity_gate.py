#!/usr/bin/env python3
"""Fail-closed source-fidelity evidence gate for Word course resources.

This script verifies traceability, exact source excerpts and version freshness.
It DOES NOT decide whether an excerpt semantically entails a factual claim;
that decision requires the independent source-fidelity-reviewer.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
BAD_VERDICTS = {'ALTERADA', 'CONTRADICTORIA', 'NO_ENCONTRADA', 'OMISION_RELEVANTE', 'CONFLICTO', 'PENDIENTE'}
SEMANTIC_CHECKS = ('claim_completeness', 'evidence_support', 'conditions_retained',
                   'source_precedence_reviewed', 'conflicts_resolved', 'no_outside_facts')


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def norm(text):
    t = unicodedata.normalize('NFKD', str(text or ''))
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', t.casefold()).strip()


def has_quote(segment, quote):
    return bool(norm(quote)) and norm(quote) in norm(segment)


def text_from_w(element):
    out = []
    for x in element.iter():
        if x.tag == W + 't':
            out.append(x.text or '')
        elif x.tag == W + 'tab':
            out.append(' ')
        elif x.tag in (W + 'br', W + 'cr'):
            out.append(' ')
    return ''.join(out).strip()


def word_content_units(path, rid):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    tables = root.findall('.//' + W + 'tbl')
    units, headings = [], 0
    block_num = 0
    for table in tables:
        col = None
        for row in table.findall('./' + W + 'tr'):
            cells = row.findall('./' + W + 'tc')
            raw = [norm(text_from_w(c)) for c in cells]
            if any('contenido del recurso' in t for t in raw) and any('notas de edicion' in t for t in raw):
                col = next((i for i, v in enumerate(raw) if 'contenido del recurso' in v), None)
                headings += 1
                continue
            if col is None or col >= len(cells):
                continue
            if not any(raw):
                continue
            block_num += 1
            paragraphs = cells[col].findall('.//' + W + 'p')
            para_count = 0
            for p in paragraphs:
                content = text_from_w(p)
                if not norm(content):
                    continue
                para_count += 1
                units.append({
                    'id': f'{rid}-U{len(units)+1:03}',
                    'block': f'{rid}-B{block_num}',
                    'paragraph': para_count,
                    'text': content,
                })
    if headings == 0 or not units:
        raise ValueError('No se pudo localizar la columna Contenido del Recurso con texto en el Word')
    return units


def source_segments(path):
    ext = path.suffix.lower()
    if ext == '.pptx':
        with zipfile.ZipFile(path) as z:
            items = []
            for name in z.namelist():
                m = re.fullmatch(r'ppt/slides/slide(\d+)\.xml', name)
                if m:
                    items.append((int(m.group(1)), name))
            segments = {}
            for n, name in sorted(items):
                root = ET.fromstring(z.read(name))
                segments[f'slide:{n}'] = ' '.join((e.text or '') for e in root.iter(A + 't'))
            return segments
    if ext == '.docx':
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read('word/document.xml'))
        pars = [text_from_w(p) for p in root.iter(W + 'p')]
        return {f'paragraph:{i}': p for i, p in enumerate(pars, 1)}
    if ext == '.pdf':
        try:
            p = subprocess.run(['pdftotext', '-layout', str(path), '-'], capture_output=True,
                               text=True, timeout=40, check=True)
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            raise ValueError(f'No se pudo extraer texto del PDF: {e}')
        return {f'page:{i}': page for i, page in enumerate(p.stdout.split('\f'), 1) if page.strip()}
    if ext in ('.txt', '.md', '.csv', '.srt', '.vtt'):
        lines = path.read_text(encoding='utf-8-sig').splitlines()
        return {f'line:{i}': line for i, line in enumerate(lines, 1)}
    raise ValueError(f'Fuente no verificable automaticamente ({ext}); exportar a texto conservando ubicaciones')


def source_at(segments, locator):
    if locator in segments:
        return segments[locator]
    m = re.fullmatch(r'lines:(\d+)-(\d+)', str(locator))
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        if start > end or end - start > 35:
            raise ValueError('Rango de lineas invalido o demasiado amplio (maximo 36)')
        missing = [n for n in range(start, end+1) if f'line:{n}' not in segments]
        if missing:
            raise ValueError('Rango de lineas fuera de la fuente')
        return ' '.join(segments[f'line:{n}'] for n in range(start, end+1))
    raise ValueError(f'Ubicacion no localizada: {locator}')


def read_json(path, errors, label):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('debe ser objeto JSON')
        return data
    except (OSError, ValueError) as e:
        errors.append(f'{label}: {e}')
        return {}


def source_catalog(root, document, errors):
    sources = document.get('sources', [])
    if not isinstance(sources, list) or not sources:
        errors.append('SOURCE_CATALOG_EMPTY: sin fuentes de contenido registradas')
        return {}, {}, {}
    catalog, segments, hashes = {}, {}, {}
    recognized={'.pptx','.docx','.pdf','.txt','.md','.csv','.srt','.vtt','.xlsx','.xls','.mp4','.mov','.mp3','.m4a','.wav'}
    available={p.relative_to(root).as_posix() for p in (root/'sources').rglob('*')
               if p.is_file() and p.suffix.lower() in recognized} if (root/'sources').is_dir() else set()
    registered={Path(s.get('path','')).as_posix() for s in sources if isinstance(s,dict) and s.get('path')}
    if available-registered:
        errors.append('UNREGISTERED_SOURCE_FILES: '+', '.join(sorted(available-registered)))
    for s in sources:
        if not isinstance(s, dict):
            errors.append('SOURCE_INVALID: objeto esperado')
            continue
        sid, relative = s.get('id'), s.get('path')
        if not sid or sid in catalog or not relative or not isinstance(relative, str):
            errors.append(f'SOURCE_INVALID: ID o ruta ausente/duplicada ({sid})')
            continue
        p = (root / relative).resolve()
        if not p.is_relative_to(root):
            errors.append(f'SOURCE_PATH_ESCAPE: {sid}')
            continue
        if not p.is_file():
            errors.append(f'SOURCE_MISSING: {sid} {relative}')
            continue
        if not s.get('factual', True) and s.get('role') not in ('guideline', 'lineamiento', 'reference'):
            errors.append(f'SOURCE_ROLE_INCONSISTENT: {sid}')
        try:
            hashes[sid] = digest(p)
            if s.get('factual', True):
                segments[sid] = source_segments(p)
                if not segments[sid] or not any(norm(v) for v in segments[sid].values()):
                    raise ValueError('sin texto legible: requiere transcripcion o inspeccion manual')
            else:
                try:
                    segments[sid] = source_segments(p)
                except (ValueError, OSError, zipfile.BadZipFile, ET.ParseError):
                    segments[sid] = {}

        except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as e:
            errors.append(f'SOURCE_UNREADABLE: {sid}: {e}')
            continue
        if s.get('sha256') and s['sha256'] != hashes[sid]:
            errors.append(f'SOURCE_CHANGED_FROM_CATALOG: {sid}')
        catalog[sid] = s
    if not any(s.get('factual', True) for s in catalog.values()):
        errors.append('NO_FACTUAL_SOURCES: no existen fuentes de contenido')
    return catalog, segments, hashes


def check_ref(source_id, locator, quote, catalog, segments, errors, tag):
    if source_id not in catalog:
        errors.append(f'{tag}: fuente desconocida {source_id}')
        return
    if not catalog[source_id].get('factual', True):
        errors.append(f'{tag}: {source_id} es un lineamiento/no fuente factual')
        return
    if not isinstance(quote, str) or len(norm(quote)) < 8:
        errors.append(f'{tag}: falta fragmento original verificable (minimo 8 caracteres)')
        return
    try:
        src = source_at(segments[source_id], locator)
        if not has_quote(src, quote):
            errors.append(f'{tag}: el fragmento NO aparece en {source_id} {locator}')
    except (ValueError, TypeError) as e:
        errors.append(f'{tag}: {e}')


def verify(root, rid, docx, registry, coverage_path, ledger_path, review_path):
    errors, warnings = [], []
    if not docx.is_file():
        return {'resource_id':rid,'docx':str(docx),'pass_machine_gates':False,
                'errors':['WORD_MISSING'],'warnings':[],'machine_checks':{},
                'semantic_review':'NO_REALIZADA'}
    word_hash = digest(docx)
    try:
        real_units = word_content_units(docx, rid)
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as e:
        errors.append(f'WORD_CONTENT_UNREADABLE: {e}')
        real_units = []
    catalog = read_json(registry, errors, 'SOURCE_CATALOG')
    topics_doc = read_json(coverage_path, errors, 'COURSE_COVERAGE')
    ledger = read_json(ledger_path, errors, 'FIDELITY_LEDGER')
    review = read_json(review_path, errors, 'FIDELITY_REVIEW')
    if catalog.get('schema_version') != '1.4.1':
        errors.append('SOURCE_CATALOG_SCHEMA_VERSION_INVALID')
    if topics_doc.get('schema_version') != '1.4.1':
        errors.append('COURSE_COVERAGE_SCHEMA_VERSION_INVALID')
    sources, segments, hashes = source_catalog(root, catalog, errors)
    if ledger.get('schema_version') != '1.4.1':
        errors.append('FIDELITY_SCHEMA: ledger debe ser version 1.4.1')
    if ledger.get('resource_id') != rid:
        errors.append('FIDELITY_RESOURCE_MISMATCH')
    if ledger.get('word_sha256') != word_hash:
        errors.append('FIDELITY_STALE_WORD: cambio el Word despues de la revision')
    if ledger.get('source_hashes') != hashes:
        errors.append('FIDELITY_STALE_SOURCES: han cambiado una o mas fuentes')
    expected_units = {u['id']: u for u in real_units}
    l_units = ledger.get('units', [])
    if not isinstance(l_units, list):l_units=[]
    seen_units = set()
    for u in l_units:
        if not isinstance(u, dict):
            errors.append('UNIT_INVALID');continue
        uid = u.get('id')
        if uid in seen_units: errors.append(f'UNIT_DUPLICATE: {uid}')
        seen_units.add(uid)
        target = expected_units.get(uid)
        if not target or norm(target['text']) != norm(u.get('text')) or target['block'] != u.get('block'):
            errors.append(f'UNIT_MISMATCH: {uid} no coincide con el Word')
        kind = u.get('classification')
        if kind not in ('factual', 'mixed', 'nonfactual'):
            errors.append(f'UNIT_UNCLASSIFIED: {uid}')
        if kind == 'nonfactual' and len(norm(u.get('nonfactual_reason'))) < 20:
            errors.append(f'UNIT_NO_REASON: {uid}, justificar por que no expresa hechos')
        if kind in ('factual','mixed') and not u.get('claim_ids'):
            errors.append(f'UNIT_NO_CLAIMS: {uid}')
    if seen_units != set(expected_units):
        errors.append(f'UNIT_COVERAGE_INCOMPLETE: faltan o sobran {sorted(set(expected_units)^seen_units)}')
    claimed = ledger.get('claims', [])
    if not isinstance(claimed, list):claimed=[]
    claim_by_id = {}
    for c in claimed:
        if not isinstance(c, dict):errors.append('CLAIM_INVALID');continue
        cid, uid = c.get('id'), c.get('unit_id')
        if not cid or cid in claim_by_id:
            errors.append(f'CLAIM_ID_MISSING_OR_DUPLICATE: {cid}');continue
        claim_by_id[cid]=c
        unit = next((u for u in l_units if u.get('id')==uid), None)
        if not unit or unit.get('classification') not in ('factual','mixed'):
            errors.append(f'CLAIM_UNIT_INVALID: {cid}');continue
        if len(norm(c.get('text'))) < 8 or not has_quote(unit.get('text',''), c.get('text','')):
            errors.append(f'CLAIM_NOT_IN_WORD: {cid}')
        if c.get('verdict') != 'RESPALDADA':
            errors.append(f'CLAIM_NOT_SUPPORTED: {cid} estado={c.get("verdict")}')
        ev = c.get('evidence', [])
        if not isinstance(ev, list) or not ev:
            errors.append(f'CLAIM_NO_EVIDENCE: {cid}');continue
        for idx, item in enumerate(ev, 1):
            if not isinstance(item,dict):errors.append(f'CLAIM_EVIDENCE_INVALID: {cid}');continue
            check_ref(item.get('source_id'),item.get('locator'),item.get('quote'),sources,segments,errors,f'{cid}/E{idx}')
            if len(norm(item.get('rationale'))) < 20:
                errors.append(f'CLAIM_NO_SEMANTIC_RATIONALE: {cid}/E{idx}')
    for u in l_units:
        if not isinstance(u, dict):continue
        ids = u.get('claim_ids') or []
        if any((cid not in claim_by_id or claim_by_id[cid].get('unit_id') != u.get('id')) for cid in ids):
            errors.append(f'UNIT_CLAIM_LINK_BROKEN: {u.get("id")}')
        if u.get('classification') == 'nonfactual' and ids:
            errors.append(f'UNIT_NONFACTUAL_HAS_CLAIMS: {u.get("id")}')
    referenced_claim_ids={cid for u in l_units if isinstance(u,dict) for cid in u.get('claim_ids',[])}
    if referenced_claim_ids != set(claim_by_id):
        errors.append('CLAIMS_NOT_FULLY_MAPPED_TO_UNITS')

    topics = topics_doc.get('topics', [])
    if not isinstance(topics,list) or not topics:
        errors.append('SOURCE_TOPICS_MISSING: matriz de cobertura verificable vacia')
        topics=[]
    topic_by_id = {}
    for t in topics:
        if not isinstance(t,dict):errors.append('TOPIC_INVALID');continue
        tid=t.get('id')
        if not tid or tid in topic_by_id:
            errors.append(f'TOPIC_ID_DUPLICATE: {tid}');continue
        topic_by_id[tid]=t
        if t.get('usage') not in ('content', 'reference', 'guideline', 'excluded'):
            errors.append(f'TOPIC_USAGE_INVALID: {tid}')
        if t.get('usage')=='content':
            if not t.get('resource_ids'):
                errors.append(f'TOPIC_NO_RESOURCES: {tid}')
            check_ref(t.get('source_id'),t.get('locator'),t.get('quote'),sources,segments,errors,f'TOPIC/{tid}')
    topic_rows = ledger.get('topic_coverage', [])
    if not isinstance(topic_rows,list):topic_rows=[]
    claimed_topics = set()
    for row in topic_rows:
        if not isinstance(row, dict):errors.append('TOPIC_COVERAGE_INVALID');continue
        tid = row.get('topic_id')
        if tid in claimed_topics:errors.append(f'TOPIC_COVERAGE_DUPLICATE: {tid}')
        claimed_topics.add(tid)
        topic = topic_by_id.get(tid)
        if not topic or rid not in topic.get('resource_ids',[]):
            errors.append(f'TOPIC_COVERAGE_OUT_OF_SCOPE: {tid}');continue
        if topic.get('usage') != 'content':
            errors.append(f'TOPIC_NON_CONTENT_USED_AS_FACT: {tid}')
        if not row.get('claim_ids') or not set(row['claim_ids']).issubset(set(claim_by_id)):
            errors.append(f'TOPIC_COVERAGE_NO_SUPPORTED_CLAIMS: {tid}')
        if len(norm(row.get('rationale'))) < 20:
            errors.append(f'TOPIC_COVERAGE_NO_RATIONALE: {tid}')
    expected_topics={tid for tid,t in topic_by_id.items() if t.get('required') is True and t.get('usage')=='content' and rid in t.get('resource_ids',[])}
    if not expected_topics:
        errors.append('RESOURCE_NO_REQUIRED_TOPICS: revisar matriz, ninguna unidad obligatoria asignada')
    if not expected_topics.issubset(claimed_topics):
        errors.append(f'OMITTED_SOURCE_TOPICS: {sorted(expected_topics - claimed_topics)}')

    if review.get('agent') != 'source-fidelity-reviewer' or review.get('resource_id') != rid:
        errors.append('INDEPENDENT_FIDELITY_REVIEW_MISSING_OR_MISMATCH')
    if review.get('word_sha256') != word_hash or review.get('source_hashes') != hashes:
        errors.append('INDEPENDENT_REVIEW_STALE')
    if review.get('status') != 'VERDE' or review.get('decision') != 'APROBADO':
        errors.append('INDEPENDENT_REVIEW_NOT_APPROVED')
    for field,ids in [('reviewed_unit_ids',set(expected_units)),('reviewed_claim_ids',set(claim_by_id)),
                      ('reviewed_topic_ids', expected_topics)]:
        val=review.get(field, [])
        if not isinstance(val,list) or set(val)!=ids or len(val)!=len(ids):
            errors.append(f'INDEPENDENT_REVIEW_COVERAGE: {field}')
    # Independent semantic judgment for EACH individual factual claim.
    assessments=review.get('claim_assessments', [])
    if not isinstance(assessments,list):assessments=[]
    assessed=set()
    for assessment in assessments:
        if not isinstance(assessment,dict):
            errors.append('INDEPENDENT_CLAIM_ASSESSMENT_INVALID');continue
        cid=assessment.get('claim_id')
        if cid in assessed:errors.append(f'INDEPENDENT_CLAIM_ASSESSMENT_DUPLICATE: {cid}')
        assessed.add(cid)
        if cid not in claim_by_id:
            errors.append(f'INDEPENDENT_ASSESSMENT_UNKNOWN_CLAIM: {cid}')
        if assessment.get('verdict')!='RESPALDADA':
            errors.append(f'INDEPENDENT_ASSESSMENT_NOT_SUPPORTED: {cid}')
        if len(norm(assessment.get('explanation'))) < 25:
            errors.append(f'INDEPENDENT_ASSESSMENT_NO_EXPLANATION: {cid}')
    if assessed != set(claim_by_id):
        errors.append(f'INDEPENDENT_CLAIM_ASSESSMENTS_INCOMPLETE: {sorted(set(claim_by_id)^assessed)}')
    topic_assessments=review.get('topic_assessments', [])
    if not isinstance(topic_assessments,list):topic_assessments=[]
    reviewed_topics=set()
    for item in topic_assessments:
        if not isinstance(item,dict):continue
        tid=item.get('topic_id')
        if tid in reviewed_topics:errors.append(f'INDEPENDENT_TOPIC_ASSESSMENT_DUPLICATE: {tid}')
        reviewed_topics.add(tid)
        if item.get('covered') is not True or len(norm(item.get('explanation'))) < 25:
            errors.append(f'INDEPENDENT_TOPIC_NOT_COVERED_OR_UNEXPLAINED: {tid}')
    if reviewed_topics != expected_topics:
        errors.append(f'INDEPENDENT_TOPIC_ASSESSMENTS_INCOMPLETE: {sorted(expected_topics^reviewed_topics)}')
    checks=review.get('semantic_checks', {})
    for key in SEMANTIC_CHECKS:
        if checks.get(key) is not True:
            errors.append(f'INDEPENDENT_SEMANTIC_CHECK_MISSING: {key}')
    if len(norm(review.get('review_notes'))) < 40:
        errors.append('INDEPENDENT_REVIEW_NOTES_MISSING')
    try:
        dt.datetime.fromisoformat(str(review.get('reviewed_at','')).replace('Z','+00:00'))
    except ValueError:
        errors.append('INDEPENDENT_REVIEW_TIMESTAMP_INVALID')
    for i in review.get('issues', []):
        if i.get('severity') in ('critical','major') or i.get('status') in BAD_VERDICTS:
            errors.append('INDEPENDENT_REVIEW_UNRESOLVED_ISSUES')
    if not ledger.get('coverage_complete') or not review.get('review_complete'):
        errors.append('FULL_FACTUAL_COVERAGE_NOT_CERTIFIED')
    if not claimed:
        errors.append('CLAIMS_EMPTY: no hay afirmaciones verificadas')
    return {'resource_id':rid, 'docx':str(docx), 'word_sha256':word_hash,
            'source_hashes':hashes, 'pass_machine_gates':not errors,
            'machine_checks':{'content_units':len(real_units),'claims':len(claim_by_id),
                              'required_topics':len(expected_topics),'covered_topics':len(expected_topics & claimed_topics),
                              'source_count':len(sources)},
            'semantic_review':'DECLARADA_POR_REVISOR_INDEPENDIENTE_NO_AUTOMATIZADA',
            'errors':errors,'warnings':warnings}


def prepare(root, rid, docx, catalog_path, output):
    errors=[]
    catalog_doc = read_json(catalog_path, errors, 'SOURCE_CATALOG')
    _, _, hashes = source_catalog(root, catalog_doc, errors)
    if errors:
        raise ValueError(' | '.join(errors))
    units=word_content_units(docx, rid)
    ledger={
        'schema_version':'1.4.1', 'resource_id':rid, 'word_sha256':digest(docx),
        'source_hashes':hashes,'coverage_complete':False,
        'units':[{'id':u['id'],'block':u['block'],'text':u['text'],
                  'classification':'PENDIENTE','claim_ids':[],'nonfactual_reason':''} for u in units],
        'claims':[], 'topic_coverage':[]}
    if output.exists():
        raise FileExistsError('El ledger ya existe. No se sobrescribe: revisar cambios y crear respaldo manual')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'status':'PREPARED_NOT_APPROVED','units':len(units),'path':str(output),
            'word_sha256':ledger['word_sha256'],'source_count':len(hashes)}


def main():
    ap=argparse.ArgumentParser(description='Gate de fidelidad afirmacion-fuente, fail-closed')
    sub=ap.add_subparsers(dest='mode',required=True)
    for action in ('prepare','audit'):
        sp=sub.add_parser(action)
        sp.add_argument('--project-dir',type=Path,default=Path('.'))
        sp.add_argument('--resource-id',required=True)
        sp.add_argument('--docx',type=Path,required=True)
        sp.add_argument('--source-catalog',type=Path)
        sp.add_argument('--ledger',type=Path)
        if action=='prepare':sp.add_argument('--output',type=Path)
        else:
            sp.add_argument('--course-coverage',type=Path)
            sp.add_argument('--review',type=Path)
            sp.add_argument('--report',type=Path)
            sp.add_argument('--strict',action='store_true')
    args=ap.parse_args()
    root=args.project_dir.expanduser().resolve()
    rid=args.resource_id
    def resolve(path, default):
        return (root / (path or default)).resolve()
    docx=resolve(args.docx, None)
    catalog=resolve(args.source_catalog,'qa/source-catalog.json')
    ledger=resolve(args.ledger,f'qa/{rid}.fidelity-ledger.json')
    if args.mode=='prepare':
        output=resolve(args.output,f'qa/{rid}.fidelity-ledger.json')
        try:
            result=prepare(root,rid,docx,catalog,output)
        except (OSError,ValueError,zipfile.BadZipFile) as e:
            print(json.dumps({'status':'ERROR','error':str(e)},ensure_ascii=False));return 2
    else:
        coverage=resolve(args.course_coverage,'qa/course-coverage-contract.json')
        review=resolve(args.review,f'qa/{rid}.fidelity-review.json')
        result=verify(root,rid,docx,catalog,coverage,ledger,review)
        if args.report:
            p=resolve(args.report,None);p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return (1 if args.mode=='audit' and args.strict and not result['pass_machine_gates'] else 0)

if __name__=='__main__':sys.exit(main())
