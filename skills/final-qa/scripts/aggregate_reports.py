#!/usr/bin/env python3
"""Aggregate reviewer reports, including mandatory Content QA x DI coverage gate."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

VALID_RESULTS={'CUMPLE','INCUMPLE','NO_APLICA','PENDIENTE_CRITERIO'}


def find_shared(script_path:Path):
    for anc in [script_path.parent, *script_path.parents]:
        for p in (anc/'shared',anc/'.course-agent-suite'/'shared'):
            if (p/'references'/'content-qa-control-register.json').is_file():return p
    return None


def analyze_content_qa(reports, shared, require_agent_ownership=False):
    if shared is None:
        return {
            'status':'ROJO','code':'CONTENT_QA_SOURCE_INCOMPLETE',
            'missing_controls':[],'problems':['PPTX/index/registro compartidos no localizados'],
            'covered':0,'total':None,
        }
    import sys
    sys.path.insert(0,str(shared/'scripts'))
    from validate_content_qa_source import audit_fast
    v=audit_fast(shared)
    if v['status']!='OK':
        return {'status':'ROJO','code':'CONTENT_QA_SOURCE_INCOMPLETE','validation':v,
                'missing_controls':[],'problems':v['errors'],'covered':0,'total':None}
    register=json.loads((shared/'references'/'content-qa-control-register.json').read_text(encoding='utf-8'))
    controls={c['id']:c for c in register['controls']}
    checks={}
    problems=[]
    for r in reports:
        for c in r.get('content_qa_checks',[]):
            code=c.get('id') or c.get('control_id')
            result=c.get('result') or c.get('status')
            if code not in controls:
                problems.append(f'Control desconocido: {code}')
                continue
            if result not in VALID_RESULTS:
                problems.append(f'{code}: resultado inválido {result}')
                continue
            if require_agent_ownership and r.get('agent') not in controls[code]['agents']:
                problems.append(f'{code}: revisor no asignado {r.get("agent")}')
            if not isinstance(c.get('evidence'),str) or not c['evidence'].strip():
                problems.append(f'{code}: falta evidencia o motivo de NO_APLICA')
            if c.get('slides') and set(c['slides'])!=set(controls[code]['source_slides']):
                problems.append(f'{code}: referencias de diapositivas inconsistentes')
            checks.setdefault(code,[]).append({'agent':r.get('agent'),**c})
    missing=sorted(set(controls)-set(checks))
    if missing:problems.append(f'Controles no evaluados: {", ".join(missing)}')
    for code, items in checks.items():
        if any((c.get('result') or c.get('status'))=='INCUMPLE' for c in items):
            problems.append(f'{code}: incumplimiento reportado')
        if any((c.get('result') or c.get('status'))=='PENDIENTE_CRITERIO' for c in items):
            problems.append(f'{code}: pendiente de criterio humano')
    if missing or problems:
        return {'status':'ROJO','code':'CONTENT_QA_COVERAGE_INCOMPLETE',
                'covered':len(checks),'total':len(controls),
                'missing_controls':missing,'problems':problems}
    return {'status':'VERDE','code':'CONTENT_QA_VERIFIED',
            'covered':len(checks),'total':len(controls),
            'missing_controls':[],'problems':[]}



def analyze_fidelity(reports, project_dir, resource_id, docx, shared):
    """Re-audit sources + Word freshness independently; never trust a green label alone."""
    errors=[]
    reviewer=[r for r in reports if r.get('agent')=='source-fidelity-reviewer' and
              (r.get('resource_id')==resource_id or r.get('resource')==resource_id)]
    if len(reviewer)!=1:
        errors.append(f'SOURCE_FIDELITY_REVIEWER_REPORT_COUNT: expected 1 got {len(reviewer)}')
    elif reviewer[0].get('status')!='VERDE' or reviewer[0].get('decision')!='APROBADO':
        errors.append('SOURCE_FIDELITY_REVIEWER_NOT_APPROVED')
    if shared is None or not (shared/'scripts'/'fidelity_gate.py').is_file():
        errors.append('FIDELITY_GATE_MISSING_FROM_SUITE')
    if not resource_id or docx is None or project_dir is None:
        errors.append('FIDELITY_CONTEXT_MISSING: --project-dir --resource-id --docx required')
    if errors:
        return {'status':'ROJO','code':'SOURCE_FIDELITY_INCOMPLETE','errors':errors}
    import sys
    sys.path.insert(0,str(shared/'scripts'))
    from fidelity_gate import verify
    root=project_dir.expanduser().resolve()
    word=(docx if docx.is_absolute() else root/docx).resolve()
    qa=root/'qa'
    result=verify(root,resource_id,word,qa/'source-catalog.json',
                  qa/'course-coverage-contract.json',qa/(resource_id+'.fidelity-ledger.json'),
                  qa/(resource_id+'.fidelity-review.json'))
    if not result['pass_machine_gates']:
        return {'status':'ROJO','code':'SOURCE_FIDELITY_EVIDENCE_FAILED',**result}
    return {'status':'VERDE','code':'SOURCE_FIDELITY_EVIDENCE_VERIFIED',**result}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('reports',nargs='+')
    ap.add_argument('--out',type=Path)
    ap.add_argument('--qa-source-root',type=Path,help='Root of shared content standards (normally auto-detected)')
    ap.add_argument('--partial-review',action='store_true',help='Return a partial review; not an integral green QA')
    ap.add_argument('--project-dir',type=Path,help='Course project folder with qa/ and source files')
    ap.add_argument('--resource-id',help='Resource identifier R1, R2...')
    ap.add_argument('--docx',type=Path,help='Current output DOCX; verified by SHA-256')
    ap.add_argument('--enforce-three-passes',action='store_true',help='Require learning/editorial/fidelity grouped reviews and fresh course consistency')
    ap.add_argument('--compact',action='store_true',help='Print only status and failing findings; full report remains in --out')
    args=ap.parse_args()
    raw_reports=[json.loads(Path(f).read_text(encoding='utf-8')) for f in args.reports]
    grouped={'status':'NOT_REQUESTED','errors':[]}
    if args.enforce_three_passes:
        if not args.project_dir or not args.docx:
            grouped={'status':'ROJO','errors':['GROUPED_CONTEXT_MISSING']}
            reports=[]
        else:
            shared_tmp=args.qa_source_root or find_shared(Path(__file__).resolve())
            sys.path.insert(0,str(shared_tmp/'scripts') if shared_tmp else str(Path(__file__).parent))
            from verify_review_passes import verify as verify_passes
            rid_tmp=args.resource_id or raw_reports[0].get('resource_id')
            grouped=verify_passes(args.project_dir.expanduser().resolve(),rid_tmp,raw_reports,args.docx)
            reports=grouped['reviewers']
    else:
        reports=[x for g in raw_reports for x in (g.get('reviews',[]) if isinstance(g.get('reviews'),list) else [g])]
    issues=[]
    for r in reports:
        for i in r.get('issues',[]):
            x=dict(i);x['agent']=r.get('agent');x['resource']=r.get('resource');issues.append(x)
    critical=[x for x in issues if x.get('severity')=='critical']
    red=[r for r in reports if r.get('status')=='ROJO' or r.get('decision')=='REGRESA_A_PRODUCCION']
    shared=args.qa_source_root or find_shared(Path(__file__).resolve())
    qa=analyze_content_qa(reports,shared,require_agent_ownership=args.enforce_three_passes)
    rid=args.resource_id or (reports[0].get('resource_id') or reports[0].get('resource'))
    fidelity=analyze_fidelity(reports,args.project_dir,rid,args.docx,shared)
    if critical or red:decision='REGRESA_A_PRODUCCION';status='ROJO'
    elif issues:decision='APROBADO_CON_AJUSTES';status='AMARILLO'
    else:decision='APROBADO';status='VERDE'
    if qa['status']!='VERDE' or fidelity['status']!='VERDE' or grouped['status']=='ROJO':
        if args.partial_review:
            # Explicit partial reviews cannot receive an unqualified integral-green decision.
            if status=='VERDE':status='AMARILLO';decision='APROBADO_CON_AJUSTES'
        else:
            status='ROJO';decision='REGRESA_A_PRODUCCION'
    result={'status':status,'decision':decision,'reports':len(reports),'issues_total':len(issues),
            'critical_total':len(critical),'auto_fixable_total':sum(1 for x in issues if x.get('auto_fixable') is True),
            'content_qa':qa,'source_fidelity':fidelity,'grouped_review':{k:v for k,v in grouped.items() if k!='reviewers'},'partial_review':args.partial_review,'issues':issues}
    data=json.dumps(result,ensure_ascii=False,indent=2)
    if args.out:args.out.write_text(data+'\n',encoding='utf-8')
    if args.compact:
        print(json.dumps({'resource_id':rid,'status':status,'decision':decision,'content_qa':qa['status'],'fidelity':fidelity['status'],'review_passes':grouped['status'],'issues':len(issues),'errors':grouped.get('errors',[])+qa.get('problems',[])+fidelity.get('errors',[])},ensure_ascii=False))
    else:print(data)
    if status=='ROJO':
        sys.exit(1)

if __name__=='__main__':main()
