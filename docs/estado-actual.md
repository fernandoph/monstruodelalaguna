# Estado Actual

## Resumen

El proyecto ya no es solo un prototipo tecnico. Hoy existe un primer nivel jugable con menu, HUD, dificultad, recoleccion de peces, salida bloqueada, pausa, reinicio y un conjunto inicial de amenazas y objetos especiales.

## Estado del roadmap

- `Milestone 0`: cerrado
- `Milestone 1`: cerrado
- `Milestone 2`: cerrado en una primera version jugable y legible
- `Milestone 3`: pendiente
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
- Fondo y tiles de laguna con render cacheado
- Hormigas acuaticas con patrulla y alerta
- Pulpos con zona de amenaza visible
- Algas moviles que transportan al jugador
- Lanzadores de burbujas con neutralizacion de enemigos
- Peces linterna con brillo reactivo

## Lo que todavia falta

- Nivel 2
- Nivel 3
- Curva completa de progresion entre niveles
- Secuencia de victoria final del juego completo
- Assets finales consistentes para jugador, enemigos y UI
- Sonido y musica
- Pasada de balance y testing mas profunda

## Deuda tecnica visible

- El arte sigue siendo procedural o placeholder en varias entidades
- No hay audio integrado
- El contenido todavia esta concentrado en un solo nivel
- Falta una bateria de pruebas mas formal; hoy predominan smoke tests

## Lectura del estado del proyecto

La base tecnica ya soporta crecimiento. El riesgo principal ya no es la estructura sino el contenido: hace falta construir los niveles restantes sin perder claridad de lectura ni balance.
