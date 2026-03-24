# Estado Actual

## Resumen

El repositorio contiene un prototipo chico en `pygame` con una base de platformer 2D. Ya existe una ventana funcional, un mapa simple, un personaje controlable, gravedad, salto, colisiones contra tiles y un scroll horizontal basico.

## Lo que ya funciona

- Inicializacion de `pygame`
- Loop principal de juego
- Carga de un nivel desde una matriz embebida
- Creacion de tiles solidos
- Spawn del jugador
- Movimiento horizontal
- Salto
- Gravedad
- Colision horizontal y vertical
- Scroll horizontal basado en la posicion del jugador
- Carga de frames de animacion desde carpetas

## Lo que existe pero esta incompleto

- El personaje ya busca animaciones `run`, `jump` y `fall`, pero hoy solo hay frames `idle`
- El mapa contiene al menos un marcador extra que no esta conectado a ninguna logica
- El `README` define controles y sistemas que todavia no existen en el codigo

## Lo que todavia no existe

- Agacharse
- Recoleccion de peces
- Sistema de vidas
- Dificultad
- Pausa
- Reinicio de nivel
- Carteles de inicio y salida
- Multiples niveles
- Enemigos
- Plataformas moviles
- Lanzadores de burbujas
- Peces linterna
- Pantallas de menu, game over o victoria
- HUD
- Sonido y musica integrados
- Persistencia o configuracion externa

## Deuda tecnica visible

- No hay `.gitignore`
- `venv/` esta dentro del repo
- Hay `__pycache__/` versionado o sin ignorar
- No hay `requirements.txt` ni `pyproject.toml`
- La configuracion esta acoplada al codigo
- El nivel esta hardcodeado en una lista de strings
- No hay separacion entre entidades solidas, peligros, coleccionables y triggers

## Lectura del estado del proyecto

La base actual sirve para empezar a construir el juego, pero todavia no alcanza para sostener la complejidad que pide el `README`. Antes de agregar mecanicas conviene ordenar la estructura, definir un formato de niveles y desacoplar los sistemas principales.

## Riesgos inmediatos

- Si se agregan mecanicas encima de la estructura actual, el codigo va a crecer de forma fragil
- Si los assets se producen sin reglas comunes, despues van a romper alineacion, hitboxes o scroll
- Si los niveles siguen embebidos en codigo, mantener tres niveles completos sera costoso
