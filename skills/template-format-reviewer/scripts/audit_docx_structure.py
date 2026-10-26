#!/usr/bin/env python3
"""Deterministic Word delivery contract gate: one non-repeating DI header,
portrait A4 by default, no internal source citations in the client-facing Word.
This is a structural gate; render and inspect every page before delivery.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='{%s}' % W
REQ=['Tipo de Recurso','Duración','Estilo/Edición','Descripción/Objetivo','Notas de Edición','Contenido del Recurso']
# Restrict to production/source provenance, not curricular mentions of legislation,
# citations explicitly taught in the lesson, or URLs used as learner materials.
PROVENANCE=[
    ('MATERIAL_BASE',r'\bmaterial\s+base\s*:'),
    ('SLIDES_DE_REFERENCIA',r'\b(?:slides?|diapositivas?)\s+de\s+referencia\s*:'),
    ('FUENTE_DOCUMENTAL',r'\bfuente\s*:\s*(?:presentaci[oó]n|transcripci[oó]n|documento|archivo|F\d+\b|[^\n]{0,90}\.(?:pptx|docx|pdf)\b)'),
    ('SOURCE_ID',r'\b(?:id\s+de\s+fuente|fuente\s+F\d+|turn\d+file\d+)\b'),
    ('SOURCE_LOCATION',r'\b(?:origen\s+de\s+informaci[oó]n|ubicaci[oó]n\s+en\s+(?:la\s+)?fuente)\s*:'),
]

def ns(tag):return P+tag

def txt(node):
    parts=[]
    for child in node.iter():
        if child.tag == ns('t'):
            parts.append(child.text or '')
        elif child.tag in (ns('br'),ns('cr')):
            parts.append('\n')
        elif child.tag == ns('tab'):
            parts.append('\t')
    return ''.join(parts).strip()

def visible_header(z, num):
    names=[n for n in z.namelist() if re.fullmatch(r'word/header\d+\.xml',n)]
    result=[]
    for name in names:
        h=ET.fromstring(z.read(name))
        if any(txt(h).split()) or list(h.iter(ns('drawing'))) or list(h.iter(ns('pict'))):
            result.append(name)
    return result

def audit(path, expected_orientation='portrait', traceability=None):
    issues=[]
    with zipfile.ZipFile(path) as z:
        doc=ET.fromstring(z.read('word/document.xml'))
        body=doc.find(ns('body'))
        paragraphs=list(doc.iter(ns('p')))
        blocks=[]
        for item in body:
            kind=item.tag.split('}')[-1]
            if kind in ('p','tbl'):
                blocks.append((kind,txt(item)))
        tables=list(doc.iter(ns('tbl')))
        cells=list(doc.iter(ns('tc')))
        labels={}
        for label in REQ:
            key=label.casefold()
            count=0
            for cell in cells:
                t=txt(cell).casefold().strip()
                if t.startswith(key) and (len(t)==len(key) or t[len(key)] in ': \n\t'):
                    count+=1
            labels[label]=count
            if count!=1:
                issues.append('HEADER_LABEL_COUNT:'+label+':'+str(count))
        # Text before the official block means a second decorative title/header.
        first=next(((kind,text) for kind,text in blocks if text.strip()),None)
        if not first or first[0]!='tbl':
            issues.append('META_HEADER_NOT_FIRST_BODY_BLOCK')
        extra_body_paragraphs=[t[:120] for kind,t in blocks if kind=='p' and t.strip()]
        if extra_body_paragraphs:
            issues.append('BODY_CONTENT_OUTSIDE_EDITORIAL_TABLE:'+str(len(extra_body_paragraphs)))
        tr_repeat=[]
        for i,tr in enumerate(doc.iter(ns('tr'))):
            pr=tr.find(ns('trPr'))
            if pr is None: continue
            h=pr.find(ns('tblHeader'))
            if h is not None and h.get(ns('val'),'1') not in ('0','false','off'):
                tr_repeat.append(i)
        if tr_repeat:
            issues.append('REPEATING_TABLE_HEADER:'+','.join(map(str,tr_repeat)))
        sections=list(doc.iter(ns('sectPr')))
        orientations=[]
        for s in sections:
            pg=s.find(ns('pgSz'))
            if pg is None:
                orientations.append('unknown')
                continue
            width=int(pg.get(ns('w'),'0'))
            height=int(pg.get(ns('h'),'0'))
            orientation='landscape' if width>height else 'portrait'
            orientations.append(orientation)
            if expected_orientation!='any' and orientation!=expected_orientation:
                issues.append('PAGE_ORIENTATION:'+orientation)
        if len(orientations)!=1:
            issues.append('UNEXPECTED_SECTION_COUNT:'+str(len(orientations)))
        # A portrait document can still render cropped if w:tblW retains the
        # preferred width of its original landscape template.
        if sections:
            s=sections[0]
            page=s.find(ns('pgSz'))
            margins=s.find(ns('pgMar'))
            if page is not None and margins is not None:
                usable=int(page.get(ns('w'),'0'))-int(margins.get(ns('left'),'0'))-int(margins.get(ns('right'),'0'))
                for idx,table in enumerate(tables):
                    pr=table.find(ns('tblPr'))
                    table_width=pr.find(ns('tblW')) if pr is not None else None
                    if table_width is not None and table_width.get(ns('type'))=='dxa':
                        declared=int(table_width.get(ns('w'),'0'))
                        if declared>usable+25:
                            issues.append(f'TABLE_WIDTH_OVERFLOW:{idx}:{declared}>{usable}')
                    grid=table.find(ns('tblGrid'))
                    if grid is not None:
                        grid_total=sum(int(col.get(ns('w'),'0')) for col in grid)
                        if grid_total>usable+25:
                            issues.append(f'TABLE_GRID_OVERFLOW:{idx}:{grid_total}>{usable}')
        headers=visible_header(z, len(sections))
        if headers:
            issues.append('REPEATING_WORD_HEADER_PART:'+','.join(headers))
        # Extract paragraph text (not whole tables, avoids duplicated nested labels).
        leakage=[]
        for p in paragraphs:
            s=txt(p)
            for code,pat in PROVENANCE:
                if re.search(pat,s,flags=re.IGNORECASE):
                    leakage.append({'code':code,'snippet':s[:140]})
                    break
        if leakage:
            issues.append('VISIBLE_SOURCE_TRACEABILITY:'+str(len(leakage)))
        images=len([n for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')])
        links=[]
        rname='word/_rels/document.xml.rels'
        if rname in z.namelist():
            rr=ET.fromstring(z.read(rname))
            rels={x.attrib.get('Id'):x.attrib for x in rr}
            for h in doc.iter(ns('hyperlink')):
                rid=h.get('{%s}id'%R)
                if rid and rid in rels:
                    links.append(rels[rid].get('Target',''))
        alltext='\n'.join(txt(p) for p in paragraphs)
        has_todo=bool(re.search(r'\b(TODO|PENDIENTE_STOCK|PENDIENTE_VERIFICACION_STOCK)\b',alltext))
        if has_todo:
            issues.append('UNRESOLVED_PLACEHOLDER')
        if traceability is not None:
            if not traceability.is_file() or traceability.stat().st_size==0:
                issues.append('TRACEABILITY_SIDECAR_MISSING')
            else:
                lines=traceability.read_text(encoding='utf-8').splitlines()
                # At least one factual row, with a recognized F# source, is mandatory.
                rows=[x for x in lines if re.match(r'^\|\s*(?:R\d+(?:-B\d+)?|[^|]+)\s*\|\s*F\d+\s*\|',x,re.IGNORECASE)]
                if not rows:
                    issues.append('TRACEABILITY_SIDECAR_UNPOPULATED')
        result={
            'file':str(path), 'required_labels':{key:(count==1) for key,count in labels.items()},
            'label_counts':labels, 'table_count':len(tables), 'embedded_images':images,
            'external_hyperlinks':[u for u in links if u.startswith('http')],
            'orientation_per_section':orientations,'repeat_header_rows':tr_repeat,
            'word_header_parts_with_content':headers,'source_leaks':leakage,'has_todo':has_todo,
            'pass_basic':all(count>=1 for count in labels.values()) and bool(tables),
            'pass_delivery':not issues, 'issues':issues,
            'gate_policy':'Template metadata once; no repeating header; portrait unless authorized; sources only in external QA files. Structural test only; visual render required.'
        }
    return result


def main():
    p=argparse.ArgumentParser(description='Gate estructural del Word DI listo para edición')
    p.add_argument('docx')
    p.add_argument('--orientation',default='portrait',choices=['portrait','landscape','any'])
    p.add_argument('--traceability',default=None,help='Archivo externo de trazabilidad; debe existir')
    p.add_argument('--json-out',default=None)
    p.add_argument('--strict',action='store_true',help='Devolver código 1 si no cumple')
    a=p.parse_args()
    result=audit(Path(a.docx),a.orientation,Path(a.traceability) if a.traceability else None)
    data=json.dumps(result,ensure_ascii=False,indent=2)
    print(data)
    if a.json_out:Path(a.json_out).write_text(data+'\n',encoding='utf-8')
    if a.strict and not result['pass_delivery']:
        sys.exit(1)

if __name__=='__main__': main()
