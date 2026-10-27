#!/usr/bin/env python3
"""Install/update the portable 11-skill suite without deleting course project data."""
import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

START='<!-- COURSE_AGENT_SUITE_START -->'
END='<!-- COURSE_AGENT_SUITE_END -->'


def update_file(path, block):
    old=path.read_text(encoding='utf-8') if path.exists() else ''
    if (START in old) != (END in old):
        raise ValueError(f'Marcadores incompletos en {path}; editar manualmente para no duplicar reglas')
    if START in old:
        a=old.index(START)
        b=old.index(END,a)+len(END)
        new=old[:a]+block.strip()+old[b:]
    else:
        new=(old.rstrip()+'\n\n'+block.strip()+'\n').lstrip()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(new,encoding='utf-8')


def staged_replace(src,target):
    incoming=target.parent/(target.name+'.course_suite_incoming')
    if incoming.exists():shutil.rmtree(incoming)
    try:
        shutil.copytree(src,incoming)
        if target.exists():shutil.rmtree(target)
        incoming.rename(target)
    finally:
        if incoming.exists():shutil.rmtree(incoming)


def main():
    ap=argparse.ArgumentParser(description='Instalar o actualizar Course Agent Suite en un proyecto existente')
    ap.add_argument('--platform',choices=['codex','claude'],required=True)
    ap.add_argument('--project-dir',required=True)
    ap.add_argument('--dry-run',action='store_true',help='Listar rutas afectadas sin hacer cambios')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    project=Path(args.project_dir).expanduser().resolve()
    dest=project/('.agents' if args.platform=='codex' else '.claude')/'skills'
    instructions=project/('AGENTS.md' if args.platform=='codex' else 'CLAUDE.md')
    shared_src=root/'shared'
    shared_dest=project/'.course-agent-suite'/'shared'
    skills=sorted(x for x in (root/'skills').iterdir() if x.is_dir() and (x/'SKILL.md').is_file())
    if len(skills)!=11:
        raise SystemExit(f'Se esperaban 11 skills, hay {len(skills)}; no actualizar parcialmente.')
    # Deep source integrity is checked once per installation, never sent to model context.
    sys.path.insert(0,str(shared_src/'scripts'))
    from validate_content_qa_source import audit as validate_full_style_guide
    style_check=validate_full_style_guide(shared_src)
    if style_check['status']!='OK':
        raise SystemExit('Content QA source corrupt or incomplete: '+str(style_check['errors']))
    affected=[dest/x.name for x in skills]+[shared_dest,instructions]
    print(f'Proyecto: {project}\nPlataforma: {args.platform}\nSkills: {len(skills)}')
    if args.dry_run:
        for p in affected:print(('REEMPLAZAR' if p.exists() else 'CREAR')+' '+str(p))
        print('Modo --dry-run: no se escribió ningún archivo.')
        return
    project.mkdir(parents=True,exist_ok=True)
    dest.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    backup=project/'.course-agent-suite'/'backups'/stamp
    has_backups=False
    for sk in skills:
        current=dest/sk.name
        if current.exists():
            backup_target=backup/'skills'/sk.name
            backup_target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(current,backup_target)
            has_backups=True
    if shared_dest.exists():
        backup_shared=backup/'shared'
        backup_shared.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(shared_dest,backup_shared)
        has_backups=True
    if instructions.exists():
        backup.mkdir(parents=True,exist_ok=True)
        shutil.copy2(instructions,backup/instructions.name)
        has_backups=True
    for sk in skills:staged_replace(sk,dest/sk.name)
    if shared_src.exists():
        shared_dest.parent.mkdir(parents=True,exist_ok=True)
        staged_replace(shared_src,shared_dest)
    update_file(instructions,(root/'global-instructions.fragment.md').read_text(encoding='utf-8'))
    print(f'Actualizadas {len(skills)} skills en {dest}')
    print(f'Referencias compartidas: {shared_dest}')
    print(f'Instrucciones: {instructions}')
    print(f'Backup: {backup}' if has_backups else 'Instalación nueva: no había contenidos anteriores para respaldo.')
    print('No se han alterado sources/, templates/, resources/, qa/ ni outputs/.')

if __name__=='__main__': main()
