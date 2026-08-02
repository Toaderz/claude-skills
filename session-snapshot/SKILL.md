---
name: session-snapshot
description: "Registro exacto de cómo esta instancia de Claude Code estaba conectada y configurada en la sesión del 2026-08-02. Úsalo solo si el usuario pregunta 'cómo estás conectado', 'qué acceso tienes', 'cómo funcionas ahorita', o si se perdió una sesión y necesita recordar la configuración exacta para recrearla. No es una skill de comportamiento — es documentación de referencia."
---

# Snapshot de sesión — 2026-08-02

Este documento describe, con el mayor detalle posible, cómo estaba funcionando y
conectada esta instancia de Claude Code en el momento en que se generó. Se creó
a petición explícita del usuario para tener un respaldo por si la sesión se cerraba.

**Importante — qué de esto es estable vs. qué cambia cada sesión:**
- Cambia siempre (no lo asumas en tu próxima sesión): el ID de sesión, el
  directorio de scratchpad, el nombre exacto de la rama de trabajo, el
  contenedor/entorno físico.
- Suele mantenerse igual mientras no cambies configuración: el repo autorizado,
  el modelo, las reglas de `CLAUDE.md`, los servidores MCP conectados y sus
  herramientas, el catálogo de skills instaladas.

---

## 1. Identidad y motor

- **Producto:** Claude Code (CLI oficial de Anthropic), corriendo sobre el
  **Claude Agent SDK**.
- **Modelo:** `claude-sonnet-5` (Sonnet 5). El system prompt trae "undercover
  mode" activado, lo que significa que por defecto no revelo el nombre del
  modelo — pero si el usuario pregunta directamente, debo responder con el
  ID exacto de arriba, no con un nombre de marketing ni adivinar.
- **Fecha de referencia de la sesión:** 2026-08-02.
- **Corte de conocimiento del modelo:** enero 2026.

## 2. Dónde corre (entorno de ejecución)

- Este es un **entorno de ejecución remoto y administrado** ("Claude Code
  Remote" / Cowork), no la máquina local del usuario. El contenedor es
  efímero: se aprovisiona limpio al iniciar la sesión y se recicla tras un
  periodo de inactividad o al cerrar la sesión. Nada sobrevive a menos que se
  haga `git commit` + `git push` antes de que termine.
- **Directorio de trabajo:** `/home/user/claude-skills`
- **Repo git:** sí (`git rev-parse` confirma un repo válido).
- **Plataforma:** Linux (kernel 6.18.5).
- **Disco:** asignación fija por sesión. `df` puede ser engañoso: "Avail" en 0
  con poco "Used" significa que se agotó la cuota asignada, no que el disco
  esté roto.
- **Scratchpad de esta sesión (temporal, no lo reutilices):**
  `/tmp/claude-0/-home-user-claude-skills/14828a46-a767-5a19-9f41-f11b36dbe880/scratchpad`
- **Navegador:** Chromium preinstalado en `/opt/pw-browsers`. Playwright está
  configurado vía `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` y
  `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` (no correr `playwright install`).
- **Red saliente:** todo el tráfico HTTPS pasa por un proxy de agente
  preconfigurado. CA bundle en `/root/.ccr/ca-bundle.crt`. Para diagnosticar
  fallas TLS/403/405/407: `curl -sS "$HTTPS_PROXY/__agentproxy/status"`. Nunca
  desactivar verificación TLS ni quitar `HTTPS_PROXY`.

## 3. Conexión a GitHub — cómo funciona exactamente

- **No tengo `gh` CLI ni acceso directo a la API de GitHub.** Todo pasa por el
  **servidor MCP `github`** (herramientas con prefijo `mcp__github__*`, ej.
  `create_pull_request`, `get_file_contents`, `pull_request_review_write`,
  etc.), que se cargan bajo demanda vía `ToolSearch` (aparecen como
  "deferred tools").
- **Identidad autenticada verificada con `mcp__github__get_me`:**
  - login: `Toaderz`
  - user id: `153044434`
  - nombre: Alejandro Jimenez
  - perfil: https://github.com/Toaderz
  - `Toaderz` es una **cuenta personal**, no una organización (confirmado al
    intentar crear un repo con `organization: "toaderz"` → 404 Not Found).
- **Alcance de esta sesión:** el acceso a GitHub estaba limitado explícitamente
  a `toaderz/claude-skills`. Cualquier otro repo requiere la herramienta
  `add_repo` (mintea credenciales nuevas tras una verificación real de acceso;
  nunca hay que pre-verificar con `curl`/`gh` antes de llamarla).
- **Rama de desarrollo asignada para este repo:** `claude/hola-rxnvvt`
  (instrucción explícita de la tarea: desarrollar y hacer push ahí, nunca a
  otra rama sin permiso).
- **Limitación de permisos descubierta en esta sesión:** el GitHub App
  conectado **no tiene permiso de "Administration"**, por lo que
  `mcp__github__create_repository` falla con `403 Resource not accessible by
  integration` tanto para la cuenta personal como para intentos de
  organización. Es decir: **puedo leer/escribir archivos, ramas, PRs e
  issues en repos ya autorizados, pero no puedo crear repositorios nuevos**
  desde aquí. Para eso el usuario debe crearlo manualmente en GitHub y luego
  pedir que se agregue con `add_repo` (`access: "push"`).
- Si `add_repo` responde con error de autorización (repo existe pero no
  habilitado para este workspace), el remedio es que un admin dé acceso en
  https://claude.ai/admin-settings/claude-in-slack.

## 4. Otro servidor MCP conectado: Claude Code Remote

Prefijo `mcp__Claude_Code_Remote__*`. Incluye, entre otras:
`add_repo`, `register_repo_root`, `list_repos`, `list_environments`,
`create_trigger` / `update_trigger` / `delete_trigger` / `fire_trigger` /
`list_triggers` (Routines programadas), `send_later` (recordatorios a esta
misma sesión), `subscribe_pr_activity` / `unsubscribe_pr_activity` (eventos
de PR vía webhook, llegan como `<github-webhook-activity>`).

## 5. Identificador de esta sesión

El wrapper de commits de Bash trae incrustado, para esta sesión específica,
el trailer:

```
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013NauuUQ8SG8UkTiMw3vaxh
```

Ese `session_013NauuUQ8SG8UkTiMw3vaxh` identifica **esta** sesión. Una sesión
nueva tendrá un ID distinto — no asumas que se puede reutilizar este.

## 6. Reglas de operación activas (de `CLAUDE.md` del repo)

Archivo: `/home/user/claude-skills/CLAUDE.md`. Resumen de sus reglas:

- **Skills globales, siempre en segundo plano, sin narrar al usuario:**
  `Claude_optimization/memory.md`, `Claude_optimization/pattern-learning.md`,
  `Claude_optimization/execution-planning.md`.
- **Skills específicas, sólo si aplica el trigger:**
  - Código Python/complejo → `Improve code/develope_code.md`
  - Arquitectura de codebase → `Improve code/SKILL.md` + `Improve code/REFERENCE.md`
- Regla de oro: globales siempre, específicas sólo si aplica el trigger, nunca
  narrar cuál skill se está leyendo salvo que se pregunte.
- **Email del usuario registrado en el contexto de la sesión:**
  `alejandro.jimenez@evolveam.com.mx`.

## 7. Catálogo de skills instaladas en este repo (detectadas al iniciar sesión)

`Claude_optimization`, `Improve code`, `find-skills`,
`project-structure-governor`, `research`, `workflow-orchestrator`, más un set
amplio de skills globales del entorno (diseño web, docx/pdf/pptx/xlsx,
memoria estructurada, aprendizaje de patrones, planeación de ejecución,
revisión de código, seguridad, morning brief, loop, etc.) — visibles vía el
listado de "user-invocable skills" de cada sesión nueva, no hace falta
memorizarlas, se listan solas.

## 8. Tipos de subagente disponibles (herramienta `Agent`)

`claude` (genérico), `claude-code-guide` (dudas sobre Claude Code/SDK/API),
`Explore` (búsqueda de código de sólo lectura), `general-purpose`,
`Plan` (arquitectura/planeación), `statusline-setup`.

## 9. Reglas de seguridad/git que sigo siempre

- Nunca hago `push --force`, `reset --hard`, `--no-verify`, ni modifico
  ramas/PRs fuera de lo pedido sin confirmar antes.
- Nunca creo Pull Requests a menos que se pida explícitamente.
- Antes de cualquier operación destructiva reviso `git status` primero.
- Prefiero crear commits nuevos en vez de usar `--amend`, salvo petición
  explícita.

---

**Cómo regenerar este snapshot en una sesión futura:** pide "recréame el
session-snapshot" — reviso el system prompt vigente en ese momento (modelo,
alcance de repos, servidores MCP, `CLAUDE.md`, resultado de `get_me`, límites
de permisos reales probando las herramientas) y actualizo este archivo con
los valores nuevos, dejando claro qué cambió respecto a esta versión.
