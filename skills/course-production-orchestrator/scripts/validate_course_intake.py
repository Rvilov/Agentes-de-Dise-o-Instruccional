#!/usr/bin/env python3
import sys
import json
from pathlib import Path

REQUIRED_FILES = [
    "00_ficha_maestra.md",
    "01_mapa_fuentes.md",
    "02_matriz_cobertura.md",
    "03_plan_recursos.md",
    "templates/resource_template.docx",
    "qa/source-catalog.json",
    "qa/course-coverage-contract.json",
    "qa/course-resource-index.json",
]

CRITICAL_FIELDS = [
    "Objetivo general",
    "Audiencia",
    "Plataforma final",
    "Tono",
    "Narrativa",
    "Nivel de adaptación",
    "Número de recursos",
]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: validate_course_intake.py <carpeta-proyecto>")
    root = Path(sys.argv[1]).expanduser().resolve()
    errors = []
    warnings = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Falta archivo obligatorio: {rel}")

    ficha_path = root / "00_ficha_maestra.md"
    if ficha_path.exists():
        text = ficha_path.read_text(encoding="utf-8")
        for field in CRITICAL_FIELDS:
            lines = [ln for ln in text.splitlines() if field.lower() in ln.lower()]
            if not lines:
                errors.append(f"Falta campo crítico en Ficha Maestra: {field}")
            elif any("PENDIENTE" in ln.upper() for ln in lines):
                errors.append(f"Campo crítico pendiente: {field}")
        if "PENDIENTE" in text.upper():
            warnings.append("La Ficha Maestra todavía contiene campos PENDIENTE no críticos.")

    source_path = root / "01_mapa_fuentes.md"
    if source_path.exists():
        text = source_path.read_text(encoding="utf-8")
        if "| F1 | PENDIENTE" in text:
            errors.append("El Mapa de Fuentes no tiene una fuente real registrada.")
        if "CONFLICTO ENTRE FUENTES" in text.upper():
            errors.append("Existe al menos un CONFLICTO ENTRE FUENTES sin resolver.")

    coverage_path = root / "02_matriz_cobertura.md"
    if coverage_path.exists():
        text = coverage_path.read_text(encoding="utf-8")
        if "| PENDIENTE |" in text:
            errors.append("La Matriz de Cobertura contiene filas sin definir.")
        if "CONFLICTO" in text.upper():
            errors.append("La Matriz de Cobertura contiene un tema bloqueado por conflicto.")

    plan_path = root / "03_plan_recursos.md"
    if plan_path.exists():
        text = plan_path.read_text(encoding="utf-8")
        if "PENDIENTE" in text.upper():
            errors.append("El Plan de Recursos aún contiene campos PENDIENTE.")

    # v1.4.1: check machine-readable source and topic registers before production.
    registry = root / 'qa/source-catalog.json'
    topics_path = root / 'qa/course-coverage-contract.json'
    index_path = root / 'qa/course-resource-index.json'
    if registry.exists() and topics_path.exists() and index_path.exists():
        try:
            sources = json.loads(registry.read_text(encoding='utf-8')).get('sources', [])
            topics = json.loads(topics_path.read_text(encoding='utf-8')).get('topics', [])
            res_index = json.loads(index_path.read_text(encoding='utf-8')).get('resources', [])
            if not sources:
                errors.append('CATALOGO DE FUENTES VACIO: registrar fuentes reales F1/F2')
            if not topics:
                errors.append('CONTRATO DE COBERTURA VACIO: identificar temas obligatorios T1/T2')
            if not res_index:
                warnings.append('INDICE DE RECURSOS SIN RUTAS DE SALIDA: completar antes de QA final')
            ids = [s.get('id') for s in sources if isinstance(s,dict)]
            if len(ids)!=len(set(ids)) or not all(ids):
                errors.append('IDs de fuente duplicados/vacios')
            if source_path.exists():
                compact_map=''.join(source_path.read_text(encoding='utf-8').split())
                if any(f"|{item.get('id')}|" not in compact_map for item in sources):
                    errors.append('Fuente registrada en JSON pero ausente en el Mapa de Fuentes')
            topic_ids = [t.get('id') for t in topics if isinstance(t,dict)]
            if len(topic_ids)!=len(set(topic_ids)) or not all(topic_ids):
                errors.append('IDs de tema duplicados/vacios')
            if coverage_path.exists():
                compact_coverage=''.join(coverage_path.read_text(encoding='utf-8').split())
                if any(f'|{tid}|' not in compact_coverage for tid in topic_ids):
                    errors.append('Tema registrado en JSON pero ausente en la Matriz de Cobertura')
            required=[t for t in topics if t.get('required') is True and t.get('usage')=='content']
            if not required:
                errors.append('No hay temas obligatorios mapeados a un recurso')
            for t in required:
                if t.get('source_id') not in ids or not t.get('resource_ids') or not t.get('locator') or not t.get('quote'):
                    errors.append('Tema obligatorio incompleto: '+str(t.get('id')))
            # Verify source files and snippets at the declared location (when available locally).
            shared = root / '.course-agent-suite/shared/scripts'
            if shared.is_dir():
                sys.path.insert(0,str(shared))
                from fidelity_gate import source_catalog, check_ref
                catalog={ 'sources':sources }
                local_errors=[]
                sources_by_id,segments,hashes=source_catalog(root,catalog,local_errors)
                errors.extend(local_errors)
                for t in required:
                    check_ref(t.get('source_id'),t.get('locator'),t.get('quote'),sources_by_id,segments,errors,'TEMA/'+str(t.get('id')))
            else:
                warnings.append('El validador de fuente local no esta instalado todavia')
        except (OSError,ValueError,TypeError,ImportError) as e:
            errors.append('ERROR LEYENDO CONTRATOS DE FIDELIDAD: '+str(e))

    print("VALIDACION DE INTAKE")
    for w in warnings:
        print(f"AVISO: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print("RESULTADO: NO LISTO PARA PRODUCCION")
        raise SystemExit(2)
    print("RESULTADO: LISTO PARA PRODUCCION")


if __name__ == "__main__":
    main()
