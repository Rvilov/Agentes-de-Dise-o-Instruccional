#!/usr/bin/env python3
"""Audit Rise Word editorial conventions: short notes left, real visuals with content right.

This checks structure, not visual relevance, factual accuracy or stock licenses.
Any sample Word used to derive this policy is a structure reference only.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WORD=re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*",re.UNICODE)
TIMECODE=re.compile(r'(?<!\d)\d{1,2}:\d{2}(?::\d{2})?\s*[\-–—]\s*\d{1,2}:\d{2}(?::\d{2})?(?!\d)')
META_PATTERNS=(
    ('NO_ACCESS_CONTINGENCY',r'\bsi\s+a[uú]n\s+no\s+tienes\s+acceso\b'),
    ('VISUAL_JUSTIFICATION_IN_NOTES',r'\bexcepci[oó]n\s+visual\s+justificada\b'),
    ('TECHNICAL_FALLBACK_IN_NOTES',r'\b(?:si\s+no\s+existe\s+el\s+bloque|si\s+no\s+puedes\s+enlazar|si\s+no\s+se\s+puede\s+acceder)\b'),
    ('QA_STATUS_IN_NOTES',r'\b(?:PENDIENTE_STOCK(?:_IMAGEN|_VIDEO)?|VALIDACI[OÓ]N\s+QA|EXCEPCI[OÓ]N\s+QA)\b'),
)
IMAGE_HINT=re.compile(r'\b(?:imagen|im[aá]genes|fotograf[ií]a|foto|captura(?:s)?\s+de\s+pantalla)\b',re.I)


def text(element):
    paragraphs=[]
    for p in element.iter(W+'p'):
        chunks=[]
        for el in p.iter():
            if el.tag==W+'t' and el.text:
                chunks.append(el.text)
            elif el.tag in {W+'br',W+'cr'}:
                chunks.append('\n')
        if chunks:
            paragraphs.append(''.join(chunks))
    return '\n'.join(paragraphs).strip()


def image_count(element):
    return sum(1 for el in element.iter() if el.tag in {W+'drawing',W+'pict'})


def row_cells(row):
    return row.findall(W+'tc')


def audit(docx:Path, max_words:int=60, allow_timecodes=False, force_rise=False):
    errors=[]; warnings=[]; sections=[]
    with zipfile.ZipFile(docx) as z:
        doc=ET.fromstring(z.read('word/document.xml'))
    all_content=text(doc)
    is_rise=force_rise or bool(re.search(r'\bRise\b|\blectura\s+interactiva\b',all_content,re.I))
    if not is_rise:
        return {'file':str(docx),'is_rise':False,'pass_delivery':True,'issues':[],
                'warnings':['NOT_RISE_DOCUMENT: No se aplicaron gates de Rise.'], 'sections':[]}
    matches=[]
    for t in doc.iter(W+'tbl'):
        rs=t.findall(W+'tr')
        if not rs:continue
        head=row_cells(rs[0])
        if len(head)>=2 and 'notas de edici' in text(head[0]).casefold() and 'contenido del recurso' in text(head[-1]).casefold():
            matches.append((t,rs))
    if len(matches)!=1:
        errors.append({'code':'RISE_EDITORIAL_TWO_COLUMNS_REQUIRED','detail':f'Se esperaba 1 tabla editorial Notas/Contenido; encontradas {len(matches)}.'})
        return {'file':str(docx),'is_rise':True,'pass_delivery':False,'issues':errors,'warnings':warnings,'sections':sections}
    _,rows=matches[0]
    for idx,row in enumerate(rows[1:],1):
        cells=row_cells(row)
        if len(cells)!=2:
            errors.append({'code':'RISE_EDITORIAL_ROW_SHAPE','section':idx,'detail':f'Fila sin 2 columnas: {len(cells)}.'})
            continue
        left,right=cells
        notes=text(left)
        content=text(right)
        left_imgs=image_count(left)
        right_imgs=image_count(right)
        if not notes and not content and not right_imgs:
            continue
        words=len(WORD.findall(notes))
        sec={'index':idx,'note_words':words,'notes_images':left_imgs,'content_images':right_imgs,
             'section_title':notes.split('\n',1)[0][:100]}
        sections.append(sec)
        if words>max_words:
            errors.append({'code':'RISE_NOTES_EXCESSIVE','section':idx,'detail':f'{words} palabras; máximo {max_words}. Mover explicación al contenido/qa.'})
        elif words>45:
            warnings.append(f'SECTION_{idx}_NOTES_LONG: {words} palabras; objetivo 20-45.')
        if left_imgs:
            errors.append({'code':'RISE_IMAGE_IN_NOTES_COLUMN','section':idx,'detail':f'{left_imgs} imágenes/dibujos a la izquierda; mover al Contenido del Recurso.'})
        if not content and not right_imgs:
            errors.append({'code':'RISE_CONTENT_EMPTY','section':idx,'detail':'La sección no tiene texto ni elemento visual en Contenido del Recurso.'})
        if IMAGE_HINT.search(notes) and not right_imgs:
            errors.append({'code':'RISE_PROMISED_IMAGE_NOT_EMBEDDED','section':idx,
                           'detail':'Notas sugieren imagen/captura pero no hay una imagen real incrustada en la columna de contenido.'})
        if not allow_timecodes and TIMECODE.search(notes):
            errors.append({'code':'RISE_TIMECODES_IN_NOTES','section':idx,'detail':'Timecodes propios de video en interactivo Rise sin sincronización aprobada.'})
        for code,pattern in META_PATTERNS:
            if re.search(pattern,notes,re.I):
                errors.append({'code':'RISE_'+code,'section':idx,'detail':'Una explicación/contingencia de producción está visible en Notas de Edición.'})
        if notes and not re.search(r'\bRise\s*:',notes,re.I):
            warnings.append(f'SECTION_{idx}_BLOCK_NOT_LABELED: indicar Rise: [tipo de bloque]')
    return {'file':str(docx),'is_rise':True,'pass_delivery':not errors,'issues':errors,
            'warnings':warnings,'sections':sections,'max_words':max_words,
            'note':'Además de este gate, ejecutar audit_docx_structure y revisar cada página renderizada.'}


def main():
    ap=argparse.ArgumentParser(description='Revisa concisión de Notas Rise y fotos en columna de Contenido, no en Notas')
    ap.add_argument('docx')
    ap.add_argument('--max-words',type=int,default=60)
    ap.add_argument('--allow-timecodes',action='store_true',help='Solo para Rise con audio/video sincronizado y aprobación')
    ap.add_argument('--rise',action='store_true',help='Forzar verificación en caso de etiqueta ambigua')
    ap.add_argument('--json-out')
    ap.add_argument('--strict',action='store_true')
    args=ap.parse_args()
    result=audit(Path(args.docx),args.max_words,args.allow_timecodes,args.rise)
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload+'\n',encoding='utf-8')
    if args.strict and not result['pass_delivery']:
        sys.exit(1)

if __name__=='__main__': main()
