# Space Waze

Proyecto integrador de primer nivel · Lógica de Programación · UIDE · Paralelo C

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
| `juego.py` | Menú que se repite hasta «Salir» (parte de DF1) | Terminado |
| `game_logic.py` | Validación de la jugada (DF2) y fin de la partida (DF3) | Terminado |
| `server.py` | Servidor del Jugador 1 (TCP, puerto 5000), se programa en la Fase 4 | Pendiente |
| `client.py` | Cliente del Jugador 2, se conecta al servidor, se programa en la Fase 4 | Pendiente |
| `diseno/` | Diagramas `.rap` de la Fase 2 | Subido |

## Del diseño al código

| Diagrama de la Fase 2 | Archivo y líneas | Qué cambió al traducirlo |
|---|---|---|
| DF1 Partida completa (solo el menú) | `juego.py`, líneas 1-40 | El Loop de RAPTOR (sale cuando `opcion = 3`) pasó a ser un `while opcion != 3`. La validación de la opción revisa el texto con `not in ("1", "2", "3")` antes de convertirlo con `int()`, para que una letra no haga caer el programa. El texto del menú se guardó en una variable para no repetirlo. Las opciones 1 y 2 por ahora solo muestran un mensaje; la partida completa y la conexión se programan en la Fase 4. |
| DF2 Validación de la jugada | `game_logic.py`, líneas 1-42 | El Loop de RAPTOR (sale cuando `entrada = 0`) pasó a ser un `while entrada != 0`. Se agregó `isdigit()` para que letras o decimales no hagan caer el programa (validación por formato), porque `input` devuelve texto. El lado «No» del rombo pasó a `elif entrada != 0` para que el 0 termine el bucle sin mostrar error. La concatenación con `+` pasó a f-strings. |
| DF3 Fin de la partida | `game_logic.py`, líneas 44-69 | Ya no usa su propio estado de ejemplo: toma `turno`, las naves y `eleccion` de DF2. El rombo `turno = 1` pasó a `if/else` para identificar al rival y su nave. La condición de acierto se tradujo a `eleccion != 0 and eleccion == nave_rival`. Los dos rombos finales pasaron a un solo `if/elif/else`: gana el Jugador 1, gana el Jugador 2 o la partida continúa. Según el RF-11 no existe empate, así que ese caso queda en el `else`. |

## Video explicativo

<<Enlace al video>> (máximo 5 minutos: el menú, la validación con una jugada inválida, el fin de la partida y cómo tradujimos un diagrama a código).

## Licencia

Este proyecto se distribuye bajo la licencia MIT. El texto completo está en el archivo `LICENSE`.

## Declaración de autoría

Declaramos que el código de este repositorio fue escrito por los integrantes del equipo, salvo los recursos citados en la sección «Créditos».

## Créditos

| Recurso (código, librería, imagen…) | Autor o fuente | Dónde se usa | Licencia |
|---|---|---|---|
| Python 3 (sin librerías externas) | Python Software Foundation | Todo el código | PSF License |
| RAPTOR | Martin C. Carlisle | Diagramas de la carpeta `diseno/` | Uso libre |

No se usó código, imágenes ni librerías de terceros.

### Uso de IA

| Herramienta | Para qué la usamos | Qué revisamos o cambiamos nosotros |
|---|---|---|
| Claude (Anthropic) | Como tutor para guiar la traducción de DF2 a Python, revisar el código, armar los comentarios de RF de `game_logic.py` y `juego.py` y los comentarios de `server.py`, `client.py` y revisar este README. | Escribimos el código de `juego.py` y `game_logic.py`, elegimos los nombres de variables siguiendo los diagramas, hicimos las pruebas de escritorio y ejecutamos el código. Ajustamos los comentarios y el README a nuestra versión final. | 

