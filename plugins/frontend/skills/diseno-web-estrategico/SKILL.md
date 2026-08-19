---
name: diseno-web-estrategico
description: >
  Diseño web estratégico: síntesis de tres metodologías, con jerarquía de reglas —
  lo que coinciden los tres autores es obligatorio, lo que menciona uno solo es opcional
  con criterio. Úsala al construir un sitio o landing premium desde cero, mejorar un
  componente que "se ve genérico" o "se ve de IA", integrar assets visuales generados
  por IA, preparar un sitio para handoff a un cliente, o evaluar si un sitio alcanza
  nivel profesional antes de publicar. Also use for "build me a landing page", "make
  this look premium", "this looks AI-generated", "design review before launch". NO la
  uses para bugs de backend, scripts utilitarios, ni tareas sin componente visual.
---

# SKILL: Diseño Web Estratégico

Síntesis de 3 metodologías de diseño web con Claude Code. Regla de jerarquía:
lo que coinciden los 3 autores es **obligatorio**; lo que menciona uno solo es
**opcional con criterio**.

---

## ¿Cuándo usar esta skill?

Actívala cuando la tarea sea cualquiera de estas:

- Construir un sitio o landing desde cero que deba verse "premium" / de alto valor.
- Mejorar un componente o sección existente que "se ve genérico" o "se ve de IA".
- Integrar un asset visual (imagen o video) generado por IA en un sitio.
- Preparar un sitio para handoff a un cliente o equipo no técnico.
- Evaluar objetivamente si un sitio ya alcanza nivel profesional antes de publicar.

NO la actives para: bugs de lógica de backend, scripts utilitarios, o tareas
sin componente visual.

---

## Relación con otras capacidades

Añadido en la migración a este repo; el resto del cuerpo viene tal cual del original.

- **`artifact-design` (built-in) para un artefacto suelto.** Un póster, una página
  autónoma o un mockup que no vive en un codebase son suyos. Esta skill es para un sitio
  o componente **dentro de un proyecto**, con su design system y sus convenciones.
- **`dataviz` (built-in) para gráficas y dashboards.** No las rediseñes aquí.
- **`ui-ux-review` para revisar lo que ya existe.** Esta skill construye y mejora;
  aquella audita accesibilidad, jerarquía y comportamiento en anchos chicos.
- **El paso "usa una skill de diseño encima del default"** más abajo se resuelve con
  `artifact-design`. No instales otra ni la reimplementes.

**Precedencia con `preflight-planning`.** Si ya hubo un preflight, sus respuestas valen:
no repitas preguntas ya contestadas. El protocolo de siete preguntas de abajo **no bloquea
todo el trabajo** — bloquea solo lo que no se puede decidir sin la respuesta. Si falta algo
no crítico, elige el default obvio, dilo, y sigue. Preguntar siete cosas antes de mover un
dedo, cuando el planeador ya acordó el alcance, es fricción, no rigor.

---

## Principios de Oro (los 3 autores coinciden — obligatorios)

1. **Parte de referencias visuales, nunca de cero conceptual.**
   El default de Claude se ve genérico ("Claude slob"). Antes de generar,
   exige 3-5 referencias del usuario (screenshots o URLs) o extrae el blueprint
   de un sitio que le guste. El objetivo es igualar un estilo, no inventarlo.
   *Requiere referencia visual del usuario.*

2. **Usa una skill de diseño encima del default.**
   Los tres autores instalan una skill que estandariza spacing, tipografía y
   "look de lujo". Nunca confíes en el diseño de fábrica como entregable final.

3. **Genera assets visuales custom, no stock.**
   Imágenes y video deben generarse para esta marca específica. Que Claude
   escriba el prompt de generación a partir del contexto del proyecto, así el
   asset sale alineado a la estética en el primer intento.

4. **Itera por lenguaje natural hasta que quede bien.**
   El primer output nunca es el final. Refina en pasadas sucesivas describiendo
   qué está mal y qué esperabas. No te detengas en "aceptable".

5. **Publica en hosting real.**
   Un sitio en localhost no existe. El entregable termina desplegado y accesible
   por URL pública (Netlify / Vercel / Hostinger según el caso).

---

## Principios de Alta Prioridad (coinciden 2 de 3)

- **Pasada móvil dedicada.** "Responsive" no es lo mismo que "diseñado para móvil".
  Haz una pasada específica: qué se oculta, qué se reajusta, qué se redimensiona.
- **Optimiza peso y rendimiento.** Comprime imágenes/hero, extrae frames de video
  como JPEG optimizados ligados al scroll, precarga. La sensación de velocidad es
  parte de la percepción de calidad.
- **Genera variantes y escoge la mejor.** Produce 2-4 opciones del asset clave y
  selecciona, en vez de aceptar la primera.
- **Usa movimiento como diferenciador premium.** Scroll 3D o micro-interacciones
  de cursor sutiles elevan el sitio de "se ve caro" a "se siente caro".
- **Protege la arquitectura existente.** Nunca introduzcas algo (ej. React en un
  sitio estático) que rompa cómo funciona todo el proyecto, aunque te lo pidan
  literal. Adapta el efecto a la stack actual.

---

## Herramientas por enfoque

- **Enfoque Animación 3D (Doc 1 — sitios animados):**
  Video como asset central vía scroll-sequence frame-by-frame; máscara de
  gradiente para fundir el fondo del video con el del sitio; compresión agresiva
  de assets pesados. Útil cuando el diferenciador es el movimiento.
  *El resultado de scroll-sequence requiere referencia visual del usuario para validar.*

- **Enfoque Rúbrica de Calidad (Doc 2 — método de $10K):**
  Checklist de 8 elementos (punto de vista, tipografía, color, jerarquía,
  imágenes, movimiento, móvil, acabado invisible); dirigir por intención y no por
  especificación; editar en lotes; matar la fuente Inter; copy sensorial y sobrio.
  Útil para autoevaluar y subir el nivel general.

- **Enfoque CMS / Entregable (Doc 3 — sitios para clientes):**
  CMS con base de datos documental (MongoDB), version control con snapshots
  reversibles, guardian systems (el cliente edita copy/imágenes pero no rompe
  estructura), panel SEO, dashboard multi-sitio con acceso por contraseña.
  Útil cuando el sitio se entrega a alguien que lo editará después.

---

## Protocolo de preguntas antes de diseñar

Nunca propongas cambios sin responder esto primero. Pregunta y espera respuesta:

1. ¿Qué función cumple este componente o página? (objetivo de negocio)
2. ¿Quién es el usuario final?
3. ¿Qué sensación o emoción debe provocar? (dirígela por intención, no por specs)
4. Restricciones técnicas: ¿colores de marca, tipografías fijas, librerías o
   stack ya en uso? (define qué NO se puede romper)
5. ¿Qué es lo que más te molesta visualmente de lo que tienes ahora?
6. ¿Tienes referencias (3-5 screenshots/URLs) del estilo que buscas?
   *Si no las tiene, ese es el primer entregable a pedir antes de seguir.*
7. ¿El sitio lo va a editar después un cliente/no técnico? (decide si aplica
   enfoque CMS / guardian).

Tras las respuestas, presenta un **plan concreto**: qué cambiar, en qué orden y
por qué. No empieces a editar antes de tener el plan aprobado.

---

## Protocolo de mejora sin ruptura

Cómo intervenir un componente existente sin destruirlo:

**Paso 1 — Diagnóstico.** Recorre sección por sección y marca cada una como
fuerte / mixta / plana. Sé honesto. Pide screenshot si no puedes ver el render.
*Requiere referencia visual del usuario.*

**Paso 2 — Orden de ataque (alto impacto, bajo riesgo primero):**
1. Tipografía y jerarquía (cambio barato, gran efecto; matar Inter si aparece).
2. Color y espaciado (moderación = calidad).
3. Copy (sobrio, sensorial, sin adjetivos de relleno).
4. Assets visuales (imagen/video custom donde haya placeholders).
5. Movimiento / micro-interacciones, una por sección plana, sutil.
6. Optimización de peso y pasada móvil.

**Paso 3 — Edita en lote, no uno por uno.** Agrupa 4-5 correcciones por
solicitud: más coherente, menos idas y vueltas, menos tokens.

**Qué NUNCA tocar sin permiso explícito:**
- La estructura/arquitectura técnica (no metas React/dependencias nuevas en un
  sitio estático).
- Tipografías o colores de marca fijos declarados como restricción.
- Funcionalidad que ya opera (formularios, navegación, integraciones).
- En contexto CMS: la capa que el cliente no debe poder romper.

Regla: si un cambio podría alterar cómo *funciona* el sitio (no solo cómo se ve),
detente y confirma con el usuario antes.

---

## Criterios de decisión de diseño (cuando hay conflicto)

- **Coincidencia entre autores manda.** Si los 3 coinciden → es regla, hazlo.
  Si solo 1 lo menciona → es opcional, úsalo solo si encaja con el caso.
- **Intención sobre especificación.** Ante dos opciones, elige la que cumpla la
  *sensación* pedida, no la que tenga más features.
- **Moderación sobre abundancia.** Menos colores, menos efectos, más intencional.
  "Más caro" casi nunca significa "más recargado".
- **No ruptura sobre mejora marginal.** Si una mejora visual arriesga romper
  funcionalidad o arquitectura, descártala o adáptala a la stack actual.
- **Impacto/riesgo.** Prioriza siempre lo de alto impacto visual y bajo riesgo de
  ruptura. Deja lo riesgoso para el final y con confirmación.
- **Ante duda de algo que dependía de una imagen en el material fuente:** márcalo
  como *requiere referencia visual del usuario* y pídela antes de decidir.
