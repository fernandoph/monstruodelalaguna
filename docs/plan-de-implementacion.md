# Plan de Implementacion

## Objetivo

Convertir el prototipo actual de `pygame` en un juego de plataformas completo para niñxs a partir de los 5 años, manteniendo la idea original de "El Monstruo de la Laguna" y cubriendo todo lo pedido en el `README`.

## Estado actual del proyecto

Hoy el repo tiene una base jugable, pero muy reducida:

- Un `loop` principal con `pygame`
- Un solo nivel embebido en codigo
- Colisiones basicas con tiles
- Movimiento horizontal, salto y gravedad
- Scroll horizontal simple
- Una sola animacion real del personaje: `idle`

Falta implementar casi todo lo que define el juego final:

- Agacharse
- Enemigos y obstaculos con comportamiento propio
- Recoleccion de peces
- Cambio de nivel
- Dificultad
- Vidas
- Pausa y reinicio
- Carteles de salida y llegada
- Baile final
- Arte de escenarios y UI
- Sonido y musica integrados

## Alcance funcional

El juego completo deberia incluir estos sistemas:

### 1. Personaje principal

- Moverse a izquierda y derecha
- Saltar
- Agacharse
- Tener animaciones de `idle`, `run`, `jump`, `fall`, `crouch`, `hurt` y `dance`
- Poder morir o reiniciar segun la dificultad

### 2. Escenario submarino

- Fondo submarino por capas
- Tiles visuales de piso, roca y plataforma
- Decoracion ambiental: algas, burbujas, ruinas, luces
- Cartel de inicio y cartel/meta de salida

### 3. Obstaculos y enemigos

- Pozos
- Piedras
- Hormigas acuaticas
- Pulpos con tentaculos animados
- Peces linterna que iluminan y se apagan al acercarse el jugador

### 4. Plataformas especiales

- Algas moviles que funcionen como plataformas
- Lanzadores de burbujas para atrapar enemigos

### 5. Coleccionables y progreso

- Peces coleccionables
- Requisito minimo de peces para terminar cada nivel
- Transicion entre 3 niveles
- Aumento gradual de dificultad entre niveles

### 6. Modos de dificultad

- Facil: no pierde vidas; reinicia el nivel
- Normal: pierde una vida; reinicia el nivel

### 7. UX y presentacion

- Pantalla inicial
- Seleccion de dificultad
- HUD con peces, vidas y nivel
- Pausa
- Reinicio manual
- Pantalla de fin de nivel
- Pantalla de victoria final

## Propuesta tecnica

### Estructura sugerida

Separar el juego en sistemas en lugar de seguir creciendo dentro de unos pocos archivos:

- `main.py` o mantener `monstruo.py` como entrada
- `settings.py` para configuraciones globales
- `game.py` para estados generales del juego
- `level.py` para carga y ejecucion de niveles
- `player.py` para el personaje
- `enemies/` para pulpos y hormigas
- `objects/` para peces, carteles, lanzadores, luces y plataformas
- `ui/` para HUD, menus y overlays
- `data/levels/` para mapas externos
- `graphics/` y `audio/` para assets

### Estados del juego

Conviene manejar una maquina de estados simple:

- `menu`
- `difficulty_select`
- `playing`
- `paused`
- `level_complete`
- `game_over`
- `victory`

### Estados del jugador

El personaje deberia tener estos estados logicos:

- `idle`
- `run`
- `jump`
- `fall`
- `crouch`
- `hurt`
- `dance`

Eso simplifica animaciones, colisiones y reglas especiales.

## Sistemas a implementar

### Movimiento y control

- Mejorar el input para que saltar no se dispare continuamente si se deja apretada la tecla
- Agregar `crouch` con ajuste de hitbox
- Definir suelo, aire e invulnerabilidad temporal si corresponde

### Colisiones y mundo

- Separar colisiones solidas de zonas de peligro
- Crear deteccion de pozo o "hazard"
- Permitir plataformas moviles que arrastren al jugador cuando esta arriba

### Enemigos

#### Hormiga acuatica

- Movimiento horizontal simple
- Patrulla entre dos puntos
- Hace daño al tocar al jugador
- Puede ser eliminada con burbujas

#### Pulpo

- Zona de amenaza
- Animacion de tentaculos
- Puede atrapar al jugador si entra en rango y no sale rapido
- Puede ser eliminado con burbujas

### Peces linterna

- Emiten luz o halo visual
- Si el jugador se acerca demasiado, bajan intensidad o se apagan
- No necesariamente hacen daño; son parte del ambiente interactivo

### Coleccionables

- Peces comunes como item recolectable
- Contador visible en HUD
- Meta de peces por nivel para habilitar la salida

### Lanzadores de burbujas

- Objeto interactivo del mapa
- Al activarlo, genera una burbuja o un efecto vertical
- Si la burbuja intercepta una hormiga o pulpo, el enemigo sube y desaparece

### Fin de nivel

- La salida solo deberia activarse cuando el jugador junto los peces requeridos
- Al completar nivel:
  - sonido o fanfarria
  - animacion de baile
  - pantalla breve de transicion

## Niveles

Se recomienda dejar de definir el nivel en una lista embebida y pasar a archivos de datos.

### Formato sugerido

Usar mapas CSV o matrices por capas:

- Capa de terreno
- Capa de decoracion
- Capa de entidades
- Capa de triggers

### Nivel 1

- Presenta controles y ritmo lento
- Pocos enemigos
- Pocos pozos
- Peces faciles de ver

### Nivel 2

- Introduce algas moviles y peces linterna
- Mezcla plataformas y enemigos
- Exige mas precision

### Nivel 3

- Usa todos los sistemas
- Mas verticalidad
- Mayor cantidad de peces requeridos
- Secuencia final y victoria

## Arte y assets necesarios

Para hacer "imagenes y todo", hace falta una lista clara de produccion visual.

### Personaje

- `idle`
- `run`
- `jump`
- `fall`
- `crouch`
- `hurt`
- `dance`

Idealmente cada estado con 4 a 8 frames.

### Enemigos

- Hormiga acuatica: caminar, recibir burbuja, desaparecer
- Pulpo: idle, tentaculos activos, capturar, recibir burbuja

### Objetos y entorno

- Tile de suelo
- Tile de roca
- Tile de plataforma
- Alga movil
- Cartel de inicio
- Cartel de salida
- Lanzador de burbujas
- Pez coleccionable
- Pez linterna
- Burbujas y particulas

### Fondos

- Fondo marino lejano
- Capa media con vegetacion o ruinas
- Capa cercana con detalles

### UI

- Icono de vidas
- Icono de pez
- Fondo de menu
- Botones o paneles
- Tipografia consistente

## Audio necesario

- Musica principal
- Efecto de salto
- Efecto de recolectar pez
- Efecto de daño
- Efecto de burbuja
- Efecto de completar nivel
- Sonido de menu y pausa

## Fases de trabajo

### Fase 1. Base tecnica

- Limpiar estructura del proyecto
- Externalizar configuraciones
- Definir sistema de niveles
- Preparar carga de assets robusta

### Fase 2. Movimiento y camara

- Completar estados del personaje
- Agregar agacharse
- Mejorar salto y colisiones
- Ajustar scroll y seguimiento de camara

### Fase 3. Mundo interactivo

- Peces coleccionables
- Pozos y hazards
- Carteles de inicio y salida
- Logica de fin de nivel

### Fase 4. Enemigos y plataformas

- Hormigas acuaticas
- Pulpos
- Algas moviles
- Lanzadores de burbujas

### Fase 5. UI y flujo de juego

- Menu inicial
- Seleccion de dificultad
- HUD
- Pausa
- Reinicio
- Game over y victory

### Fase 6. Arte y audio

- Reemplazar placeholders por assets finales
- Integrar musica y efectos
- Pulir feedback visual

### Fase 7. Balancing y QA

- Ajustar dificultad
- Verificar legibilidad para niñxs
- Probar colisiones y progresion
- Corregir bugs de borde

## Riesgos principales

- Que el arte se produzca sin una grilla comun y luego no encaje con el `tile_size`
- Que las mecanicas se agreguen sin estados claros y el codigo se vuelva fragil
- Que el mapa siga embebido en codigo y escale mal a 3 niveles
- Que la dificultad para un publico infantil quede mal calibrada

## Criterios de terminado

El proyecto puede considerarse alineado con el `README` cuando:

- Existen 3 niveles completos
- Se puede seleccionar dificultad
- El jugador junta peces para habilitar la salida
- Hay hormigas, pulpos, algas moviles y peces linterna funcionales
- Los lanzadores de burbujas eliminan enemigos
- Hay pausa, reinicio, vidas y progresion de nivel
- El monstruo baila al terminar
- El arte y la UI ya no son placeholders

## Orden recomendado de ejecucion

Si hubiera que hacerlo de forma pragmatica, este seria el orden:

1. Estructura del proyecto y sistema de niveles
2. Estados completos del jugador
3. Peces, salida y progresion
4. Dificultad, vidas y HUD
5. Enemigos y algas moviles
6. Lanzadores de burbujas
7. Menus y pantallas
8. Arte final, audio y pulido
