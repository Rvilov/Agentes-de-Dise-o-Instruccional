#!/usr/bin/env python3
"""Return a compact, reviewer-scoped set of Content QA controls. Never load the 97-slide index."""
import argparse
import json
from pathlib import Path


def select(root, agents):
    register=json.loads((root/'references/content-qa-control-register.json').read_text(encoding='utf-8'))
    wanted=set(agents)
    return [{'id':c['id'],'slides':c['source_slides'],'check':c['check']}
            for c in register['controls'] if wanted.intersection(c['agents'])]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument('--agents',required=True,help='Comma-separated reviewer IDs')
    ap.add_argument('--out',type=Path)
    a=ap.parse_args()
    result={'agents':a.agents.split(','),'controls':select(a.root,a.agents.split(','))}
    dump=json.dumps(result,ensure_ascii=False,separators=(',',':'))
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(dump+'\n',encoding='utf-8')
    else:print(dump)

if __name__=='__main__':main()
