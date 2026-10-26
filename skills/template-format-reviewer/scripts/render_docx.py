#!/usr/bin/env python3
import argparse, shutil, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('docx'); ap.add_argument('--out',required=True); args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    libre=shutil.which('libreoffice') or shutil.which('soffice')
    if not libre: raise SystemExit('LibreOffice no disponible; marcar RENDER_NO_VERIFICADO')
    subprocess.run([libre,'--headless','--convert-to','pdf','--outdir',str(out),args.docx],check=True)
    pdf=out/(Path(args.docx).stem+'.pdf')
    pdftoppm=shutil.which('pdftoppm')
    if not pdftoppm: print(pdf); raise SystemExit(0)
    subprocess.run([pdftoppm,'-png','-r','144',str(pdf),str(out/'page')],check=True)
    print(pdf)
if __name__=='__main__': main()
