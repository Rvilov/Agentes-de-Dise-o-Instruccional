#!/usr/bin/env python3
"""Mandatory preflight for every resource in Course Agent Suite v1.4.1.

This verifies structural evidence for source fidelity but does not automatically
judge semantic entailment; independent source-reviewer QA is still required.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description='Compuerta unificada Word + notas + busqueda stock')
    ap.add_argument('--project-dir',type=Path,default=Path('.'))
    ap.add_argument('--resource-id',required=True)
    ap.add_argument('--docx',required=True,type=Path)
    ap.add_argument('--platform',choices=['auto','codex','claude'],default='auto')
    ap.add_argument('--report',type=Path)
    ap.add_argument('--orientation',choices=['portrait','landscape'],default='portrait')
    args=ap.parse_args()
    root=args.project_dir.expanduser().resolve()
    docx=args.docx if args.docx.is_absolute() else root/args.docx
    q=root/'qa'; rid=args.resource_id
    contract=q/(rid+'.editorial-contract.json')
    stock_log=q/(rid+'.stock-search-log.json')
    trace=q/(rid+'_trazabilidad.md')
    manifest=q/(rid+'.manifest.json')
    shared=Path(__file__).resolve().parent
    if args.platform=='auto':
        platform='codex' if (root/'.agents/skills/template-format-reviewer').is_dir() else 'claude'
    else:platform=args.platform
    skills=root/('.agents' if platform=='codex' else '.claude')/'skills'
    tf=skills/'template-format-reviewer/scripts'
    visual=skills/'visual-stock-reviewer/scripts'
    steps=[
        ('notes_canonical',[str(shared/'editorial_contract.py'),'audit','--contract',str(contract),'--docx',str(docx),'--strict']),
        ('stock_execution',[str(shared/'audit_stock_execution.py'),'--contract',str(contract),'--search-log',str(stock_log),'--docx',str(docx),'--strict']),
        ('factual_fidelity',[str(shared/'fidelity_gate.py'),'audit','--project-dir',str(root),'--resource-id',rid,'--docx',str(docx),'--strict','--report',str(q/(rid+'.fidelity-preflight.json'))]),
        ('editorial_length',[str(tf/'audit_editorial_notes.py'),str(docx),'--strict']),
        ('document_structure',[str(tf/'audit_docx_structure.py'),str(docx),'--orientation',args.orientation,'--traceability',str(trace),'--strict']),
    ]
    try:
        resource_type=json.loads(contract.read_text(encoding='utf-8')).get('resource_type','').lower()
    except (OSError,ValueError):resource_type=''
    if resource_type in ('rise','interactivo','lectura_interactiva'):
        steps.append(('rise_notes',[str(tf/'audit_rise_editorial.py'),str(docx),'--rise','--strict']))
    if manifest.exists():
        steps.append(('visual_plan',[str(visual/'audit_visual_plan.py'),str(manifest),'--docx',str(docx),'--require-ready']))
    else:
        steps.append(('visual_plan_missing',None))
    findings=[]
    for name,params in steps:
        if params is None:
            findings.append({'gate':name,'pass':False,'detail':'Falta manifest interno de fuente y plan visual'})
            continue
        cmd=[sys.executable]+params
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            detail=p.stdout.strip() or p.stderr.strip()
            findings.append({'gate':name,'pass':p.returncode==0,'exit_code':p.returncode,'detail':detail[-9000:]})
        except (OSError,subprocess.TimeoutExpired) as e:
            findings.append({'gate':name,'pass':False,'detail':str(e)})
    pass_all=all(x['pass'] for x in findings)
    report={'resource_id':rid,'docx':str(docx),'pass_machine_gates':pass_all,
            'gates':findings,'human_review_required':['fidelidad semantica: evidencia realmente respalda la afirmacion', 'cobertura de todas las afirmaciones y excepciones', 'coherencia visual','licencias y URLs de stock','render por pagina','accesibilidad']}
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:
        out=args.report if args.report.is_absolute() else root/args.report
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text+'\n',encoding='utf-8')
    print(text)
    if not pass_all:sys.exit(1)

if __name__=='__main__':main()
