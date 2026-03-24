# Niveles y Progresion

## Objetivo del documento

Definir como escalan los niveles, que mecanicas introduce cada uno y que cantidad de contenido hace falta para sostener la progresion.

## Estructura general

El juego tendra 3 niveles con dificultad creciente. Cada nivel deberia:

- Introducir una nueva mecanica o combinar mecanicas previas
- Exigir una cantidad minima de peces
- Tener cartel de inicio y salida
- Comunicar visualmente el camino principal

## Nivel 1

### Objetivo

Presentar el mundo, los controles y la idea de juntar peces para habilitar la salida.

### Contenido sugerido

- Caminos amplios
- Saltos cortos
- Pocos pozos
- Pocas plataformas elevadas
- Peces ubicados en zonas faciles de leer
- Un enemigo simple o ninguno en la primera mitad

### Mecanicas activas

- Movimiento
- Salto
- Agacharse
- Peces coleccionables
- Salida bloqueada hasta cumplir meta

## Nivel 2

### Objetivo

Introducir movimiento de plataformas y amenazas mas activas.

### Contenido sugerido

- Algas moviles
- Primeros peces linterna
- Hormigas acuaticas patrullando
- Sectores con mayor verticalidad

### Mecanicas activas

- Todo lo del nivel 1
- Plataformas moviles
- Enemigos de patrulla
- Iluminacion reactiva simple

## Nivel 3

### Objetivo

Cerrar el juego combinando todas las mecanicas y exigiendo mayor precision sin perder legibilidad.

### Contenido sugerido

- Mezcla de algas moviles y enemigos
- Pulpos con zonas de amenaza
- Lanzadores de burbujas en posiciones clave
- Mayor cantidad de peces requerida
- Secuencia final de salida y baile

### Mecanicas activas

- Todo lo anterior
- Pulpos
- Lanzadores de burbujas
- Combinaciones de obstaculos

## Curva de dificultad

- Nivel 1: ensenia reglas
- Nivel 2: pide coordinacion
- Nivel 3: pide combinacion de sistemas

## Metas de peces sugeridas

- Nivel 1: 5 peces
- Nivel 2: 8 peces
- Nivel 3: 12 peces

Estas cifras son iniciales y deben ajustarse en testing.

## Principios de diseno de niveles

- Evitar saltos ciegos
- Mostrar con claridad donde estan los peligros
- No esconder peces obligatorios de forma injusta
- Usar color, luz y composicion para marcar camino principal y desvio opcional
- Mantener zonas de respiro entre secciones dificiles

## Datos que cada nivel deberia tener

- Nombre
- Fondo o tema visual
- Meta de peces
- Spawn del jugador
- Posicion de salida
- Lista de enemigos
- Plataformas moviles
- Coleccionables
- Triggers especiales

## Condicion de cierre del juego

Al completar el nivel 3, debe mostrarse una secuencia breve de victoria con:

- Baile del monstruo
- Confirmacion visual de juego completado
- Opcion de volver al menu principal
