#!/usr/bin/env python3
"""Validate that the canonical Content QA x DI source and slide-level coverage are intact.

Stdlib-only: works in Claude Code and Codex without extra dependencies.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


def audit(shared_root: Path):
    root=Path(shared_root)
    refs=root/'references'
    src=root/'source-guides'/'Content - Revisión QA x DI.pptx'
    required={
        'source':src,
        'policy':refs/'content-qa-policy.md',
        'index':refs/'content-qa-full-slide-index.md',
        'inventory':refs/'content-qa-slide-inventory.json',
        'register':refs/'content-qa-control-register.json',
        'summary':refs/'content-qa-guidelines.md',
        'supplement':refs/'general-spanish-supplement.md',
    }
    errors=[]
    for key,path in required.items():
        if not path.is_file():errors.append(f'{key}: missing {path}')
    if errors:return {'status':'FAIL','error_code':'CONTENT_QA_SOURCE_INCOMPLETE','errors':errors}

    with zipfile.ZipFile(src) as z:
        slide_ids=sorted(int(m.group(1)) for name in z.namelist() if (m:=re.fullmatch(r'ppt/slides/slide(\d+)\.xml',name)))
    actual_hash=hashlib.sha256(src.read_bytes()).hexdigest()
    register=json.loads(required['register'].read_text(encoding='utf-8'))
    inventory=json.loads(required['inventory'].read_text(encoding='utf-8'))
    idx=required['index'].read_text(encoding='utf-8')
    policy=required['policy'].read_text(encoding='utf-8')

    if len(slide_ids)!=97 or slide_ids!=list(range(1,98)):errors.append('PPTX does not have precisely 97 consecutive slides')
    if inventory.get('slide_count')!=97 or len(inventory.get('slides',[]))!=97:errors.append('Inventory does not list 97 slides')
    for i in range(1,98):
        if not re.search(rf'^## Diapositiva {i:02d} [—-]',idx,re.M):errors.append(f'Index misses slide {i}')
    if inventory.get('sha256') != actual_hash: errors.append('Inventory hash differs from PPTX')
    if register.get('source_sha256') != actual_hash:errors.append('Register hash differs from PPTX')
    if actual_hash not in policy:errors.append('Policy does not identify original source hash')
    controls=register.get('controls',[])
    if len(controls)!=27:errors.append('Control register must include 27 source-backed checks')
    ids=[x['id'] for x in controls]
    if len(set(ids))!=len(ids):errors.append('Repeated control IDs')
    referenced={s for x in controls for s in x.get('source_slides',[])}
    regulatory={x['slide'] for x in inventory['slides'] if x['kind']=='regla / explicación'}
    if regulatory-referenced:errors.append(f'Normative slides without control: {sorted(regulatory-referenced)}')
    for c in controls:
        if not c.get('agents') or not c.get('check'):errors.append(f'Incomplete control {c.get("id")}')
        if not all(1<=s<=97 for s in c.get('source_slides',[])):errors.append(f'Invalid slide number in {c["id"]}')
    if register.get('semicolon_scope',{}).get('independent_uses_defined_in_source') is not False:
        errors.append('Semicolon general rule must not be attributed to PPT')
    return {
        'status':'OK' if not errors else 'FAIL',
        'error_code':None if not errors else 'CONTENT_QA_SOURCE_INCOMPLETE',
        'source_sha256':actual_hash,
        'slides':len(slide_ids),
        'slides_indexed':len(inventory.get('slides',[])),
        'normative_slides_covered':len(regulatory & referenced),
        'normative_slides_total':len(regulatory),
        'controls':len(controls),
        'errors':errors,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,required=True,help='Path to the suite shared/ folder')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    result=audit(args.root)
    raw=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:args.output.write_text(raw+'\n',encoding='utf-8')
    print(raw)
    return 0 if result['status']=='OK' else 1

if __name__=='__main__':raise SystemExit(main())
