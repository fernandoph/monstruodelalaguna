# Backlog Priorizado

## Objetivo

Traducir la vision del juego a trabajo ejecutable, con dependencias claras y prioridad realista.

## Convenciones

- `P0`: bloquea el resto o habilita el loop jugable base
- `P1`: agrega mecanicas centrales del juego
- `P2`: pulido, contenido final y mejora de experiencia

## P0. Base tecnica y loop jugable

### BLK-001. Limpiar estructura del proyecto

- Crear estructura de carpetas para datos, UI, enemigos y objetos
- Extraer configuraciones globales a un modulo claro
- Separar entrada del juego de la logica de estados
- Definir un `.gitignore`

### BLK-002. Externalizar niveles

- Dejar de usar una lista embebida para el mapa
- Definir formato de capas y metadatos
- Implementar loader de nivel
- Validar spawn, salida y meta de peces

### BLK-003. Robustecer carga de assets

- Centralizar carga de imagenes
- Manejar faltantes con errores claros o placeholders
- Definir convencion de rutas

### BLK-004. Completar estados basicos del jugador

- `idle`
- `run`
- `jump`
- `fall`
- `crouch`
- `hurt`
- `dance`

### BLK-005. Reglas de input y fisica

- Evitar salto continuo por tecla mantenida
- Agregar deteccion de suelo confiable
- Agregar agacharse
- Ajustar hitbox cuando corresponda

### BLK-006. HUD minimo

- Mostrar nivel actual
- Mostrar peces recolectados
- Mostrar vidas o indicador de modo facil

## P1. Mecanicas centrales

### MEC-001. Peces coleccionables

- Crear entidad de pez
- Detectar coleccion
- Actualizar HUD
- Reponer estado al reiniciar nivel

### MEC-002. Salida y progresion

- Crear entidad de salida
- Bloquear salida hasta cumplir meta
- Pasar al siguiente nivel
- Activar baile al completar

### MEC-003. Sistema de dificultad

- Implementar `facil` y `normal`
- Manejar vidas
- Implementar `game_over`

### MEC-004. Pausa y reinicio

- Pausar actualizacion del mundo
- Mostrar overlay
- Reiniciar nivel con `R`

### MEC-005. Pozos y hazards

- Separar peligros de colisiones solidas
- Implementar caida fuera de zona segura
- Definir reinicio y dano

## P1. Enemigos y plataformas especiales

### ENM-001. Hormiga acuatica

- Patrulla simple
- Dano al contacto
- Integracion con colisiones

### ENM-002. Pulpo

- Zona de amenaza
- Animacion de tentaculos
- Captura o dano si el jugador no escapa

### OBJ-001. Algas moviles

- Movimiento ciclico
- Transporte del jugador si esta arriba

### OBJ-002. Lanzadores de burbujas

- Activacion por contacto o input
- Proyectil o columna de burbujas
- Neutralizacion de enemigos

### OBJ-003. Peces linterna

- Halo visual
- Apagado o atenuacion al acercarse el jugador

## P2. UX, contenido y pulido

### UX-001. Menu inicial

- Pantalla de presentacion
- Inicio de partida
- Salida del juego

### UX-002. Selector de dificultad

- Seleccion simple antes de empezar
- Feedback visual del modo elegido

### UX-003. Pantallas de estado

- `paused`
- `game_over`
- `victory`
- `level_complete`

### CNT-001. Construccion del nivel 1

- Layout final
- Peces y salida
- Ajuste de dificultad

### CNT-002. Construccion del nivel 2

- Introduccion de algas y peces linterna
- Ajuste de ritmo y lectura

### CNT-003. Construccion del nivel 3

- Pulpos
- Lanzadores de burbujas
- Secuencia final

### ART-001. Reemplazo de placeholders

- Personaje completo
- Tiles finales
- Enemigos finales
- UI final
- Fondos

### AUD-001. Integracion de audio

- Musica
- SFX de accion
- SFX de estados

### QA-001. Balance y testing

- Ajustar cantidad de peces
- Ajustar dano y vidas
- Ajustar velocidad de enemigos
- Probar legibilidad y claridad de objetivos

## Dependencias principales

- `BLK-002` depende de `BLK-001`
- `BLK-006` depende de `MEC-001` y `MEC-003`
- `MEC-002` depende de `MEC-001`
- `ENM-002` depende de `BLK-004`
- `OBJ-002` depende de `ENM-001` o `ENM-002`
- `CNT-002` y `CNT-003` dependen de mecanicas previas
- `ART-001` y `AUD-001` pueden avanzar en paralelo con programacion, pero deben seguir convenciones cerradas

## Primer corte recomendable

El primer hito realmente jugable deberia incluir:

- `BLK-001`
- `BLK-002`
- `BLK-003`
- `BLK-004`
- `BLK-005`
- `MEC-001`
- `MEC-002`
- `MEC-003`
- `MEC-004`
- `CNT-001`

## Definition of Done por tarea

Cada tarea deberia darse por terminada cuando:

- Tiene comportamiento implementado
- Tiene assets minimos funcionales
- Se puede probar manualmente dentro del juego
- No rompe el loop jugable existente
- Tiene criterios de uso claros para contenido futuro
