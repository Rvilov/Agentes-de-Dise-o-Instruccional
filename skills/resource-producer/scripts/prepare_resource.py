#!/usr/bin/env python3
"""Create the editable DI Word plus its SEPARATE internal QA sidecars."""
import argparse
import json
import shutil
from pathlib import Path
from normalize_resource_docx import normalize


def main():
    ap=argparse.ArgumentParser(description='Preparar recurso Word limpio y trazabilidad externa')
    ap.add_argument('--resource-id',required=True)
    ap.add_argument('--title',required=True)
    ap.add_argument('--output-dir',required=True)
    ap.add_argument('--qa-dir',default=None,help='Directorio de control; por defecto carpeta hermana qa/')
    ap.add_argument('--orientation',choices=['portrait','landscape'],default='portrait',help='A4 vertical por defecto')
    ap.add_argument('--template',default=str(Path(__file__).resolve().parents[1]/'assets'/'resource_template.docx'))
    args=ap.parse_args()
    outdir=Path(args.output_dir).expanduser().resolve()
    outdir.mkdir(parents=True,exist_ok=True)
    qa_dir=Path(args.qa_dir).expanduser().resolve() if args.qa_dir else outdir.parent/'qa'
    qa_dir.mkdir(parents=True,exist_ok=True)
    resource_id=args.resource_id.strip()
    safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in args.title).strip('_')[:80]
    docx=outdir/f'{resource_id}_{safe}.docx'
    template=Path(args.template).expanduser().resolve()
    if not template.is_file():
        raise SystemExit(f'Plantilla no encontrada: {template}')
    shutil.copy2(template,docx)
    # Adjust the historically landscape template to the current portrait delivery policy.
    normalize(docx,docx,args.orientation)
    manifest=qa_dir/f'{resource_id}.manifest.json'
    if not manifest.exists():
        manifest.write_text(json.dumps({
            'resource_id':resource_id,'title':args.title,'type':'','objective':'',
            'source_refs':[],'narrative':{},'visuals':[],'interactions':[],
            'visual_plan':{'resource_type':'','blocks':[],'video_scenes':[]},
            'evaluation_key':[],'output_docx':str(docx),
            'word_orientation':args.orientation,
            'visible_source_citations':False,
            'external_traceability_file':str(qa_dir/f'{resource_id}_trazabilidad.md')
        },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    trace=qa_dir/f'{resource_id}_trazabilidad.md'
    if not trace.exists():
        trace.write_text(
            f'# Trazabilidad interna {resource_id} — no copiar al Word\n\n'
            '| Bloque del recurso | Fuente ID | Ubicación en fuente | Tipo de uso | Validación | Observaciones |\n'
            '|---|---|---|---|---|---|\n'
            '<!-- Añadir una fila por bloque factual (ej.: R1-B1 | F1 | slide 3). No dejar esta tabla vacía antes de QA final. -->\n',
            encoding='utf-8')
    print(docx)
    print(manifest)
    print(trace)


if __name__=='__main__':main()
