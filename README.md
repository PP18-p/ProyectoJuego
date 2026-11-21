# ProyectoJuego
Proyecto integrador primer semestre

# [Space Waze]

Proyecto integrador de primer nivel · Lógica de Programación · UIDE · Paralelo [C]

Juego por turnos para dos jugadores con modo local y, más adelante, modo multijugador cliente-servidor en red LAN.

## Integrantes

- Jhair Celi
- José Paredes
- Dennis Toapanta

## Cómo ejecutarlo

Requiere Python 3. Desde la carpeta del repositorio:

```
python juego.py          (menú)
python game_logic.py     (validación de la jugada y fin de la partida)
```

## Estructura del repositorio

| Archivo | Qué hace | Estado |
|---|---|---|
| `juego.py` | [Menú que se repite hasta «Salir» (parte de DF1)] | [Terminado / Iniciado] |
| `game_logic.py` | [Validación de la jugada (DF2) y fin de la partida (DF3)] | [Terminado / Iniciado] |
| `server.py` | [Comentario con lo que hará el servidor (Jugador 1)] | [Pendiente] |
| `client.py` | [Comentario con lo que hará el cliente (Jugador 2)] | [Pendiente] |
| `diseno/` | Diagramas `.rap` de la Fase 2 | [Subido] |

## Del diseño al código

| Diagrama de la Fase 2 | Archivo y líneas | Qué cambió al traducirlo |
|---|---|---|
| DF1 Partida completa (solo el menú) | [`juego.py`, líneas …] | [...] |
| DF2 Validación de la jugada | game_logic.py, líneas 1-40 | El Loop de RAPTOR (sale cuando entrada = 0) pasó a ser un while entrada != 0. Se agregó isdigit() para que letras o decimales no hagan caer el programa (validación por formato), porque input devuelve texto. La concatenación con + pasó a f-strings. |
| DF3 Fin de la partida | [`game_logic.py`, líneas …] | [...] |

## Video explicativo

[Enlace al video] (máximo 5 minutos: el menú, la validación con una jugada inválida, el fin de la partida y cómo
tradujimos un diagrama a código).

## Licencia

Este proyecto se distribuye bajo la licencia [MIT]. El texto completo está en el archivo `LICENSE`.

## Declaración de autoría

Declaramos que el código de este repositorio fue escrito por los integrantes del equipo, salvo los recursos
citados en la sección «Créditos».

## Créditos

| Recurso (código, librería, imagen…) | Autor o fuente | Dónde se usa | Licencia |
|---|---|---|---|
| [...] | [...] | [...] | [...] |

### Uso de IA

| Herramienta | Para qué la usamos | Qué revisamos o cambiamos nosotros |
|---|---|---|
| Claude | Guía en redacción y construcción de código | Escritura del código fuente, designación de variables, pruebas de escritorio |

