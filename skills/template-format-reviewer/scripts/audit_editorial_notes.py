#!/usr/bin/env python3
"""Universal DOCX editorial-notes audit for all course resource types.

Validates structural constraints only. Human QA must still judge whether a note
is useful, whether links are real, and whether visual decisions are appropriate.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WORD = re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*", re.UNICODE)
URL = re.compile(r'https?://\S+', re.I)
TIMECODE = re.compile(r'(?<!\d)\d{1,2}:\d{2}(?::\d{2})?\s*[-–—]\s*\d{1,2}:\d{2}(?::\d{2})?(?!\d)')
TECH_META = (
    ('NOTES_INTERNAL_QA', r'\b(?:PENDIENTE_STOCK(?:_VIDEO|_IMAGEN)?|VALIDACI[OÓ]N\s+QA|EXCEPCI[OÓ]N\s+QA|motivo\s+(?:del\s+)?QA|razonamiento\s+interno)\b'),
    ('NOTES_ACCESS_CONTINGENCY', r'\bsi\s+a[uú]n\s+no\s+tienes\s+acceso\b'),
    ('NOTES_TECHNICAL_FALLBACK', r'\b(?:si\s+no\s+existe\s+el\s+bloque|si\s+no\s+puedes\s+enlazar|si\s+no\s+se\s+puede\s+acceder)\b'),
    ('NOTES_VISUAL_JUSTIFICATION', r'\bexcepci[oó]n\s+visual\s+justificada\b'),
    ('NOTES_SOURCE_TRACE', r'\b(?:material\s+base\s*:|slides?\s+de\s+referencia\s*:|fuente\s+factual\s*:|mapeo\s+de\s+fuentes\s*:)'),
)


def extract_text(element: ET.Element) -> str:
    lines = []
    for p in element.iter(W + 'p'):
        chunks = []
        for piece in p.iter():
            if piece.tag == W + 't' and piece.text:
                chunks.append(piece.text)
            if piece.tag in (W + 'br', W + 'cr'):
                chunks.append('\n')
        if chunks:
            lines.append(''.join(chunks))
    return '\n'.join(lines).strip()


def count_images(element: ET.Element) -> int:
    return sum(1 for x in element.iter() if x.tag in (W + 'drawing', W + 'pict'))


def infer_type(meta: str) -> str:
    x = meta.casefold()
    if re.search(r'\bvideo\b|guion\s+de\s+video|videoplus|video\s+plus', x):
        return 'video'
    if re.search(r'\brise\b|lectura\s+interactiva|articulate|interactivo', x):
        return 'rise'
    if re.search(r'evaluaci[oó]n|cuestionario|quiz', x):
        return 'evaluacion'
    if re.search(r'descargable|one.pager|infograf[ií]a|pdf', x):
        return 'descargable'
    if re.search(r'\blectura\b|\btexto\b', x):
        return 'lectura'
    return 'otro'


def audit(docx: Path, resource_type: str = 'auto', max_words: int = 60,
          allow_sync_timecodes: bool = False) -> dict:
    errors = []
    warnings = []
    sections = []
    with zipfile.ZipFile(docx) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W + 'body')
    if body is None:
        return dict(file=str(docx), resource_type=resource_type, pass_delivery=False,
                    issues=[dict(code='WORD_BODY_MISSING')], warnings=[], sections=[])
    tables = body.findall(W + 'tbl')
    candidates = []
    metadata_fragments = []
    for tbl in tables:
        rows = tbl.findall(W + 'tr')
        for row_index, row in enumerate(rows):
            cells = row.findall(W + 'tc')
            if len(cells) != 2:
                continue
            headings = [extract_text(c).casefold() for c in cells]
            if 'notas de edici' in headings[0] and 'contenido del recurso' in headings[1]:
                candidates.append((rows, row_index))
                metadata_fragments.append(' '.join(extract_text(r) for r in rows[:row_index]))
    metadata = (' '.join(extract_text(t) for t in tables[:1])[:1800] if tables else '')
    # Combined templates put metadata and editorial rows in a SINGLE table.
    # Other templates use two. In either case, use only the pre-header text
    # for resource-type detection, not the narration that may mention videos.
    if metadata_fragments and metadata_fragments[0].strip():
        metadata = metadata_fragments[0]
    if tables:
        first_row = tables[0].find(W + 'tr')
        first_cells = first_row.findall(W + 'tc') if first_row is not None else []
        type_label = extract_text(first_cells[0]) if first_cells else ''
    else:
        type_label = ''
    kind = infer_type(type_label or metadata) if resource_type == 'auto' else resource_type
    if len(candidates) != 1:
        return dict(file=str(docx), resource_type=kind, pass_delivery=False,
                    issues=[dict(code='EDITORIAL_NOTES_TABLE_REQUIRED',
                                 detail=f'Se esperaba una tabla Notas de Edición / Contenido del Recurso; encontradas {len(candidates)}.')],
                    warnings=[], sections=[])
    candidate_rows, header_index = candidates[0]
    for idx, row in enumerate(candidate_rows[header_index+1:], 1):
        cells = row.findall(W + 'tc')
        if len(cells) != 2:
            errors.append(dict(code='EDITORIAL_NOTES_ROW_SHAPE', section=idx,
                               detail=f'Fila {idx}: {len(cells)} celdas; se requieren 2.'))
            continue
        left, right = cells
        notes, content = extract_text(left), extract_text(right)
        imgs_left, imgs_right = count_images(left), count_images(right)
        if not (notes or content or imgs_left or imgs_right):
            continue
        countable = URL.sub(' ', notes)  # a clickable stock URI is not instructional prose
        words = len(WORD.findall(countable))
        sections.append(dict(index=idx, notes_words=words, note_images=imgs_left,
                             content_images=imgs_right, section_title=notes.split('\n', 1)[0][:100]))
        if words > max_words:
            errors.append(dict(code='NOTES_EXCESSIVE_ALL_RESOURCES', section=idx,
                               detail=f'{words} palabras en la nota; máximo {max_words}. Acortar o separar la escena/bloque.'))
        elif words > 45:
            warnings.append(f'SECTION_{idx}_NOTES_LONG: {words} palabras; objetivo editorial 20-45.')
        if imgs_left:
            errors.append(dict(code='IMAGE_IN_EDITORIAL_NOTES', section=idx,
                               detail='Mover la imagen incrustada a Contenido del Recurso y dejar la instrucción en Notas de Edición.'))
        if not content and not imgs_right:
            errors.append(dict(code='EDITORIAL_CONTENT_EMPTY', section=idx,
                               detail='La fila carece de Contenido del Recurso.'))
        if kind != 'video' and not allow_sync_timecodes and TIMECODE.search(notes):
            errors.append(dict(code='UNJUSTIFIED_TIMECODES_NOT_VIDEO', section=idx,
                               detail='Intervalos de video en un recurso sin sincronización audiovisual aprobada.'))
        for code, regex in TECH_META:
            if re.search(regex, notes, re.I):
                errors.append(dict(code=code, section=idx,
                                   detail='La nota contiene QA, procedencia o contingencia interna en lugar de una instrucción de edición.'))
    return dict(file=str(docx), resource_type=kind, pass_delivery=not errors,
                issues=errors, warnings=warnings, sections=sections, max_words=max_words,
                note='Auditoría estructural; complementar con auditoría de Rise (si aplica), links, fidelidad y render visual.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Auditoría universal de Notas de Edición para todos los recursos Word')
    parser.add_argument('docx', type=Path)
    parser.add_argument('--resource-type', choices=['auto','video','rise','lectura','evaluacion','descargable','otro'], default='auto')
    parser.add_argument('--max-words', type=int, default=60,
                        help='Solo cambiar con aprobación editorial explícita registrada en QA externo.')
    parser.add_argument('--allow-sync-timecodes', action='store_true',
                        help='Para un recurso con audio/video sincronizado aunque no sea un guion de video.')
    parser.add_argument('--json-out', type=Path)
    parser.add_argument('--strict', action='store_true')
    options = parser.parse_args()
    result = audit(options.docx, options.resource_type, options.max_words, options.allow_sync_timecodes)
    result_text = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_text)
    if options.json_out:
        options.json_out.write_text(result_text + '\n', encoding='utf-8')
    if options.strict and not result['pass_delivery']:
        sys.exit(1)

if __name__ == '__main__':
    main()
