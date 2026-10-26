#!/usr/bin/env python3
import argparse, json, collections
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); args=ap.parse_args()
    data=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    keys=data.get('evaluation_key',[])
    letters=[]
    for x in keys:
        if isinstance(x,str): ans=x
        elif isinstance(x,dict): ans=x.get('correct') or x.get('answer') or ''
        else: ans=''
        ans=str(ans).strip().upper()
        if ans in {'A','B','C','D'}: letters.append(ans)
    c=collections.Counter(letters); total=len(letters)
    dominant=(max(c.values())/total) if total else 0
    flag= total>=6 and dominant>0.5
    print(json.dumps({'multiple_choice_items':total,'distribution':dict(sorted(c.items())),
                      'dominant_ratio':round(dominant,3),'pattern_risk':flag},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
