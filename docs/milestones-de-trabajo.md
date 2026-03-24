# Milestones de Trabajo

## Objetivo

Agrupar el backlog en hitos de entrega concretos, con una secuencia que permita construir el juego sin mezclar demasiadas decisiones al mismo tiempo.

## Como leer este documento

- Cada milestone representa una entrega jugable o una base que habilita la siguiente.
- Los milestones estan pensados para ejecutarse en orden.
- Cada uno tiene alcance, entregables, dependencias y criterio de salida.

## Milestone 0. Fundacion tecnica

### Objetivo

Dejar el proyecto listo para crecer sin que cada mecanica nueva aumente la deuda tecnica.

### Alcance

- Reorganizar estructura del proyecto
- Separar configuracion, entrada y logica de juego
- Definir convenciones de assets
- Externalizar niveles
- Preparar carga robusta de datos y recursos

### Tareas del backlog involucradas

- `BLK-001`
- `BLK-002`
- `BLK-003`

### Entregables

- Estructura de carpetas estable
- Loader de niveles funcional
- Primer nivel cargado desde datos externos
- Sistema de carga de assets centralizado
- `.gitignore` y base de proyecto saneada

### Criterio de salida

- El juego sigue arrancando
- El nivel ya no esta embebido en una lista de strings
- Agregar un nuevo nivel no requiere tocar el loop principal
- Los assets faltantes producen errores claros o placeholders controlados

## Milestone 1. Core jugable

### Objetivo

Cerrar el loop minimo de juego para que ya exista una experiencia completa, aunque todavia simple.

### Alcance

- Completar estados basicos del jugador
- Ajustar fisica e input
- Agregar HUD minimo
- Implementar peces coleccionables
- Implementar salida y progresion
- Implementar dificultad y vidas
- Implementar pausa y reinicio

### Tareas del backlog involucradas

- `BLK-004`
- `BLK-005`
- `BLK-006`
- `MEC-001`
- `MEC-002`
- `MEC-003`
- `MEC-004`
- `MEC-005`
- `CNT-001`

### Entregables

- Personaje con `idle`, `run`, `jump`, `fall`, `crouch`, `hurt` y `dance`
- Nivel 1 completo y terminable
- HUD con peces, vidas o estado de dificultad
- Salida bloqueada hasta cumplir meta de peces
- Pausa y reinicio funcionales
- Diferencia real entre modo facil y normal

### Criterio de salida

- Se puede jugar del inicio al fin del nivel 1
- El jugador entiende cuantos peces faltan
- Caer o recibir dano reinicia segun las reglas del modo elegido
- El fin de nivel activa baile y transicion

## Milestone 2. Mundo interactivo

### Objetivo

Agregar amenazas y objetos especiales para que el juego deje de ser solo un platformer basico.

### Alcance

- Implementar hormigas acuaticas
- Implementar pulpos
- Implementar algas moviles
- Implementar lanzadores de burbujas
- Implementar peces linterna reactivos

### Tareas del backlog involucradas

- `ENM-001`
- `ENM-002`
- `OBJ-001`
- `OBJ-002`
- `OBJ-003`

### Entregables

- Enemigos patrullando o atacando segun su logica
- Plataformas moviles funcionales
- Mecanica de neutralizacion con burbujas
- Elementos de iluminacion reactiva

### Criterio de salida

- Los enemigos agregan desafio legible
- Las burbujas interactuan con enemigos de forma consistente
- Las algas moviles pueden usarse para progresar
- Los peces linterna aportan feedback ambiental reconocible

## Milestone 3. Contenido completo

### Objetivo

Construir los tres niveles y cerrar la progresion completa del juego.

### Alcance

- Construir nivel 2
- Construir nivel 3
- Ajustar curva de dificultad
- Integrar secuencia de victoria

### Tareas del backlog involucradas

- `CNT-002`
- `CNT-003`

### Entregables

- Tres niveles jugables
- Curva de progresion clara
- Uso combinado de mecanicas
- Pantalla o secuencia de victoria final

### Criterio de salida

- Los tres niveles pueden completarse en una sola sesion
- Cada nivel introduce o combina mecanicas con sentido
- El juego termina de forma clara al cerrar el nivel 3

## Milestone 4. Presentacion final

### Objetivo

Reemplazar placeholders y llevar la experiencia a una version presentable.

### Alcance

- Menu inicial
- Selector de dificultad
- Pantallas de estado
- Reemplazo de placeholders visuales
- Integracion de musica y efectos
- Pulido de feedback

### Tareas del backlog involucradas

- `UX-001`
- `UX-002`
- `UX-003`
- `ART-001`
- `AUD-001`
- `QA-001`

### Entregables

- Menu completo
- UI final
- Assets finales o consistentes
- Audio integrado
- Ajustes de balance y testing basico

### Criterio de salida

- El juego se siente cohesivo visual y sonoramente
- La navegacion entre pantallas es clara
- El contenido tiene un nivel aceptable de pulido

## Dependencias entre milestones

- `Milestone 1` depende de `Milestone 0`
- `Milestone 2` depende de `Milestone 1`
- `Milestone 3` depende de `Milestone 2`
- `Milestone 4` puede avanzar en paralelo en arte y audio, pero necesita el core jugable para cerrar bien

## Primer release recomendable

El primer release interno razonable es al cerrar `Milestone 1`.

Ese corte ya deberia permitir:

- abrir el juego
- elegir dificultad
- jugar un nivel completo
- juntar peces
- llegar a la salida
- perder o reiniciar segun reglas

## Segundo release recomendable

El segundo release interno razonable es al cerrar `Milestone 3`.

Ese corte ya deberia permitir:

- jugar los 3 niveles
- usar mecanicas especiales
- enfrentar enemigos
- ver la progresion completa del juego

## Release final

El release final coincide con el cierre de `Milestone 4`.

En ese punto el proyecto deberia estar listo para mostrarse como juego terminado dentro del alcance actual del `README`.
