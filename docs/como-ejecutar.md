# Como Ejecutar

## Requisitos

- Python 3.9 o superior
- Un entorno con soporte para abrir ventanas de `pygame`

## Opcion rapida con el `venv` actual del repo

Desde la raiz del proyecto:

```bash
./venv/bin/python monstruo.py
```

## Opcion recomendada

Crear un entorno virtual nuevo e instalar dependencias desde cero:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python monstruo.py
```

## Archivo de entrada

El juego arranca desde [monstruo.py](/home/fernandoph/projects/monstruodelalaguna/monstruo.py).

## Controles actuales

- `1`: iniciar partida en modo facil
- `2`: iniciar partida en modo normal
- Flechas izquierda y derecha: mover
- Flecha abajo: agacharse
- Espacio: saltar
- Dos toques rapidos de `Espacio`: `super jump` o salto doble asistido
- `P`: pausar o reanudar
- `R`: reiniciar nivel
- `M`: volver al menu cuando el juego esta en pausa
- `Enter` o `R`: volver al menu desde `game over` o `victory`

La ventana para el segundo toque es deliberadamente generosa: alrededor de `0.4s` a `60 FPS`, pensada para que una nina de 7 anios pueda activarlo sin precision fina.

En el estado actual del juego:

- las algas moviles hacen un recorrido oscilante y te arrastran si quedas arriba
- las hormigas acuaticas patrullan y se activan si te detectan cerca
- los pulpos muestran una zona de amenaza antes de atrapar
- los lanzadores de burbujas se activan al tocarlos
- las burbujas suben en columna, tienen recarga corta y pueden eliminar hormigas o pulpos
- los peces linterna pierden intensidad y se alejan cuando el jugador se acerca
- el `level_01` ya usa estas mecanicas como parte del recorrido y de la recoleccion de peces
- el juego ya tiene musica de menu y de nivel, mas efectos procedurales para salto, `super jump`, pez, dano, burbujas, pausa y victoria

## Problemas comunes

### Se abre una ventana pero no inicia la partida

Eso es esperado: primero hay que elegir dificultad con `1` o `2`.

### El personaje cambia a un sprite repetido al moverse

Hoy solo hay frames reales para `idle`. Las animaciones faltantes se generan de forma procedural a partir de esos frames para que `run`, `jump`, `fall`, `crouch`, `hurt` y `dance` no queden estaticos mientras faltan assets especificos.

### Quiero ejecutar solo una prueba tecnica

Se puede correr un smoke test sin abrir ventana real:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy ./venv/bin/python -c "from game import Game; Game().run(max_frames=2)"
```

### Quiero correrlo sin sonido real

Si el entorno no tiene dispositivo de audio o solo queres validar el loop:

```bash
SDL_AUDIODRIVER=dummy ./venv/bin/python monstruo.py
```
