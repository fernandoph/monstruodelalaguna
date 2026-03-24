# Guia de Roadmaps

## Objetivo

Este documento explica como pensar, documentar y ordenar proyectos de este tipo para que el trabajo no dependa solo de intuicion o memoria. La idea es que funcione como referencia general para futuros proyectos, no solo para `El Monstruo de la Laguna`.

## Para que sirve un roadmap

Un roadmap no es una lista de deseos. Sirve para:

- convertir una idea en trabajo ejecutable
- separar vision de implementacion
- ordenar dependencias
- detectar riesgos temprano
- evitar que el proyecto crezca de forma caotica
- alinear producto, arte y programacion

Si un roadmap esta bien armado, deberia permitir responder:

- que problema se quiere resolver
- que version minima tiene sentido construir
- que falta para llegar ahi
- que tareas bloquean a otras
- que se puede postergar sin romper el objetivo

## Cuando conviene armarlo

Conviene documentar un roadmap cuando el proyecto tiene al menos una de estas caracteristicas:

- mas de un sistema relevante
- mas de una persona involucrada
- contenido progresivo o por niveles
- assets visuales o de audio que deben coordinarse
- riesgo de que el alcance crezca mientras se implementa

En proyectos chicos tambien sirve, porque evita improvisar arquitectura a medida que aparecen requisitos.

## Principios generales

### 1. Separar producto de implementacion

No conviene mezclar "que se quiere lograr" con "como se va a programar". Por eso la documentacion suele dividirse entre:

- vision y alcance
- flujo de uso o de juego
- arquitectura tecnica
- backlog y milestones

### 2. Ir de lo general a lo ejecutable

El orden natural no es arrancar por tareas. Primero se define:

- estado actual
- vision
- alcance
- sistemas principales
- arquitectura
- backlog
- milestones

El backlog sin contexto termina siendo una lista de trabajo sin criterio.

### 3. Documentar dependencias

No todas las tareas pesan lo mismo. Algunas habilitan muchas otras. Por ejemplo:

- una estructura de proyecto clara habilita implementar sistemas sin mezclar responsabilidades
- un formato de niveles habilita contenido escalable
- un loader de assets robusto evita errores repetidos durante toda la produccion

### 4. Definir entregas intermedias

Un roadmap util no apunta solo al resultado final. Tambien define cortes jugables o verificables.

Eso permite:

- probar antes
- ajustar alcance
- detectar problemas de base
- mostrar progreso real

### 5. Mantener el documento vivo

La documentacion inicial no deberia tratarse como texto sagrado. Hay que actualizarla cuando cambia:

- el alcance
- la prioridad
- el orden de trabajo
- el estado real del proyecto

## Estructura recomendada de documentacion

La estructura que arme en este `docs/` responde a una logica reusable.

### `estado-actual.md`

Sirve para separar fantasia de realidad. Antes de planear, hay que entender que existe de verdad.

Esto evita errores como:

- planear encima de features que no estan terminadas
- asumir que el proyecto esta mas avanzado de lo que realmente esta
- subestimar deuda tecnica

### `vision-y-alcance.md`

Define que producto se quiere construir y que cosas entran realmente en el alcance.

Sin esto, el proyecto suele desviarse por ideas nuevas o interpretaciones distintas de los requerimientos.

### `flujo-de-juego.md` o flujo de uso

Documenta la experiencia desde el punto de vista del usuario.

En videojuegos suele incluir:

- loop principal
- reglas
- controles
- estados del juego

En otros proyectos puede equivaler a:

- flujo de usuario
- journey
- estados del sistema

### `niveles-y-progresion.md` o contenido

Se usa cuando el proyecto tiene contenido escalonado, etapas, niveles o modulos funcionales que cambian con el tiempo.

Ayuda a pensar:

- ritmo
- introduccion gradual de complejidad
- reutilizacion de sistemas

### `arquitectura-propuesta.md`

Existe para bajar el problema a modulos, responsabilidades y datos.

No es una especificacion cerrada, pero si una guia para evitar que el codigo crezca sin forma.

### `arte-y-audio.md` o assets

Separa produccion tecnica de produccion de contenido.

Esto es importante porque muchas veces el cuello de botella no es solo el codigo, sino:

- que assets faltan
- que convenciones de tamanio o formato se necesitan
- que piezas visuales o sonoras bloquean una feature

### `backlog-priorizado.md`

Convierte la vision en trabajo.

El backlog deberia:

- tener prioridades reales
- mostrar dependencias
- separar base tecnica de features
- ser lo bastante concreto como para ejecutarse

### `milestones-de-trabajo.md`

Agrupa tareas en hitos verificables.

Esta capa es importante porque el backlog suele ser demasiado granular para explicar progreso. Los milestones permiten decir:

- que version intermedia existe
- que ya se puede probar
- que todavia falta para la siguiente entrega

### `plan-de-implementacion.md`

Funciona como resumen operativo. Es util para quienes necesitan una vista general antes de bajar al detalle.

## Por que esta estructura funciona

La estructura no esta separada por capricho. Responde a problemas tipicos de proyectos que empiezan chicos y despues crecen:

- el producto cambia mientras se desarrolla
- el codigo se mezcla con decisiones de contenido
- no queda claro que es prioritario
- el equipo pierde tiempo reinterpretando objetivos

Separar documentos reduce ese ruido porque cada archivo responde una pregunta distinta:

- que hay hoy
- que queremos construir
- como deberia sentirse o usarse
- como deberia organizarse tecnicamente
- que trabajo concreto hay que hacer
- en que orden conviene hacerlo

## Metodo general para armar un roadmap

### Paso 1. Levantar estado actual

Antes de planear, relevar:

- stack actual
- features existentes
- deuda tecnica
- assets disponibles
- riesgos visibles

### Paso 2. Definir vision y alcance

Escribir:

- publico objetivo
- objetivo del producto
- experiencia principal
- alcance minimo
- cosas fuera de alcance

### Paso 3. Identificar sistemas

Separar el proyecto en grandes bloques, por ejemplo:

- gameplay o logica principal
- datos y configuracion
- interfaz
- contenido
- assets
- testing o QA

### Paso 4. Diseñar arquitectura base

Definir:

- modulos
- responsabilidades
- formato de datos
- convenciones de carpetas
- puntos de extension

### Paso 5. Convertir sistemas en backlog

Cada sistema se baja a tareas concretas con prioridad.

La prioridad deberia responder a estas preguntas:

- desbloquea otras tareas
- crea valor jugable o usable
- reduce riesgo tecnico
- puede probarse

### Paso 6. Agrupar en milestones

No conviene entregar solo tareas sueltas. Conviene agruparlas en cortes con sentido:

- fundacion tecnica
- core funcional
- features diferenciales
- contenido completo
- presentacion final

### Paso 7. Revisar y ajustar

Cada milestone cerrado deberia disparar una revision:

- que aprendimos
- que resulto mas costoso de lo esperado
- que alcance conviene reducir o mover
- que documento quedo desactualizado

## Reglas practicas para priorizar

- primero resolver lo que desbloquea otras capas
- despues cerrar el loop minimo usable o jugable
- despues agregar variedad y profundidad
- al final pulir presentacion, audio y detalle

Una regla simple:

- sin base tecnica no hay velocidad
- sin loop minimo no hay producto
- sin contenido no hay progresion
- sin pulido no hay presentacion final

## Anti patrones comunes

- arrancar por detalles visuales antes de cerrar reglas base
- hacer todo en un solo documento
- mezclar ideas futuras con trabajo comprometido
- definir milestones demasiado abstractos
- no distinguir deuda tecnica de feature nueva
- no revisar el roadmap cuando cambia el proyecto

## Plantilla reusable para proyectos futuros

Una estructura simple y general seria:

1. `README.md` dentro de `docs/` como indice
2. `estado-actual.md`
3. `vision-y-alcance.md`
4. `flujo-de-uso.md` o `flujo-de-juego.md`
5. `arquitectura-propuesta.md`
6. `contenido-o-modulos.md` si aplica
7. `assets-o-integraciones.md` si aplica
8. `backlog-priorizado.md`
9. `milestones-de-trabajo.md`
10. `plan-de-implementacion.md`

No todos los proyectos necesitan todos los documentos, pero esta base cubre bien productos con varias capas de trabajo.

## Como adaptar esta metodologia

### Proyecto chico

- menos documentos
- backlog corto
- milestones mas compactos
- una sola persona puede mantener todo

### Proyecto mediano

- separar producto, tecnica y contenido
- mantener backlog y milestones por separado
- revisar dependencias con frecuencia

### Proyecto grande

- separar por equipos o dominios
- versionar decisiones tecnicas relevantes
- llevar planning y documentacion de release con mas rigor

## Criterio de calidad para un roadmap

Un roadmap esta bien armado cuando:

- se entiende rapido
- baja del objetivo a tareas concretas
- muestra dependencias
- permite saber que version existe en cada etapa
- se puede mantener sin demasiado costo

## Cierre

La estructura que use en este proyecto busca exactamente eso: transformar una idea general en una secuencia de decisiones y entregas que se puedan ejecutar, revisar y reutilizar. Si esta base se mantiene actualizada, sirve no solo para este juego sino como plantilla para futuros proyectos con alcance similar.
