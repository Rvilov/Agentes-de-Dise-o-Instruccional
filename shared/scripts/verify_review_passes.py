#!/usr/bin/env python3
"""Strict structural checks for three group reviews and one course-wide consistency pass.

This script cannot replace human semantic review; it blocks missing/stale evidence.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

GROUPS={'learning':{'pedagogical-reviewer','dynamism-reviewer','accessibility-reviewer'},
        'editorial':{'visual-stock-reviewer','template-format-reviewer','language-humanizer'},
        'fidelity':{'source-fidelity-reviewer'}}


def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()


def timestamp(value,tag,errors):
    try:
        d=datetime.fromisoformat(value.replace('Z','+00:00'))
        if d.tzinfo is None:raise ValueError('timezone missing')
        return d
    except (ValueError,TypeError,AttributeError) as e:
        errors.append(f'{tag}: completed_at invalid: {e}')
        return None


def verify(root,rid,raw,docx):
    """Return checked status and flattened reviewer payloads.

    The group output is compact but every specialist remains accountable.
    """
    errors=[]; flattened=[]; times={}
    if len(raw)!=3:errors.append('REVIEW_PASS_COUNT: require exactly three grouped files')
    seen=set()
    for r in raw:
        phase=r.get('pass')
        if phase not in GROUPS:
            errors.append(f'REVIEW_PASS_UNKNOWN: {phase}');continue
        if phase in seen:errors.append(f'REVIEW_PASS_DUPLICATE: {phase}')
        seen.add(phase)
        if r.get('resource_id')!=rid:errors.append(f'REVIEW_PASS_RESOURCE_MISMATCH: {phase}')
        times[phase]=timestamp(r.get('completed_at'),phase,errors)
        reviews=r.get('reviews')
        if not isinstance(reviews,list):
            errors.append(f'REVIEW_PASS_SUBREVIEWS_MISSING: {phase}');continue
        agents=[x.get('agent') for x in reviews if isinstance(x,dict)]
        if len(agents)!=len(GROUPS[phase]) or set(agents)!=GROUPS[phase]:
            errors.append(f'REVIEW_PASS_AGENTS_INCOMPLETE: {phase}: {agents}')
        for review in reviews:
            if not isinstance(review,dict):continue
            if review.get('status')!='VERDE':
                errors.append(f'REVIEW_NOT_APPROVED: {phase} {review.get("agent")} status={review.get("status")}')
            if not isinstance(review.get('issues'),list):
                errors.append(f'REVIEW_ISSUES_MISSING: {phase} {review.get("agent")}')
            if review.get('resource_id',review.get('resource'))!=rid:
                errors.append(f'REVIEW_RESOURCE_MISMATCH: {phase} {review.get("agent")}')
            flattened.append(review)
    if set(GROUPS)-seen:errors.append('REVIEW_PASSES_MISSING: '+','.join(sorted(set(GROUPS)-seen)))
    if all(times.get(p) for p in GROUPS):
        if not (times['learning'] <= times['editorial'] <= times['fidelity']):
            errors.append('REVIEW_PASS_ORDER_INVALID: learning -> editorial -> fidelity')
    if times.get('editorial') and times.get('fidelity'):
        fidelity_path=root/'qa'/(rid+'.fidelity-review.json')
        if fidelity_path.is_file():
            try:
                reviewed=json.loads(fidelity_path.read_text(encoding='utf-8'))
                reviewed_at=timestamp(reviewed.get('reviewed_at'),'fidelity-semantic-review',errors)
                if reviewed_at and reviewed_at<times['editorial']:
                    errors.append('FIDELITY_SEMANTIC_REVIEW_BEFORE_EDITORIAL')
            except (ValueError,OSError) as e:
                errors.append(f'FIDELITY_REVIEW_UNREADABLE: {e}')
        else:
            errors.append('FIDELITY_SEMANTIC_REVIEW_MISSING')
    consistency=root/'qa/course-consistency-review.json'
    if not consistency.exists():errors.append('COURSE_CONSISTENCY_REVIEW_MISSING')
    else:
        try:
            c=json.loads(consistency.read_text(encoding='utf-8'))
            if c.get('status')!='VERDE' or c.get('issues'):
                errors.append('COURSE_CONSISTENCY_NOT_APPROVED')
            ct=timestamp(c.get('completed_at'),'consistency',errors)
            if ct and times.get('editorial') and times.get('fidelity'):
                if not times['editorial']<=ct<=times['fidelity']:
                    errors.append('COURSE_CONSISTENCY_ORDER_INVALID')
            items=c.get('resources',[])
            if not isinstance(items,list) or not items:
                errors.append('COURSE_CONSISTENCY_NO_RESOURCES');items=[]
            checked=set()
            for item in items:
                ident=item.get('id')
                if ident in checked:errors.append(f'COURSE_CONSISTENCY_DUPLICATE: {ident}')
                checked.add(ident)
                loc=root/item.get('docx','')
                try:
                    actual=digest(loc)
                    if actual!=item.get('sha256'):errors.append(f'COURSE_CONSISTENCY_STALE_WORD: {ident}')
                except (OSError,IsADirectoryError):errors.append(f'COURSE_CONSISTENCY_WORD_MISSING: {ident}')
            if rid not in checked:errors.append(f'COURSE_CONSISTENCY_RESOURCE_NOT_REVIEWED: {rid}')
            index=root/'qa/course-resource-index.json'
            if index.exists():
                declared=json.loads(index.read_text(encoding='utf-8')).get('resources',[])
                for v in declared:
                    if v.get('id') not in checked:
                        errors.append(f'COURSE_CONSISTENCY_RESOURCE_NOT_REVIEWED: {v.get("id")}')
            else:errors.append('COURSE_RESOURCE_INDEX_MISSING')
        except (OSError,ValueError,TypeError) as e:
            errors.append(f'COURSE_CONSISTENCY_INVALID: {e}')
    return {'status':'VERDE' if not errors else 'ROJO','errors':errors,
            'passed_roles':sorted(x.get('agent') for x in flattened if x.get('agent')),
            'reviewers':flattened}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-dir',type=Path,required=True)
    ap.add_argument('--resource-id',required=True)
    ap.add_argument('--docx',type=Path,required=True)
    ap.add_argument('reports',nargs=3)
    ap.add_argument('--out',type=Path)
    a=ap.parse_args()
    raw=[json.loads(Path(x).read_text(encoding='utf-8')) for x in a.reports]
    result=verify(a.project_dir.resolve(),a.resource_id,raw,a.docx)
    compact={k:v for k,v in result.items() if k!='reviewers'}
    s=json.dumps(compact,ensure_ascii=False,indent=2)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(s+'\n',encoding='utf-8')
    else:print(s)
    raise SystemExit(0 if not result['errors'] else 1)

if __name__=='__main__':main()
