# Estado Actual

## Resumen

El proyecto ya no es solo un prototipo tecnico. Hoy existe una progresion completa de 3 niveles jugables con menu, HUD, dificultad, recoleccion de peces, salida bloqueada, pausa, reinicio y amenazas especiales integradas al recorrido.

## Estado del roadmap

- `Milestone 0`: cerrado
- `Milestone 1`: cerrado
- `Milestone 2`: cerrado en una primera version jugable y legible
- `Milestone 3`: cerrado
- `Milestone 4`: pendiente

## Lo que ya funciona

- Estructura modular con `data/`, `entities/` y `world/`
- Carga de nivel desde archivos externos
- Placeholder visual robusto cuando faltan assets
- Menu de inicio con seleccion de dificultad
- HUD con peces, nivel y modo o vidas
- Movimiento, salto, `super jump`, gravedad y colisiones
- Estados del jugador `idle`, `run`, `jump`, `fall`, `crouch`, `hurt` y `dance`
- Peces coleccionables y salida bloqueada hasta cumplir meta
- Dificultad `facil` y `normal`
- Pausa, reinicio, `game_over` y `victory`
- Transiciones de presentacion entre niveles
- Fondo y tiles de laguna con render cacheado
- Hormigas acuaticas con patrulla y alerta
- Pulpos con zona de amenaza visible
- Algas moviles que transportan al jugador
- Lanzadores de burbujas con neutralizacion de enemigos
- Peces linterna con brillo reactivo
- Musica de menu y gameplay generada de forma procedural
- Efectos de sonido procedurales para acciones y estados principales
- Tres niveles funcionales con progresion completa

## Lo que todavia falta

- Assets finales consistentes para jugador, enemigos y UI
- Pasada de balance y testing mas profunda

## Deuda tecnica visible

- El arte sigue siendo procedural o placeholder en varias entidades
- El audio actual es sintetico y funcional, no final
- Los niveles existen, pero aun falta una pasada fuerte de balance entre ellos
- Falta una bateria de pruebas mas formal; hoy predominan smoke tests

## Lectura del estado del proyecto

La base tecnica ya soporta crecimiento. El riesgo principal ya no es la estructura sino el pulido: hace falta afinar claridad, balance y presentacion final para que la progresion completa se sienta consistente.

El foco principal paso a ser `Milestone 4`: reemplazar placeholders, terminar presentacion visual y sonora, y hacer una pasada fuerte de balance.
