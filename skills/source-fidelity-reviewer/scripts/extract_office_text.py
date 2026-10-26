#!/usr/bin/env python3
import argparse, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def docx(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    out=[]
    for p in root.findall('.//w:p',NS):
        t=''.join(x.text or '' for x in p.findall('.//w:t',NS)).strip()
        if t: out.append(t)
    return '\n'.join(f'P{i+1}: {t}' for i,t in enumerate(out))

def pptx(path):
    with zipfile.ZipFile(path) as z:
        names=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        def num(n):
            s=n.split('slide')[-1].split('.xml')[0]
            try:return int(s)
            except:return 999999
        names.sort(key=num)
        blocks=[]
        for n in names:
            root=ET.fromstring(z.read(n))
            texts=[x.text or '' for x in root.findall('.//a:t',NS)]
            blocks.append(f"SLIDE {num(n)}:\n"+' '.join(texts))
    return '\n\n'.join(blocks)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); args=ap.parse_args()
    p=Path(args.file); ext=p.suffix.lower()
    if ext=='.docx': print(docx(p))
    elif ext=='.pptx': print(pptx(p))
    else: raise SystemExit('Supported: .docx, .pptx')
if __name__=='__main__': main()
