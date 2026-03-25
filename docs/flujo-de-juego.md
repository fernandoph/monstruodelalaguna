# Flujo de Juego

## Loop principal

El flujo esperado del juego es:

1. Pantalla inicial
2. Seleccion de dificultad desde el menu
3. Presentacion breve del nivel
4. Juego activo
5. Pausa o reinicio si el jugador lo pide
6. Reinicio por dano o caida segun dificultad
7. Fin de nivel al llegar a la salida con peces suficientes
8. Presentacion del nivel siguiente
9. Victoria final al completar el nivel 3

## Estados del juego

- `menu`
- `level_intro`
- `playing`
- `paused`
- `game_over`
- `victory`

## Controles esperados

- Flechas izquierda y derecha: mover al personaje
- Flecha abajo: agacharse
- Espacio: saltar
- Dos toques rapidos de `Espacio`: activar un `super jump`
- `R`: reiniciar nivel
- `P`: pausar y reanudar

## Reglas del jugador

- El jugador puede moverse a izquierda y derecha
- El jugador puede saltar solo cuando esta en suelo o plataforma valida
- Si el jugador vuelve a pulsar salto rapidamente despues del primer salto, puede activar un `super jump` con una ventana amplia de input
- El jugador puede agacharse para cambiar su pose y eventualmente pasar por sectores bajos
- El jugador recolecta peces al tocarlos
- El jugador sufre dano al caer en pozos o tocar enemigos hostiles
- El jugador hace un baile al completar un nivel
- Al tocar un lanzador de burbujas, este se activa automaticamente y puede neutralizar enemigos en su columna
- Los peces linterna iluminan el entorno pero bajan su brillo si el jugador se acerca demasiado
- Las hormigas acuaticas patrullan, pero si detectan al jugador cerca cambian a persecucion corta
- Los pulpos telegraphan su amenaza con una zona visible antes de atrapar
- Las algas moviles desplazan al jugador mientras este arriba de la plataforma

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
- Al tocar la salida con la meta cumplida, se prepara la transicion al siguiente nivel
- El nivel siguiente se desbloquea automaticamente en la misma sesion

## Reglas de pausa

- El estado `paused` congela entidades y fisica
- Debe mostrar un overlay simple con opcion de continuar o reiniciar
- La musica del nivel se pausa y se reanuda al volver a jugar

## Reglas de dano y reinicio

- Caer en un pozo cuenta como dano o fallo de nivel
- Tocar un enemigo hostil cuenta como dano
- Quedarse demasiado tiempo dentro de la zona de amenaza de un pulpo tambien cuenta como dano
- Al reiniciar, el jugador vuelve al spawn del nivel
- Los coleccionables del intento actual vuelven a su estado inicial
- Los enemigos vuelven a su posicion original

## Feedback esperado

- Al saltar o hacer `super jump`: sonido breve y legible
- Al juntar un pez: efecto visual y sonido corto
- Al recibir dano: animacion o flash y sonido
- Al activar un surtidor: columna de burbujas, brillo y mensaje corto
- Al neutralizar un enemigo con burbujas: estallido visual reconocible
- En menu y gameplay: bucles musicales suaves que no tapen los efectos
- Al completar nivel: fanfarria breve, baile del monstruo y transicion
- Al pausar: overlay claro
- Al llegar a una salida bloqueada: feedback de que faltan peces
