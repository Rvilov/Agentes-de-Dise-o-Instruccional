#!/usr/bin/env python3
"""Gate that couples a visual decision to evidence of actual stock search.

No internet calls: requires a source-tool result reference and candidate evidence
recorded at execution time. It does not prove a third-party URL is currently live
or that a photograph is instructionally appropriate. Human visual QA remains required.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from docx import Document
from docx.oxml.ns import qn

STOCK_TYPES={'stock_image','stock_video'}
BAD_URL=re.compile(r'example\.|placeholder|your.?url|link_del|enlace_|localhost|/search(?:/|\?|$)|/results(?:/|\?|$)',re.I)
UNHELPFUL=re.compile(r'^(?:no aplica|n/a|ningun[ao]?|no se necesita|sin stock|imagen generica|opcional|por estilo|sin motivo)\.?$',re.I)


def url_ok(s):
    if not isinstance(s,str) or BAD_URL.search(s):return False
    try:
        u=urlparse(s)
        return u.scheme=='https' and bool(u.netloc and '.' in u.netloc)
    except ValueError:return False


def good_reason(reason):
    return isinstance(reason,str) and len(reason.strip())>=18 and not UNHELPFUL.fullmatch(reason.strip())


def find_rows(docx):
    d=Document(docx)
    found=[]
    for table in d.tables:
        for i,row in enumerate(table.rows):
            if len(row.cells)<2:continue
            if 'notas de edici' in row.cells[0].text.casefold() and 'contenido del recurso' in row.cells[1].text.casefold():
                found.append((table,i))
    if len(found)!=1:raise ValueError('Falta una tabla editorial unica')
    table,index=found[0]
    return [(row.cells[0],row.cells[1]) for row in table.rows[index+1:] if len(row.cells)>=2]


def image_count(cell):
    return sum(1 for x in cell._tc.iter() if x.tag in (qn('w:drawing'),qn('w:pict')))


def link_targets(cell):
    targets=[]
    for h in cell._tc.iter(qn('w:hyperlink')):
        rid=h.get(qn('r:id'))
        if rid and rid in cell.part.rels:targets.append(cell.part.rels[rid].target_ref)
    return targets


def audit(contract, log, docx=None):
    errors=[];pending=[];passes=[];warnings=[]
    def issue(code,msg,where=None):errors.append({'code':code,'where':where,'message':msg})
    def wait(code,msg,where=None):pending.append({'code':code,'where':where,'message':msg})
    blocks=contract.get('blocks',[])
    search_list=log.get('searches',[])
    if not isinstance(blocks,list) or not blocks:issue('NO_EDITORIAL_BLOCKS','No hay bloques de produccion')
    if not isinstance(search_list,list):issue('SEARCH_LOG_INVALID','El log debe incluir searches[]');search_list=[]
    index={}
    for s in search_list:
        if not isinstance(s,dict):issue('SEARCH_RECORD_INVALID','Un registro de busqueda no es objeto');continue
        key=s.get('asset_id')
        if not key:issue('SEARCH_ASSET_ID_MISSING','Falta asset_id en log');continue
        if key in index:issue('DUPLICATE_STOCK_SEARCH',str(key));continue
        index[key]=s
    rows=[]
    if docx:
        try:rows=find_rows(docx)
        except Exception as exc:issue('DOCX_EDITORIAL_ROWS_MISSING',str(exc))
        if len(rows)!=len(blocks):issue('WORD_BLOCK_COUNT_MISMATCH',f'{len(rows)} filas Word vs {len(blocks)} en contrato')
    selected_refs=set();seen_queries=[];all_non_stock=True
    for i,b in enumerate(blocks,1):
        if not isinstance(b,dict):issue('BLOCK_INVALID','Bloque no es objeto',str(i));continue
        block_id=str(b.get('id') or i)
        decision=b.get('stock_decision')
        if not isinstance(decision,dict) or not isinstance(decision.get('needed'),bool):
            issue('STOCK_DECISION_REQUIRED','Cada bloque necesita stock_decision.needed y razon',block_id);continue
        if not good_reason(decision.get('reason')):
            issue('STOCK_DECISION_REASON_EMPTY','Explicar decision contextual concreta, no solo no aplica',block_id)
        asset_ids=b.get('stock_assets',[])
        if not isinstance(asset_ids,list):
            issue('STOCK_ASSET_LIST_INVALID','stock_assets debe ser lista',block_id);asset_ids=[]
        if len(asset_ids)!=len(set(asset_ids)):
            issue('DUPLICATE_ASSET_IN_BLOCK','Asset duplicado',block_id)
        if decision['needed'] and not asset_ids:
            issue('REQUIRED_STOCK_WITHOUT_ASSET','El bloque demanda stock pero no registra ninguna busqueda/asset',block_id)
        if not decision['needed'] and asset_ids:
            issue('STOCK_DECISION_CONTRADICTION','Hay assets stock pero se declaro needed=false',block_id)
        if decision['needed']:all_non_stock=False
        visuals=b.get('visuals')
        if not isinstance(visuals,list) or not visuals:
            issue('BLOCK_VISUAL_DECISION_MISSING','Indicar visual seleccionado: stock, diagrama, interfaz, icono, texto o talento',block_id)
        else:
            for v in visuals:
                if not isinstance(v,dict) or not v.get('kind') or not good_reason(v.get('purpose','')):
                    issue('VISUAL_PURPOSE_MISSING','Cada visual requiere kind y purpose especificos',block_id)
        # Every tab/accordion panel gets its own grounded decision. No stock quota.
        if str(b.get('block_kind','')).casefold() in {'tabs','tab','pestanas','pesta\u00f1as','accordion','acordeon','acorde\u00f3n'}:
            panels=b.get('panels')
            if not isinstance(panels,list) or not panels:
                issue('PANEL_DECISIONS_MISSING','Tabs/acordeon sin decisiones por panel',block_id)
            else:
                for pidx,panel in enumerate(panels,1):
                    if not isinstance(panel,dict) or not panel.get('kind') or not good_reason(panel.get('purpose','')):
                        issue('PANEL_VISUAL_UNDEFINED','Falta visual o razon por panel',f'{block_id}.panel{pidx}')
                    if isinstance(panel,dict) and panel.get('kind') in STOCK_TYPES and panel.get('asset_id') not in asset_ids:
                        issue('PANEL_STOCK_ASSET_UNTRACKED','Asset de panel no figura en stock_assets',f'{block_id}.panel{pidx}')
        expected_images=0
        for aid in asset_ids:
            r=index.get(aid)
            if not r:
                issue('STOCK_SEARCH_NOT_EXECUTED','No existe evidencia de busqueda real para '+str(aid),block_id);continue
            selected_refs.add(aid)
            if str(r.get('block_id',''))!=block_id:
                issue('STOCK_SEARCH_WRONG_BLOCK','El registro no esta asociado a este bloque',block_id)
            status=str(r.get('status','')).strip()
            if status not in {'selected','no_match','access_blocked'}:
                issue('STOCK_SEARCH_STATUS_INVALID','status debe ser selected, no_match o access_blocked',aid);continue
            if not str(r.get('provider','')).strip() or not str(r.get('query','')).strip():
                issue('STOCK_SEARCH_QUERY_MISSING','Registrar proveedor y terminos especificos',aid)
            if len(str(r.get('query','')).strip())<12:
                issue('STOCK_SEARCH_QUERY_GENERIC','Busqueda demasiado generica; describir accion/objeto/escenario',aid)
            seen_queries.append(str(r.get('query','')).lower().strip())
            stamp=r.get('searched_at')
            try:
                if not stamp:raise ValueError('empty')
                datetime.fromisoformat(str(stamp).replace('Z','+00:00'))
            except (ValueError,TypeError):issue('STOCK_SEARCH_DATE_MISSING','Registrar marca de ejecucion ISO-8601',aid)
            evidence=r.get('evidence') or {}
            if status in {'selected','no_match'} and (not isinstance(evidence,dict) or not str(evidence.get('tool','')).strip() or not (str(evidence.get('result_ref','')).strip() or evidence.get('result_snapshot'))):
                issue('STOCK_TOOL_EVIDENCE_MISSING','Busqueda real requiere herramienta y resultado recuperado, no un supuesto',aid)
            if status=='access_blocked':
                if not str(r.get('error','')).strip():issue('STOCK_ACCESS_ERROR_MISSING','Explicar por que no pudo usar la herramienta',aid)
                wait('STOCK_ACCESS_BLOCKED','No fue posible ejecutar la busqueda; entregar pendiente, no READY',aid)
            elif status=='no_match':
                attempts=r.get('attempted_queries')
                if not isinstance(attempts,list) or len(attempts)<2:
                    issue('STOCK_SEARCH_RETRY_REQUIRED','Sin resultados: registrar al menos dos consultas reales',aid)
                wait('STOCK_SEARCH_NO_MATCH','Se busco sin encontrar asset adecuado; no publicar como listo',aid)
            else:
                candidates=r.get('candidates')
                selected=r.get('selected') or {}
                if not isinstance(candidates,list) or not candidates:
                    issue('STOCK_CANDIDATES_MISSING','Seleccionar de candidatos recuperados, no inventar URLs',aid);continue
                if not isinstance(selected,dict) or not url_ok(selected.get('url')) or not selected.get('title'):
                    issue('STOCK_SELECTED_INVALID','Seleccion requiere titulo y URL de pieza concreta',aid);continue
                if not any(isinstance(c,dict) and c.get('url')==selected['url'] for c in candidates):
                    issue('STOCK_NOT_IN_RESULTS','URL seleccionada no figura en candidatos de busqueda',aid)
                if not url_ok(selected['url']):
                    issue('STOCK_URL_NOT_PERSISTENT','Utilizar enlace autentico al asset; no enlaces efimeros de descarga',aid)
                asset_kind=str(r.get('kind',''))
                if asset_kind not in STOCK_TYPES:issue('STOCK_KIND_INVALID','stock_image o stock_video',aid)
                if asset_kind=='stock_image':expected_images+=1
                if docx and i<=len(rows):
                    left,right=rows[i-1]
                    if asset_kind=='stock_video' and selected['url'] not in link_targets(left):
                        issue('STOCK_VIDEO_LINK_MISSING_IN_NOTES','Video stock requiere enlace real en nota',aid)
                    if asset_kind=='stock_image' and selected['url'] not in link_targets(right):
                        issue('STOCK_IMAGE_LINK_MISSING_IN_CONTENT','Imagen de stock requiere enlace al asset en contenido',aid)
                passes.append({'code':'STOCK_SEARCH_EXECUTED','asset_id':aid,'provider':r.get('provider')})
        if docx and i<=len(rows) and expected_images:
            image_total=image_count(rows[i-1][1])
            if image_total < expected_images:
                issue('STOCK_IMAGE_NOT_EMBEDDED_IN_BLOCK',f'Se esperan {expected_images} imagenes stock en Contenido; hay {image_total}',block_id)
    # A clip referenced from Notas must match the selected search result.
    for b in blocks:
        if not isinstance(b,dict):continue
        for link in b.get('stock_video_links',[]):
            if not isinstance(link,dict):continue
            aid=link.get('asset_id');found=index.get(aid,{})
            if aid not in b.get('stock_assets',[]):
                issue('VIDEO_LINK_ASSET_NOT_DECLARED','Un link en notas no esta registrado en stock_assets',aid)
            selected=found.get('selected') or {}
            if found.get('status')!='selected' or selected.get('url')!=link.get('url'):
                issue('VIDEO_LINK_NOT_FROM_SEARCH','El enlace en Notas no coincide con asset seleccionado de busqueda',aid)
    orphan=set(index)-selected_refs
    if orphan:
        warnings.append({'code':'UNUSED_STOCK_RECORDS','asset_ids':sorted(orphan)})
    if all_non_stock and len(blocks)>=3:
        review=log.get('all_no_stock_review') or {}
        if (review.get('reviewer')!='visual-stock-reviewer'
                or review.get('accepted') is not True
                or not good_reason(review.get('rationale'))):
            wait('NO_STOCK_INDEPENDENT_REVIEW_PENDING','Recurso extenso sin stock; revisor visual debe confirmar pertinencia de alternativas por bloque')
        else:
            passes.append({'code':'NO_STOCK_INDEPENDENT_REVIEW_ACCEPTED','rationale':review['rationale']})
    state='INVALID' if errors else 'IMPLEMENTATION_PENDING' if pending else 'READY_FOR_VISUAL_REVIEW'
    return {'state':state,'pass_delivery':not errors and not pending,'errors':errors,'pending':pending,
            'warnings':warnings,'passes':passes,'blocks':len(blocks),
            'note':'Evidencias declaradas y OOXML; el revisor debe verificar manualmente resultados del proveedor, URL activa, derechos y pertinencia.'}


def main():
    ap=argparse.ArgumentParser(description='Verifica decisiones visuales, busquedas reales y ubicacion de stock')
    ap.add_argument('--contract',type=Path,required=True)
    ap.add_argument('--search-log',type=Path,required=True)
    ap.add_argument('--docx',type=Path)
    ap.add_argument('--json-out',type=Path)
    ap.add_argument('--strict',action='store_true')
    opt=ap.parse_args()
    contract=json.loads(opt.contract.read_text(encoding='utf-8'))
    log=json.loads(opt.search_log.read_text(encoding='utf-8'))
    result=audit(contract,log,opt.docx)
    rendered=json.dumps(result,ensure_ascii=False,indent=2);print(rendered)
    if opt.json_out:opt.json_out.write_text(rendered+'\n',encoding='utf-8')
    if opt.strict and not result['pass_delivery']:sys.exit(1)

if __name__=='__main__':main()
