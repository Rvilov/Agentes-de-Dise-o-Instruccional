#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

SKILL_NAME = "course-production-orchestrator"


def main():
    ap = argparse.ArgumentParser(description="Instala la skill en un proyecto Codex o Claude Code.")
    ap.add_argument("--platform", required=True, choices=["codex", "claude"])
    ap.add_argument("--project-dir", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    src = Path(__file__).resolve().parent.parent
    project = Path(args.project_dir).expanduser().resolve()
    base = project / (".agents/skills" if args.platform == "codex" else ".claude/skills")
    dst = base / SKILL_NAME
    base.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        if not args.force:
            raise SystemExit(f"Ya existe {dst}. Usa --force para reemplazarlo.")
        shutil.rmtree(dst)

    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "skill.zip")
    shutil.copytree(src, dst, ignore=ignore)
    print(dst)


if __name__ == "__main__":
    main()
