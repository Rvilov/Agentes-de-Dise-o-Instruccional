#!/usr/bin/env python3
"""Audit contextual Rise/video art direction from QA manifest; never invent links.

Usage: audit_visual_plan.py qa/R1.manifest.json --docx outputs/R1.docx --strict

This is a consistency gate, not a visual relevance check or URL availability test.
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET

INTERACTIVE_TYPES = {'tabs', 'tab', 'accordion', 'acordeon', 'acordeón', 'pestanas', 'pestañas'}
PLANNABLE = {'stock_image','custom_image','image','illustration','diagram','icon','interface','screenshot','none'}
STOCK_TYPES = {'stock_video','stock_image'}
SCREEN_TEXT = {'lower_third','pleca','pop_up','popup','big_caption'}
GRAPHICS = {'mind_map','pyramid','flowchart','timeline','process','comparison','hierarchy','table','diagram'}
PENDING = {'pending','pendiente','PENDIENTE_STOCK_VIDEO','PENDIENTE_STOCK_IMAGEN'}


def valid_asset_url(value):
    if not isinstance(value, str):
        return False
    v=value.strip()
    if not v or re.search(r'(example\.|placeholder|your[-_ ]?url|\[|\]|PENDIENTE|link_del|enlace_|xxx|localhost)',v,re.I):
        return False
    try:
        u=urlparse(v)
    except ValueError:
        return False
    if u.scheme != 'https' or not u.netloc or '.' not in u.netloc:
        return False
    # Avoid generic search pages offered as a selected asset.
    if re.search(r'/(search|results)(/|\?|$)',u.path,re.I) or re.search(r'(^|&)q=|(^|&)search=',u.query,re.I):
        return False
    return True


def word_external_links(filename):
    with zipfile.ZipFile(filename) as z:
        rels='word/_rels/document.xml.rels'
        if rels not in z.namelist() or 'word/document.xml' not in z.namelist():
            return set()
        relationships=ET.fromstring(z.read(rels))
        external={n.get('Id'):n.get('Target') for n in relationships
                  if n.get('TargetMode')=='External' and 'hyperlink' in n.get('Type','').lower()}
        doc=ET.fromstring(z.read('word/document.xml'))
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        rid='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
        return {external[h.get(rid)] for h in doc.findall('.//w:hyperlink',ns) if h.get(rid) in external}


def rise_editorial_image_counts(filename):
    """Count actual Word visuals in the two-column DI layout without equating text links with images."""
    W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(filename) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    for table in root.iter(W+'tbl'):
        rows=table.findall(W+'tr')
        if not rows: continue
        header=rows[0].findall(W+'tc')
        if len(header)!=2: continue
        lt=''.join(x.text or '' for x in header[0].iter(W+'t')).casefold()
        rt=''.join(x.text or '' for x in header[1].iter(W+'t')).casefold()
        if 'notas de edici' not in lt or 'contenido del recurso' not in rt: continue
        left=right=0
        for row in rows[1:]:
            cells=row.findall(W+'tc')
            if len(cells)!=2: continue
            left+=sum(x.tag in (W+'drawing',W+'pict') for x in cells[0].iter())
            right+=sum(x.tag in (W+'drawing',W+'pict') for x in cells[1].iter())
        return {'notes_images':left,'content_images':right}
    return None

def text_set(v):
    return isinstance(v,str) and bool(v.strip())


def audit(manifest, docx=None):
    errors=[]; pending=[]; passes=[]
    def err(code,message):errors.append({'code':code,'message':message})
    def pen(code,message):pending.append({'code':code,'message':message})
    def ok(code,message):passes.append({'code':code,'message':message})
    if not isinstance(manifest,dict):
        return [{'code':'MANIFEST_INVALID','message':'Manifest no es objeto JSON'}],[],[]
    plan=manifest.get('visual_plan',{})
    if plan is None:plan={}
    if not isinstance(plan,dict):
        err('VISUAL_PLAN_INVALID','visual_plan debe ser objeto')
        return errors,pending,passes
    blocks=plan.get('blocks',[]) or []
    scenes=plan.get('video_scenes',[]) or []
    interactions=manifest.get('interactions',[]) or []
    if not isinstance(blocks,list) or not isinstance(scenes,list):
        err('PLAN_SHAPE','blocks y video_scenes deben ser listas')
        return errors,pending,passes
    links=None
    if docx:
        try:links=word_external_links(docx)
        except Exception as exc:err('DOCX_READ_FAILED',f'No se pudieron leer hipervínculos de Word: {exc}')

    # In Rise the images must accompany the learning content, not the editor notes.
    if docx and str(manifest.get('type','')).strip().lower() in {
        'rise','rise_interactive','lectura_interactiva','lectura interactiva','interactivo','interactive'
    }:
        try:
            counts=rise_editorial_image_counts(docx)
        except Exception as exc:
            err('RISE_EDITORIAL_DOCUMENT_UNREADABLE',str(exc))
            counts=None
        if counts is None:
            err('RISE_EDITORIAL_TABLE_NOT_FOUND','Falta tabla de dos columnas Notas/Contenido')
        else:
            if counts['notes_images']:
                err('RISE_IMAGE_IN_NOTES_COLUMN',f'{counts["notes_images"]} visuales en notas; ubicar en Contenido del Recurso')
            required=sum(
                1 for block in blocks if isinstance(block,dict)
                for item in (block.get('items') or []) if isinstance(item,dict)
                for visual in [item.get('visual') or {}] if isinstance(visual,dict)
                and str(visual.get('kind','')).lower() in {'stock_image','custom_image','image','illustration','screenshot'}
                and str(visual.get('status','')).lower() not in {'pending','pendiente','pendiente_stock_imagen'}
            )
            if counts['content_images']<required:
                err('RISE_CONTENT_IMAGES_INCOMPLETE',f'{required} imágenes comprometidas en plan, solo {counts["content_images"]} incrustadas en Contenido')
            else:
                ok('RISE_CONTENT_IMAGE_PLACEMENT',f'{counts["content_images"]} visuales en Contenido del Recurso; 0 en Notas requerido')

    # Cross-check declared Rise blocks that need item-level decisions.
    declared=[]
    for item in interactions:
        kind=item.get('kind','') if isinstance(item,dict) else ''
        if kind.lower() in INTERACTIVE_TYPES: declared.append(kind.lower())
    represented=[str(b.get('kind','')).lower() for b in blocks if isinstance(b,dict)]
    if str(manifest.get('type','')).strip().lower() in {'video','video_explicativo','video pro','video corto'} and not scenes:
        err('VIDEO_SCENES_NOT_PLANNED','Recurso de video sin decisiones por escena en visual_plan.video_scenes')

    for kind in set(declared):
        equivalent={'tabs','tab','pestanas','pestañas'} if kind in {'tabs','tab','pestanas','pestañas'} else {'accordion','acordeon','acordeón'}
        if not any(x in equivalent for x in represented):
            err('RISE_VISUAL_PLAN_ABSENT',f'Interacción {kind} declarada sin bloque visual en visual_plan.blocks')

    tab_names={'tabs','tab','pestanas','pestañas'}
    accordion_names={'accordion','acordeon','acordeón'}
    for group,label in [(tab_names,'tabs'),(accordion_names,'accordion')]:
        original=sum(1 for kind in declared if kind in group)
        planned=sum(1 for kind in represented if kind in group)
        if planned < original:
            err('RISE_BLOCK_COVERAGE_INCOMPLETE',f'{label}: {original} bloques declarados, {planned} bloques con decisiones visuales')

    for i,b in enumerate(blocks,1):
        place=f'block[{i}]'
        if not isinstance(b,dict):err('BLOCK_TYPE',f'{place} no es objeto');continue
        kind=str(b.get('kind','')).lower()
        if kind not in INTERACTIVE_TYPES:continue
        items=b.get('items',[])
        if not isinstance(items,list) or not items:
            err('RISE_NO_ITEMS',f'{place} ({kind}) sin items para verificar');continue
        for j,item in enumerate(items,1):
            loc=f'{place}.items[{j}]'
            if not isinstance(item,dict):err('RISE_ITEM_TYPE',f'{loc} no es objeto');continue
            v=item.get('visual')
            if not isinstance(v,dict):
                err('RISE_ITEM_VISUAL_MISSING',f'{loc} no incluye visual o alternativa justificada');continue
            k=str(v.get('kind','')).lower()
            if k not in PLANNABLE:
                err('RISE_ITEM_VISUAL_KIND',f'{loc} visual.kind no aceptado: {k}');continue
            if k=='none':
                if not text_set(v.get('justification')):
                    err('RISE_NO_VISUAL_UNJUSTIFIED',f'{loc} sin imagen y sin justificación de excepción')
                else:ok('RISE_VISUAL_EXCEPTION',f'{loc}: {v["justification"]}')
            else:
                if not text_set(v.get('description')) or not text_set(v.get('purpose')):
                    err('RISE_VISUAL_UNSPECIFIED',f'{loc} necesita description y purpose editables')
                else:ok('RISE_VISUAL_PLANNED',f'{loc} tiene visual pertinente definido para edición')
                if k=='stock_image':validate_stock(v,loc,err,pen,ok,links)

    for i,scene in enumerate(scenes,1):
        loc=f'video_scenes[{i}]'
        if not isinstance(scene,dict):err('SCENE_TYPE',f'{loc} no es objeto');continue
        if not text_set(scene.get('cue')):
            err('SCENE_CUE_MISSING',f'{loc}: falta indicación del momento narrativo (cue)')
        visuals=scene.get('visuals',[])
        if not isinstance(visuals,list) or not visuals:
            err('SCENE_VISUAL_DECISION_MISSING',f'{loc}: elegir talento en cámara o apoyo visual en visuals[]');continue
        for j,v in enumerate(visuals,1):
            position=f'{loc}.visuals[{j}]'
            if not isinstance(v,dict):err('SCENE_VISUAL_TYPE',f'{position} no es objeto');continue
            kind=str(v.get('kind','')).lower()
            if kind=='talent_only':
                ok('TALENT_ONLY',f'{position}: escena con talento a cámara')
                continue
            if not text_set(v.get('purpose')):
                err('SCENE_VISUAL_PURPOSE_MISSING',f'{position}: falta propósito del visual')
            if kind in SCREEN_TEXT and not text_set(v.get('on_screen_text')):
                err('SCREEN_TEXT_MISSING',f'{position} ({kind}): escribir el texto exacto que aparecerá')
            if kind in GRAPHICS and not text_set(v.get('description')):
                err('GRAPHIC_NOT_SPECIFIED',f'{position} ({kind}): describir componentes y relaciones que se mostrarán')
            if kind in STOCK_TYPES:
                validate_stock(v,position,err,pen,ok,links)

    # Catch stock video in legacy manifest visuals[] too; let older manifests be valid when not used.
    for i,v in enumerate(manifest.get('visuals',[]) or [],1):
        if not isinstance(v,dict):continue
        if str(v.get('kind','')).lower()=='stock_video':
            validate_stock(v,f'visuals[{i}]',err,pen,ok,links,legacy=True)
    return errors,pending,passes


def validate_stock(v,loc,err,pen,ok,links,legacy=False):
    kind=str(v.get('kind','')).lower()
    pending_state=str(v.get('status','')).lower() in {x.lower() for x in PENDING}
    url=v.get('url','')
    if pending_state:
        if valid_asset_url(url):
            err('STOCK_STATUS_CONTRADICTION',f'{loc}: declara pendiente pese a tener URL de asset; resolver estado')
        elif not text_set(v.get('search_terms')):
            err('STOCK_PENDING_WITHOUT_SEARCH',f'{loc}: pendiente sin términos de búsqueda para el editor')
        else:
            pen('PENDIENTE_STOCK_VIDEO' if kind=='stock_video' else 'PENDIENTE_STOCK_IMAGEN',f'{loc}: falta enlace de asset; no declarar listo para edición')
        return
    if not valid_asset_url(url):
        err('STOCK_LINK_REQUIRED',f'{loc}: {kind} concreto sin URL https válida (o estado pending + search_terms)')
        return
    if kind=='stock_video' and links is not None and url not in links:
        err('STOCK_VIDEO_WORD_HYPERLINK_MISSING',f'{loc}: {url} no existe como hipervínculo real en Word')
        return
    ok('STOCK_REAL_LINK',f'{loc}: URL de asset presente'+(' y enlazada en Word' if kind=='stock_video' and links is not None else ''))


def main():
    ap=argparse.ArgumentParser(description='Auditor Rise+video contextual de manifest de producción')
    ap.add_argument('manifest',help='Manifest interno QA de recurso (.json)')
    ap.add_argument('--docx',help='Word final para comprobar links de video-stock')
    ap.add_argument('--strict',action='store_true',help='Salida 1 si hay errores de consistencia')
    ap.add_argument('--require-ready',action='store_true',help='Salida 1 cuando quedan assets pendientes')
    args=ap.parse_args()
    manifest=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    errors,pending,passes=audit(manifest,args.docx)
    state='INVALID' if errors else 'IMPLEMENTATION_PENDING' if pending else 'READY'
    print(json.dumps({'manifest':args.manifest,'docx':args.docx,'state':state,'errors':errors,'pending':pending,'passes':passes},ensure_ascii=False,indent=2))
    if (args.strict and errors) or (args.require_ready and (pending or errors)):
        sys.exit(1)

if __name__=='__main__':main()
