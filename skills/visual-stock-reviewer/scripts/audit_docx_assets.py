#!/usr/bin/env python3
import argparse, zipfile, xml.etree.ElementTree as ET, json, re
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PKG='http://schemas.openxmlformats.org/package/2006/relationships'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('docx'); args=ap.parse_args()
    with zipfile.ZipFile(args.docx) as z:
        names=z.namelist()
        images=[n for n in names if n.startswith('word/media/')]
        rels={}
        relname='word/_rels/document.xml.rels'
        if relname in names:
            root=ET.fromstring(z.read(relname))
            for rel in root:
                rid=rel.attrib.get('Id'); target=rel.attrib.get('Target',''); mode=rel.attrib.get('TargetMode','')
                rels[rid]={'target':target,'external':mode=='External'}
        root=ET.fromstring(z.read('word/document.xml'))
        links=[]
        for h in root.findall('.//w:hyperlink',NS):
            rid=h.attrib.get('{%s}id'%NS['r'])
            text=''.join(t.text or '' for t in h.findall('.//w:t',NS)).strip()
            if rid in rels:
                links.append({'text':text,'url':rels[rid]['target'],'external':rels[rid]['external']})
        result={'docx':args.docx,'embedded_images':len(images),'images':images,'hyperlinks':links,
                'magnific_links':[x for x in links if 'magnific.com' in x['url'].lower()]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
