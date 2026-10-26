#!/usr/bin/env python3
import argparse, zipfile, xml.etree.ElementTree as ET, json
WP='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('docx'); args=ap.parse_args()
    with zipfile.ZipFile(args.docx) as z:
        root=ET.fromstring(z.read('word/document.xml'))
        items=[]
        for d in root.iter('{%s}docPr'%WP):
            items.append({'name':d.attrib.get('name',''),'title':d.attrib.get('title',''),'descr':d.attrib.get('descr','')})
        missing=[x for x in items if not (x['title'].strip() or x['descr'].strip())]
    print(json.dumps({'images_with_docPr':len(items),'missing_alt_or_title':missing,'count_missing':len(missing)},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
