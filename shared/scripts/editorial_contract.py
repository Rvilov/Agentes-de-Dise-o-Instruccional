#!/usr/bin/env python3
"""Canonical, reproducible editorial notes for every Word resource.

The JSON blueprint is internal QA data. This tool touches ONLY the left notes
column; right-side content and embedded visuals are preserved. Use --audit
on final Word files, and --apply before visual render. It does not verify stock
search or visual relevance; audit_stock_execution.py owns those gates.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

LABELS = {
    'video': 'Video', 'rise': 'Rise', 'lectura': 'Lectura',
    'evaluacion': 'Evaluaci\u00f3n', 'descargable': 'Descargable',
    'infografia': 'Infograf\u00eda', 'otro': 'Recurso',
}
BAD_NOTE = re.compile(r'\b(?:si aun no|si a[u\u00fa]n no|excepci[o\u00f3]n visual justificada|motivo qa|material base|fuente factual|plan de b[u\u00fa]squeda|alternativamente|o bien se puede)\b', re.I)
TIMECODE = re.compile(r'^\d{1,2}:\d{2}(?:-\d{1,2}:\d{2})?$')
WORD = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*", re.UNICODE)


def canonical_type(raw):
    x = str(raw).casefold().strip()
    aliases = {'interactivo':'rise','lectura_interactiva':'rise','video_explicativo':'video',
               'video_pro':'video','video_corto':'video','evaluaci\u00f3n':'evaluacion',
               'infograf\u00eda':'infografia','one_pager':'descargable'}
    return aliases.get(x,x)


def load_contract(path):
    doc = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(doc,dict) or not isinstance(doc.get('blocks'), list) or not doc.get('blocks'):
        raise ValueError('Contrato sin blocks[]')
    kind = canonical_type(doc.get('resource_type',''))
    if kind not in LABELS:
        raise ValueError('resource_type no reconocido: '+str(kind))
    if not doc.get('resource_id'):
        raise ValueError('Falta resource_id')
    return doc,kind


def build_notes(block, idx, kind):
    errors=[]
    for key in ('id','title','format','direction','stock_decision'):
        if key not in block:
            errors.append('Falta '+key)
    if errors:
        return [],errors,[]
    title = str(block['title']).strip()
    form = str(block['format']).strip().strip('.')
    direction = str(block['direction']).strip()
    if not title or not form or not direction:
        errors.append('Titulo, formato y accion no pueden estar vacios')
    if re.match(r'^\s*\d+\s*[.)-]',title):
        errors.append('El numero es automatico; title no debe empezar por indice')
    if '\n' in title or '\n' in form or '\n' in direction:
        errors.append('Cada campo debe ser una sola linea; no escribir parrafos multiples')
    if BAD_NOTE.search(direction):
        errors.append('La accion incluye contingencias, QA o razonamientos')
    if direction.count(';')>=3:
        errors.append('Demasiadas instrucciones separadas por punto y coma')
    words=len(WORD.findall(title+' '+form+' '+direction))
    if words > 60:
        errors.append('Nota demasiado larga: %d palabras (max 60)'%words)
    sync=str(block.get('timecode','')).strip()
    if sync and kind!='video':
        errors.append('Timecode sincrono solo para video en este contrato')
    if sync and not TIMECODE.fullmatch(sync):
        errors.append('Formato timecode no valido (MM:SS-MM:SS)')
    if re.search(r'(?<!\d)\d{1,2}:\d{2}',title+' '+direction) and kind!='video':
        errors.append('No introducir timecodes en notas no audiovisuales')
    dec=block.get('stock_decision')
    if not isinstance(dec,dict) or not isinstance(dec.get('needed'),bool) or len(str(dec.get('reason','')).strip())<12:
        errors.append('stock_decision requiere needed boolean y reason concreto')
    line1='%d. %s%s'%(idx,title,(' ('+sync+')') if sync else '')
    line2='%s: %s.'%(LABELS[kind],form)
    line3=direction
    extras=[]
    for item in block.get('stock_video_links',[]):
        if kind != 'video':
            errors.append('stock_video_links solo para videos')
        if not isinstance(item,dict) or not item.get('asset_id') or not item.get('title') or not item.get('url'):
            errors.append('stock_video_links necesita asset_id/title/url')
            continue
        extras.append({'label':'Stock: '+str(item['title']).strip(), 'url':str(item['url']).strip(), 'asset_id':item['asset_id']})
    if words + sum(len(WORD.findall(x['label'])) for x in extras) > 60:
        errors.append('Nota + etiquetas de stock superan las 60 palabras')
    return [line1,line2,line3],errors,extras


def editorial_rows(doc):
    found=[]
    for table in doc.tables:
        rows=table.rows
        for i,row in enumerate(rows):
            if len(row.cells)<2: continue
            left=row.cells[0].text.casefold().replace('\n',' ')
            right=row.cells[1].text.casefold().replace('\n',' ')
            if 'notas de edici' in left and 'contenido del recurso' in right:
                found.append((table,i))
    if len(found)!=1:
        raise ValueError('Esperada una sola tabla editorial (Notas/Contenido); encontradas %d'%len(found))
    table,start=found[0]
    return [row.cells[0] for row in table.rows[start+1:] if len(row.cells)>=2]


def add_external_hyperlink(paragraph,label,url):
    part=paragraph.part
    rid=part.relate_to(url,RT.HYPERLINK,is_external=True)
    el=OxmlElement('w:hyperlink');el.set(qn('r:id'),rid)
    run=OxmlElement('w:r'); pr=OxmlElement('w:rPr')
    color=OxmlElement('w:color');color.set(qn('w:val'),'0563C1');pr.append(color)
    underline=OxmlElement('w:u');underline.set(qn('w:val'),'single');pr.append(underline)
    run.append(pr);tt=OxmlElement('w:t');tt.text=label;run.append(tt);el.append(run)
    paragraph._p.append(el)


def cell_external_links(cell):
    links=[]
    for el in cell._tc.iter(qn('w:hyperlink')):
        rid=el.get(qn('r:id'))
        if rid and rid in cell.part.rels:
            link=cell.part.rels[rid]
            links.append(link.target_ref)
    return links


def apply(docx,contract,out):
    d=Document(docx); cells=editorial_rows(d)
    if len(cells)!=len(contract['blocks']):
        raise ValueError('Numero filas Word (%d) distinto a contrato (%d)'%(len(cells),len(contract['blocks'])))
    kind=canonical_type(contract['resource_type']); issues=[]
    for i,(block,cell) in enumerate(zip(contract['blocks'],cells),1):
        lines,errors,extras=build_notes(block,i,kind)
        issues += [{'block':i,'issue':x} for x in errors]
        if errors:continue
        # Abort rather than silently destroy visuals mistakenly placed in notes.
        if any(x.tag in (qn('w:drawing'),qn('w:pict')) for x in cell._tc.iter()):
            raise ValueError('Imagen dentro de Notas; mover a Contenido antes de aplicar el contrato')
        # Keep the content column, table layout and styles unchanged.
        for p in cell.paragraphs:
            p._element.getparent().remove(p._element)
        p=cell.add_paragraph();p.add_run(lines[0]).bold=True
        p2=cell.add_paragraph();p2.add_run(lines[1]).bold=True
        p3=cell.add_paragraph();p3.add_run(lines[2])
        for item in extras:
            p4=cell.add_paragraph();add_external_hyperlink(p4,item['label'],item['url'])
    if issues:raise ValueError(json.dumps(issues,ensure_ascii=False))
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    d.save(out)


def audit(docx,contract):
    d=Document(docx);issues=[];summary=[]
    try:cells=editorial_rows(d)
    except ValueError as exc:return {'pass_delivery':False,'issues':[{'code':'TABLE_MISSING','detail':str(exc)}]}
    blocks=contract['blocks'];kind=canonical_type(contract['resource_type'])
    if len(cells)!=len(blocks):
        issues.append({'code':'BLOCK_ROW_COUNT_MISMATCH','expected':len(blocks),'actual':len(cells)})
    for i,(block,cell) in enumerate(zip(blocks,cells),1):
        result=build_notes(block,i,kind)
        lines,errors,extras=result
        for error in errors:issues.append({'code':'CONTRACT_BLOCK_INVALID','block':i,'detail':error})
        if errors:continue
        actual=[p.text.strip() for p in cell.paragraphs if p.text.strip()]
        # python-docx does not expose hyperlink text in paragraph.text in older releases.
        expected=lines + [e['label'] for e in extras]
        if actual != expected:
            issues.append({'code':'NOTES_NOT_CANONICAL','block':i,'expected':expected,'actual':actual})
        links=cell_external_links(cell)
        for extra in extras:
            if extra['url'] not in links:
                issues.append({'code':'STOCK_LINK_NOT_IN_NOTES','block':i,'asset_id':extra['asset_id']})
        if not extras and links:
            issues.append({'code':'UNDECLARED_URL_IN_NOTES','block':i,'urls':links})
        summary.append({'block_id':block['id'],'index':i,'notes_words':len(WORD.findall(' '.join(lines))),'stock_links':len(extras)})
    return {'pass_delivery':not issues,'issues':issues,'summary':summary,'resource_id':contract.get('resource_id')}


def main():
    p=argparse.ArgumentParser(description='Notas editoriales canonicas: aplicar o auditar')
    p.add_argument('command',choices=['apply','audit'])
    p.add_argument('--contract',required=True,type=Path)
    p.add_argument('--docx',required=True,type=Path)
    p.add_argument('--output',type=Path,help='DOCX nuevo para comando apply')
    p.add_argument('--json-out',type=Path)
    p.add_argument('--strict',action='store_true')
    args=p.parse_args();contract,_=load_contract(args.contract)
    if args.command=='apply':
        if not args.output:p.error('apply requiere --output')
        apply(args.docx,contract,args.output)
        report={'pass_delivery':True,'output':str(args.output),'status':'NOTES_APPLIED'}
    else:report=audit(args.docx,contract)
    s=json.dumps(report,ensure_ascii=False,indent=2);print(s)
    if args.json_out:args.json_out.write_text(s+'\n',encoding='utf-8')
    if args.strict and not report['pass_delivery']:raise SystemExit(1)

if __name__=='__main__':main()
