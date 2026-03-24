# Flujo de Juego

## Loop principal

El flujo esperado del juego es:

1. Pantalla inicial
2. Seleccion de dificultad
3. Inicio de nivel
4. Juego activo
5. Pausa o reinicio si el jugador lo pide
6. Reinicio por dano o caida segun dificultad
7. Fin de nivel al llegar a la salida con peces suficientes
8. Transicion al siguiente nivel
9. Victoria final al completar el nivel 3

## Estados del juego

- `menu`
- `difficulty_select`
- `playing`
- `paused`
- `level_complete`
- `game_over`
- `victory`

## Controles esperados

- Flechas izquierda y derecha: mover al personaje
- Flecha abajo: agacharse
- Espacio: saltar
- `R`: reiniciar nivel
- `P`: pausar y reanudar

## Reglas del jugador

- El jugador puede moverse a izquierda y derecha
- El jugador puede saltar solo cuando esta en suelo o plataforma valida
- El jugador puede agacharse para cambiar su pose y eventualmente pasar por sectores bajos
- El jugador recolecta peces al tocarlos
- El jugador sufre dano al caer en pozos o tocar enemigos hostiles
- El jugador hace un baile al completar un nivel

## Dificultad

### Facil

- El jugador no pierde vidas
- Si recibe dano o cae, el nivel se reinicia
- La progresion general se mantiene amable

### Normal

- El jugador pierde una vida al recibir dano o caer
- Si quedan vidas, el nivel se reinicia
- Si no quedan vidas, aparece `game_over`

## Reglas de progresion

- Cada nivel define una cantidad minima de peces
- La salida queda bloqueada hasta alcanzar esa cantidad
- Al tocar la salida con la meta cumplida, se activa `level_complete`
- El nivel siguiente se desbloquea automaticamente en la misma sesion

## Reglas de pausa

- El estado `paused` congela entidades y fisica
- Debe mostrar un overlay simple con opcion de continuar o reiniciar
- El audio puede bajar de volumen o pausarse

## Reglas de dano y reinicio

- Caer en un pozo cuenta como dano o fallo de nivel
- Tocar un enemigo hostil cuenta como dano
- Al reiniciar, el jugador vuelve al spawn del nivel
- Los coleccionables del intento actual vuelven a su estado inicial
- Los enemigos vuelven a su posicion original

## Feedback esperado

- Al juntar un pez: efecto visual y sonido corto
- Al recibir dano: animacion o flash y sonido
- Al completar nivel: fanfarria breve, baile del monstruo y transicion
- Al pausar: overlay claro
- Al llegar a una salida bloqueada: feedback de que faltan peces
