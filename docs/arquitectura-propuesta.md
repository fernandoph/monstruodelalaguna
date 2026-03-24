# Arquitectura Propuesta

## Objetivo

Definir una estructura de codigo que permita agregar mecanicas sin volver fragil el proyecto.

## Principios

- Separar logica de juego, datos de nivel y assets
- Reducir el acoplamiento entre entidades
- Hacer que los niveles sean datos, no codigo duro
- Mantener responsabilidades claras por modulo

## Estructura sugerida

- `monstruo.py`: punto de entrada
- `settings.py`: constantes globales
- `game.py`: estado global, bucle principal y cambio de pantallas
- `level.py`: carga de un nivel y coordinacion de entidades
- `player.py`: movimiento, estado y animacion del jugador
- `camera.py`: seguimiento y limites del mundo
- `ui.py` o `ui/`: HUD, menus y overlays
- `support.py`: helpers de carga de archivos y assets
- `entities/`: base comun para sprites y entidades dinamicas
- `enemies/`: hormiga y pulpo
- `objects/`: peces, salida, carteles, algas, lanzadores y luces
- `data/levels/`: mapas y metadatos de niveles
- `graphics/`: sprites, fondos y UI
- `audio/`: musica y efectos

## Responsabilidades clave

### `game.py`

- Cambiar entre `menu`, `playing`, `paused`, `level_complete`, `game_over` y `victory`
- Mantener dificultad elegida
- Llevar vidas y progreso general

### `level.py`

- Cargar capas del nivel
- Instanciar entidades
- Actualizar mundo
- Resolver colisiones de alto nivel
- Detectar fin de nivel

### `player.py`

- Resolver input
- Aplicar fisica
- Manejar estados del personaje
- Exponer hitboxes y eventos de dano o coleccion

### `enemies/`

- Encapsular IA minima
- Definir dano
- Reaccionar a burbujas

### `objects/`

- Mantener comportamiento de plataformas, peces, salida y elementos de escenario interactivo

## Formato de niveles

Se recomienda que cada nivel tenga un archivo de metadatos y una o varias capas.

### Capas sugeridas

- `terrain`
- `hazards`
- `collectibles`
- `enemies`
- `decor`
- `triggers`

### Metadatos sugeridos

- `level_id`
- `name`
- `background`
- `fish_goal`
- `spawn`
- `exit`
- `time_limit` opcional

## Modelo de entidades

Conviene usar una clase base para entidades dinamicas con:

- `rect`
- `hitbox`
- `state`
- `velocity`
- `update()`
- `draw()` cuando haga falta comportamiento especial

## Colisiones

Separar por tipo:

- Solidas
- Daninas
- Interactivas
- Coleccionables
- Triggers de nivel

Esa separacion evita condicionales mezclados en una sola lista de tiles.

## Assets y carga

La carga de assets deberia ser robusta ante faltantes:

- Validar carpetas
- Dar errores claros
- Permitir placeholders temporales
- Centralizar rutas

## Testing recomendado

Aunque sea un juego chico, conviene validar:

- Carga de assets
- Carga de niveles
- Reglas de progresion
- No regressions en fisica basica

## Decision tecnica importante

Antes de agregar contenido, conviene elegir una de estas dos estrategias:

- Evolucion controlada del codigo actual
- Reorganizacion temprana y luego implementacion de mecanicas

La segunda opcion es mas lenta al principio, pero reduce deuda tecnica fuerte en las fases medias.
