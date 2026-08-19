# Claude Skills Configuration

## Skills globales — leer en TODA tarea, sin excepción

Estas tres skills corren siempre en segundo plano. Léelas al inicio de cada conversación.

- `Claude_optimization/memory.md` — recupera memoria relevante antes de empezar, captura aprendizajes al terminar
- `Claude_optimization/pattern-learning.md` — detecta patrones buenos y malos durante la ejecución
- `Claude_optimization/execution-planning.md` — planifica antes de ejecutar tareas no triviales

**Operación:** silenciosa. No narrar la maquinaria al usuario.

---

## Arquitectura por defecto de proyectos nuevos — ICM

**Cuándo:** SIEMPRE que se inicie un proyecto, repositorio, o carpeta de trabajo nueva — en este repo o en cualquier otro repo/proyecto que trabajemos — o que se vaya a reestructurar una carpeta existente sin organización clara. No hace falta que el usuario lo pida.

**Skill:** `icm-architect/SKILL.md` (con `references/` y `assets/templates/`)

**Qué es:** Interpretable Context Methodology (ICM, Van Clief & McDermott) — usa la estructura de carpetas como arquitectura del agente: carpetas numeradas para secuencia, jerarquía para alcance de contexto, archivos markdown planos para estado. Reemplaza orquestación por código con convenciones de carpetas + un `CLAUDE.md`/`CONTEXT.md` de entrada.

**Acción por defecto:**
1. Al arrancar un proyecto nuevo o describir un flujo de trabajo repetible, aplicar el modo Build de `icm-architect` (elegir una de las seis formas: pipeline, umbrella, record library, knowledge bundle, context map, system map) sin preguntar si se debe usar ICM.
2. Al entrar a un repo/carpeta existente sin estructura clara, ofrecer o aplicar el modo Restructure (con el gate humano de "proponer antes de mover" que exige la skill).
3. Excepción: tareas realmente puntuales, de un solo uso, no repetibles — ahí no forzar una estructura de carpetas; decirlo brevemente en vez de escalar.
4. Esta skill convive con `project-structure-governor` (organización general del repo) y con `find-skills`/`workflow-orchestrator` como bootstrap base — ICM es el método concreto para el paso "crear o refinar la estructura".

---

## Skills específicas — leer SOLO cuando aplica

### Python / código complejo
**Cuándo:** el usuario pide fix, feature, refactor, nuevo módulo, o cualquier cambio que toque más de una función  
**Skill:** `Improve code/develope_code.md`

### Arquitectura de codebase
**Cuándo:** el usuario quiere mejorar estructura, reducir acoplamiento, hacer el código más testeable, o pide un "refactor grande"  
**Skills:** `Improve code/SKILL.md` + `Improve code/REFERENCE.md`

---

## Regla de oro

> Globales siempre. ICM por defecto en todo proyecto nuevo, sin preguntar. Específicas solo cuando el trigger aplica. Nunca narrar cuál skill se está leyendo a menos que el usuario lo pregunte.
