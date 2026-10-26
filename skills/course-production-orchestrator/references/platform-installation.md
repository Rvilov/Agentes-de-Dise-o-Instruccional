# Instalación portable

La lógica central vive en `SKILL.md`, `references/`, `scripts/` y `assets/`. No duplicar reglas por plataforma.

## Codex

Instalar en el proyecto:

`.agents/skills/course-production-orchestrator/`

Ejemplo:

```bash
python scripts/install.py --platform codex --project-dir /ruta/al/proyecto
```

## Claude Code

Instalar en el proyecto:

`.claude/skills/course-production-orchestrator/`

Ejemplo:

```bash
python scripts/install.py --platform claude --project-dir /ruta/al/proyecto
```

## Regla de portabilidad

- No depender de rutas privadas de ChatGPT.
- Resolver assets y referencias de forma relativa al directorio de la skill.
- Mantener scripts en Python estándar cuando sea posible.
- Si una plataforma carece de una integración opcional, degradar con claridad y solicitar el archivo local en vez de inventar contenido.
