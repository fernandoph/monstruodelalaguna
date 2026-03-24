# Arte y Audio

## Objetivo

Definir el inventario minimo de produccion audiovisual para que el juego tenga identidad y no dependa de placeholders.

## Direccion visual sugerida

- Mundo submarino amable, colorido y legible
- Siluetas claras
- Contraste suficiente entre fondo, piso, enemigo y coleccionables
- Animaciones cortas pero expresivas
- UI simple y muy facil de leer

## Grilla y escala

- Mantener una grilla comun alineada al `tile_size`
- Definir desde el inicio el tamano logico del personaje
- Asegurar que todos los assets respeten proporciones similares

## Inventario de sprites

### Personaje principal

- `idle`
- `run`
- `jump`
- `fall`
- `crouch`
- `hurt`
- `dance`

## Inventario de enemigos

### Hormiga acuatica

- caminar
- dano o contacto
- atrapada por burbuja
- desaparicion

### Pulpo

- idle
- tentaculos activos
- captura o ataque
- atrapado por burbuja
- desaparicion

## Inventario de objetos

- pez coleccionable
- pez linterna
- alga movil
- lanzador de burbujas
- cartel de inicio
- cartel de salida
- roca
- tile de piso
- tile de plataforma
- burbujas
- brillo o halo de luz

## Fondos

- fondo lejano submarino
- capa media con vegetacion o ruinas
- capa cercana con detalles que no oculten gameplay

## UI

- pantalla inicial
- selector de dificultad
- icono de vidas
- icono de pez
- panel HUD
- overlay de pausa
- pantalla de game over
- pantalla de victoria

## Convencion de carpetas sugerida

- `graphics/player/idle/`
- `graphics/player/run/`
- `graphics/player/jump/`
- `graphics/player/fall/`
- `graphics/player/crouch/`
- `graphics/player/hurt/`
- `graphics/player/dance/`
- `graphics/enemies/ant/`
- `graphics/enemies/octopus/`
- `graphics/objects/fish/`
- `graphics/objects/lantern_fish/`
- `graphics/objects/bubble_launcher/`
- `graphics/tiles/`
- `graphics/backgrounds/`
- `graphics/ui/`

## Audio

### Musica

- tema de menu
- tema de gameplay
- fanfarria de nivel completado

### Efectos

- salto
- recolectar pez
- dano
- burbuja
- enemigo eliminado
- pausa
- reanudar
- victoria

## Criterios de calidad

- Cada asset debe comunicar su funcion
- El pez coleccionable debe distinguirse instantaneamente
- Los peligros deben ser legibles incluso sin texto
- La salida debe verse importante aun cuando este bloqueada
- El audio no debe saturar ni competir con la musica
