#!/usr/bin/env python3
"""Compare static instruction bytes/words, not actual model token counts."""
import argparse
import json
import zipfile
from pathlib import Path


def read_baseline(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        texts=[z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('/SKILL.md')]
        texts += [z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('/global-instructions.fragment.md')]
    return texts


def read_current(root):
    return [p.read_text(encoding='utf-8') for p in root.glob('skills/*/SKILL.md')]+[
        (root/'global-instructions.fragment.md').read_text(encoding='utf-8')]


def stats(items):
    return {'files':len(items),'bytes_utf8':sum(len(x.encode('utf-8')) for x in items),
            'whitespace_words':sum(len(x.split()) for x in items)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--baseline-zip',type=Path,required=True)
    p.add_argument('--current-suite',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    old=stats(read_baseline(a.baseline_zip));new=stats(read_current(a.current_suite))
    result={'metric':'static_skill_and_global_instructions_only',
            'baseline':old,'optimized':new,
            'reduction_utf8_bytes_percent':round(100*(1-new['bytes_utf8']/old['bytes_utf8']),2),
            'reduction_whitespace_words_percent':round(100*(1-new['whitespace_words']/old['whitespace_words']),2),
            'old_review_invocations':7,'new_review_invocations':3,
            'review_invocation_reduction_percent':round(100*(1-3/7),2),
            'caveat':'NOT measured API tokens. Actual tokens depend on tokenizer, retrieved sources, prompts, repeated context, caching and model routing.'}
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text+'\n',encoding='utf-8')
    print(text)

if __name__=='__main__':main()
