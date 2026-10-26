#!/usr/bin/env python3
"""Normalize safe, structural aspects of the DI Word deliverable.

Never deletes source evidence or instructional text: source-citation leakage must be
reviewed and moved to an external traceability file by the producer.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Mm
from docx.oxml.ns import qn


def fit_table(table, usable_width):
    """Reflow a fixed-grid Word table while preserving original cell merges/styles."""
    grid = table._tbl.tblGrid
    cols = list(grid)
    if not cols:
        return
    old = [int(c.get(qn('w:w'))) for c in cols]
    total = sum(old)
    if total == 0:
        return
    target = round(usable_width / 635)  # EMUs -> twips
    scaled = [max(1, round(target * width / total)) for width in old]
    scaled[-1] += target - sum(scaled)
    # Word keeps table preferred width (<w:tblW>) separate from tblGrid.
    # Leaving the original landscape preferred width causes the entire table
    # to remain centered beyond both edges of a portrait page.
    tblw = table._tbl.tblPr.find(qn('w:tblW'))
    if tblw is not None:
        tblw.set(qn('w:w'), str(target))
        tblw.set(qn('w:type'), 'dxa')
    for col, tw in zip(cols, scaled):
        col.set(qn('w:w'), str(tw))
    for row in table._tbl.tr_lst:
        gridpos = 0
        for tc in row.tc_lst:
            tcPr = tc.get_or_add_tcPr()
            span = tcPr.find(qn('w:gridSpan'))
            cells = int(span.get(qn('w:val'))) if span is not None else 1
            tw = sum(scaled[gridpos:gridpos+cells])
            tcw = tcPr.find(qn('w:tcW'))
            if tcw is None:
                from docx.oxml import OxmlElement
                tcw = OxmlElement('w:tcW')
                tcPr.insert(0, tcw)
            tcw.set(qn('w:w'),str(tw))
            tcw.set(qn('w:type'),'dxa')
            gridpos += cells
    table.autofit = False


def normalize(source: Path, target: Path, orientation: str='portrait'):
    doc = Document(str(source))
    cleared_repeat_rows = 0
    for sect in doc.sections:
        if orientation == 'portrait':
            sect.orientation = WD_ORIENT.PORTRAIT
            sect.page_width, sect.page_height = Mm(210), Mm(297)
        elif orientation == 'landscape':
            sect.orientation = WD_ORIENT.LANDSCAPE
            sect.page_width, sect.page_height = Mm(297), Mm(210)
        else:
            raise ValueError('orientation must be portrait or landscape')
    for table in doc.tables:
        for row in table._tbl.tr_lst:
            trpr = row.trPr
            if trpr is not None:
                for h in list(trpr.findall(qn('w:tblHeader'))):
                    trpr.remove(h)
                    cleared_repeat_rows += 1
        s = doc.sections[0]
        fit_table(table, s.page_width - s.left_margin - s.right_margin)
    target.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(target))
    return {'source':str(source),'output':str(target),'orientation':orientation,'removed_tblHeader':cleared_repeat_rows,
            'source_references': 'not modified; must move outside Word separately'}


def main():
    p=argparse.ArgumentParser(description='Normalizar orientación y desactivar filas de cabecera repetidas sin borrar contenido.')
    p.add_argument('docx')
    p.add_argument('--output', required=True)
    p.add_argument('--orientation', choices=['portrait','landscape'], default='portrait')
    args=p.parse_args()
    print(json.dumps(normalize(Path(args.docx),Path(args.output),args.orientation),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
