# Claude Skills Configuration

## Skills globales — leer en TODA tarea, sin excepción

Estas tres skills corren siempre en segundo plano. Léelas al inicio de cada conversación.

- `Claude_optimization/memory.md` — recupera memoria relevante antes de empezar, captura aprendizajes al terminar
- `Claude_optimization/pattern-learning.md` — detecta patrones buenos y malos durante la ejecución
- `Claude_optimization/execution-planning.md` — planifica antes de ejecutar tareas no triviales

**Operación:** silenciosa. No narrar la maquinaria al usuario.

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

> Globales siempre. Específicas solo cuando el trigger aplica. Nunca narrar cuál skill se está leyendo a menos que el usuario lo pregunte.
