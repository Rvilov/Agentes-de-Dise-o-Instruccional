#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9áéíóúüñ]+", "-", value)
    return value.strip("-") or "curso"


def write_if_missing(path: Path, text: str):
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Crea el scaffold local de un curso instruccional.")
    ap.add_argument("--course-name", required=True)
    ap.add_argument("--out", required=True, help="Directorio padre donde crear el proyecto")
    ap.add_argument("--resource-count", type=int, default=0)
    ap.add_argument("--template", default=None, help="Plantilla DOCX alternativa")
    args = ap.parse_args()

    root = Path(args.out).expanduser().resolve() / slugify(args.course_name)
    root.mkdir(parents=True, exist_ok=True)
    for d in ["sources", "resources", "qa", "outputs", "templates"]:
        (root / d).mkdir(exist_ok=True)

    skill_root = Path(__file__).resolve().parent.parent
    template = Path(args.template).expanduser().resolve() if args.template else skill_root / "assets" / "resource_template.docx"
    if not template.exists():
        raise SystemExit(f"No se encontró la plantilla: {template}")
    dest_template = root / "templates" / "resource_template.docx"
    if not dest_template.exists():
        shutil.copy2(template, dest_template)

    ficha = f"""# Ficha Maestra del Curso\n\n- Nombre del curso: {args.course_name}\n- Cliente / marca: PENDIENTE\n- Objetivo general: PENDIENTE\n- Audiencia: PENDIENTE\n- Contexto de uso: PENDIENTE\n- Plataforma final: PENDIENTE\n- Tono: PENDIENTE\n- Persona lingüística: PENDIENTE\n- Narrativa: PENDIENTE\n- Personajes: PENDIENTE\n- Rol del participante: PENDIENTE\n- Nivel de adaptación (0-4): PENDIENTE\n- Duración total: PENDIENTE\n- Número de recursos: {args.resource_count if args.resource_count else 'PENDIENTE'}\n- Tipos de recursos: PENDIENTE\n- Duración por recurso: PENDIENTE\n- Nivel de interacción: PENDIENTE\n- Estrategia visual: PENDIENTE\n- Política de stock: PENDIENTE\n- Evaluación: PENDIENTE\n- Reglas de redacción: PENDIENTE\n- Entregable: Word A4 vertical, cabecera única y cuerpo de notas/contenido por recurso\n- Evidencia de fuentes y QA: exclusiva en qa/ (no en Word)\n- Corrección automática: errores objetivos y verificables\n- Escalamiento humano: decisiones pedagógicas, narrativas, conflictos y ambigüedades\n- Criterio de éxito: PENDIENTE\n"""
    write_if_missing(root / "00_ficha_maestra.md", ficha)

    source_map = """# Mapa de Fuentes\n\n| ID | Fuente | Tipo | Rol | Fecha/versión | Temas | Prioridad | Restricciones | Acceso | Estado |\n|---|---|---|---|---|---|---|---|---|---|\n| F1 | PENDIENTE | PENDIENTE | principal | PENDIENTE | PENDIENTE | 1 | PENDIENTE | local/adjunto/conectado | PENDIENTE |\n\n## Conflictos detectados\n\n- Ninguno identificado todavía.\n"""
    write_if_missing(root / "01_mapa_fuentes.md", source_map)

    coverage = """# Matriz de Cobertura\n\n| ID | Tema | Fuente ID | Ubicación | Recurso asignado | Tipo de uso | Obligatorio | Evaluable | Estado | Notas |\n|---|---|---|---|---|---|---|---|---|\n| PENDIENTE | F1 | PENDIENTE | PENDIENTE | Contenido | Sí | Sí | PENDIENTE | |\n"""
    write_if_missing(root / "02_matriz_cobertura.md", coverage)

    resource_plan = "# Plan de Recursos\n\n"
    if args.resource_count:
        for i in range(1, args.resource_count + 1):
            resource_plan += f"## R{i}\n- Tipo: PENDIENTE\n- Título: PENDIENTE\n- Objetivo: PENDIENTE\n- Fuentes asignadas: PENDIENTE\n- Duración: PENDIENTE\n\n"
    else:
        resource_plan += "- Estructura aprobada: PENDIENTE\n"
    write_if_missing(root / "03_plan_recursos.md", resource_plan)

    # Machine-readable evidence indexes start incomplete on purpose. Never invent source facts.
    defaults = {
        "source-catalog.json": {"schema_version":"1.4.1", "sources":[]},
        "course-coverage-contract.json": {"schema_version":"1.4.1", "topics":[]},
        "course-resource-index.json": {"schema_version":"1.4.1", "resources":[]},
    }
    for filename, data in defaults.items():
        f=root/"qa"/filename
        if not f.exists():
            f.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(root)


if __name__ == "__main__":
    main()
