#!/usr/bin/env python3
"""Whole-course mandatory topic coverage: all declared resources must pass fidelity gate.

Machine-verifiable coverage of registered topics, not automatic semantic discovery
of all topics in the source corpus. The human reviewer must check topic completeness.
"""
import argparse
import json
import sys
from pathlib import Path
from fidelity_gate import verify


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--project-dir',type=Path,default=Path('.'))
    p.add_argument('--report',type=Path)
    p.add_argument('--strict',action='store_true')
    a=p.parse_args()
    root=a.project_dir.expanduser().resolve()
    qa=root/'qa'
    problems=[]
    try:
        topics=json.loads((qa/'course-coverage-contract.json').read_text(encoding='utf-8')).get('topics',[])
        index=json.loads((qa/'course-resource-index.json').read_text(encoding='utf-8')).get('resources',[])
    except (OSError,ValueError) as e:
        topics,index=[],[]
        problems.append(f'COURSE_COVERAGE_METADATA_MISSING: {e}')
    entries={r.get('id'):r for r in index if isinstance(r,dict) and r.get('id')}
    if not entries:problems.append('COURSE_RESOURCE_INDEX_EMPTY')
    required={t['id']:t for t in topics if t.get('required') is True and t.get('usage')=='content' and t.get('id')}
    if not required:problems.append('REQUIRED_TOPICS_EMPTY')
    assigned={rid for t in required.values() for rid in t.get('resource_ids',[])}
    missing_resources=sorted(assigned-set(entries))
    if missing_resources:problems.append('TOPICS_REFER_TO_MISSING_RESOURCES: '+','.join(missing_resources))
    outputs={}
    for rid,resource in entries.items():
        if not resource.get('docx') or not isinstance(resource['docx'],str):
            problems.append(f'WORD_PATH_MISSING_FOR_RESOURCE: {rid}')
            continue
        d=(root/resource['docx']).resolve()
        if not d.is_relative_to(root):
            problems.append(f'WORD_PATH_ESCAPE_FOR_RESOURCE: {rid}')
            continue
        result=verify(root,rid,d,qa/'source-catalog.json',qa/'course-coverage-contract.json',
                      qa/(rid+'.fidelity-ledger.json'),qa/(rid+'.fidelity-review.json'))
        outputs[rid]=result
        if not result['pass_machine_gates']:
            problems.append(f'FIDELITY_NOT_APPROVED_FOR_{rid}: '+ '; '.join(result['errors'][:4]))
    if not set(entries).issuperset(assigned):
        problems.append('MANDATORY_RESOURCE_MISSING')
    summary={'status':'VERDE' if not problems else 'ROJO',
             'pass_machine_gates':not problems,'resources':len(entries),
             'required_topics':len(required),'verified_resources':sum(r['pass_machine_gates'] for r in outputs.values()),
             'problems':problems,'resource_results':outputs,
             'limitation':'Machine verifies REGISTERED topics, not whether the original source has other omitted topics.'}
    text=json.dumps(summary,ensure_ascii=False,indent=2)
    if a.report:
        out=a.report if a.report.is_absolute() else root/a.report
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(text+'\n',encoding='utf-8')
    print(text)
    if a.strict and problems:return 1
    return 0

if __name__=='__main__':sys.exit(main())
