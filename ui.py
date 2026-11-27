"""
ui.py - Parte gráfica de Space Waze con pygame.
Aquí solo se dibuja y se lee el teclado y el mouse; las reglas están en game_logic.py.
"""
import os
import sys
import math
import random
import pygame
import game_logic as gl

# ---------------- Paso 2: constantes ----------------
ANCHO = 900
ALTO = 640
FPS = 60
ANCHO_COLUMNA = 150

COLORES = {
    "fondo": [8, 10, 28],
    "texto": [225, 235, 255],
    "suave": [130, 145, 185],
    "azul": [80, 160, 255],
    "rojo": [240, 80, 95],
    "verde": [90, 230, 140],
    "amarillo": [255, 215, 80],
}

ZONA_RIVAL = pygame.Rect(75, 78, 750, 210)     # arriba
ZONA_PROPIA = pygame.Rect(75, 362, 750, 210)   # abajo

CARPETA_SPRITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sprites")
ARCHIVOS = {
    "nave": "nave_jugador.png",
    "nave_rival": "nave_rival.png",
    "laser": "laser.png",
    "mira": "mira.png",
    "fallo": "fallo.png",
    "icono": "icono.png",
}

VELOCIDAD_LASER = 950    # píxeles por segundo
NUM_CUADROS = 6          # cuadros de la explosión
DURACION_CUADRO = 0.09   # segundos por cuadro
DURACION_TEXTO = 1.1     # segundos que dura "¡IMPACTO!"

IMAGENES = {}
FUENTES = {}
EXPLOSIONES = []          # son listas porque los cuadros van en orden
EXPLOSIONES_GRANDES = []


# ---------------- Paso 3: carga de recursos ----------------
def cargar_imagen(nombre_archivo):
    """Carga un PNG de assets/sprites. Si no existe, devuelve un cuadro de color."""
    ruta = os.path.join(CARPETA_SPRITES, nombre_archivo)
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
    except Exception:
        imagen = pygame.Surface([48, 48])
        imagen.fill([200, 0, 200])
    return imagen


def cargar_recursos():
    """Carga todas las imágenes y fuentes una sola vez."""
    for clave in ARCHIVOS:
        IMAGENES[clave] = cargar_imagen(ARCHIVOS[clave])

    for i in range(NUM_CUADROS):
        cuadro = cargar_imagen("explosion_" + str(i) + ".png")
        EXPLOSIONES.append(cuadro)
        EXPLOSIONES_GRANDES.append(pygame.transform.scale(cuadro, [128, 128]))

    FUENTES["chica"] = pygame.font.Font(None, 24)
    FUENTES["normal"] = pygame.font.Font(None, 30)
    FUENTES["grande"] = pygame.font.Font(None, 46)
    FUENTES["titulo"] = pygame.font.Font(None, 96)


# ---------------- Paso 4: ventana ----------------
def iniciar_ventana():
    """Abre la ventana del juego y carga los recursos."""
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    pygame.display.set_caption("Space Waze - Equipo Nova")
    cargar_recursos()            # después de set_mode, porque convert_alpha necesita la ventana
    pygame.display.set_icon(IMAGENES["icono"])
    return pantalla


def revisar_cierre(evento):
    """Si el usuario cierra la ventana con la X, termina el programa."""
    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def escribir(pantalla, texto, fuente, color, centro):
    """Escribe un texto centrado en la posición 'centro'."""
    superficie = FUENTES[fuente].render(texto, True, color)
    rect = superficie.get_rect(center=centro)
    pantalla.blit(superficie, rect)

    # ---------------- Paso 5: fondo de estrellas ----------------
def crear_estrellas(cantidad):
    """Crea una lista de estrellas; cada una es un diccionario."""
    estrellas = []
    for i in range(cantidad):
        estrella = {
            "x": random.uniform(0, ANCHO),
            "y": random.uniform(0, ALTO),
            "velocidad": random.uniform(8, 45),
        }
        estrellas.append(estrella)
    return estrellas


def mover_estrellas(estrellas, dt):
    """Baja las estrellas; las que salen por abajo vuelven arriba."""
    for estrella in estrellas:
        estrella["y"] += estrella["velocidad"] * dt
        if estrella["y"] > ALTO:
            estrella["y"] = 0
            estrella["x"] = random.uniform(0, ANCHO)


def dibujar_estrellas(pantalla, estrellas):
    """Pinta el fondo y las estrellas (las rápidas se ven más grandes)."""
    pantalla.fill(COLORES["fondo"])
    for estrella in estrellas:
        tamano = 1
        if estrella["velocidad"] > 30:
            tamano = 2
        pantalla.fill([200, 200, 230], [int(estrella["x"]), int(estrella["y"]), tamano, tamano])

# ---------------- Paso 6: tablero ----------------
def rect_columna(zona, columna):
    """Rectángulo de la columna (1 a 5) dentro de una zona."""
    return pygame.Rect(zona.x + (columna - 1) * ANCHO_COLUMNA, zona.y, ANCHO_COLUMNA, zona.height)


def columna_en_punto(zona, punto):
    """Columna donde se hizo clic, o 0 si fue fuera de la zona."""
    if not zona.collidepoint(punto):
        return 0
    return (punto[0] - zona.x) // ANCHO_COLUMNA + 1


def dibujar_zona(pantalla, zona, titulo, color, activa):
    """Dibuja las 5 columnas de una zona. Si está activa, resalta la columna bajo el mouse."""
    for columna in range(1, gl.NUM_POSICIONES + 1):
        rect = rect_columna(zona, columna)
        alfa = 12
        if columna % 2 == 1:
            alfa = 22
        if activa and rect.collidepoint(pygame.mouse.get_pos()):
            alfa = 55
        capa = pygame.Surface([rect.width, rect.height], pygame.SRCALPHA)
        capa.fill([color[0], color[1], color[2], alfa])
        pantalla.blit(capa, rect)
        escribir(pantalla, str(columna), "normal", COLORES["suave"], [rect.centerx, rect.bottom - 16])
    pygame.draw.rect(pantalla, color, zona, 2, border_radius=8)
    escribir(pantalla, titulo, "chica", color, [zona.centerx, zona.y - 12])

# ---------------- Paso 7: animaciones ----------------
def crear_efecto(tipo, x, y, destino_x, destino_y, acierto, texto):
    """Crea un efecto: 'laser', 'explosion' o 'texto'."""
    return {"tipo": tipo, "x": x, "y": y, "destino_x": destino_x, "destino_y": destino_y,
            "tiempo": 0.0, "acierto": acierto, "texto": texto}


def actualizar_efectos(efectos, dt):
    """Avanza las animaciones y devuelve una lista NUEVA con los efectos que siguen vivos."""
    vivos = []
    for efecto in efectos:
        efecto["tiempo"] += dt
        if efecto["tipo"] == "laser":
            dx = efecto["destino_x"] - efecto["x"]
            dy = efecto["destino_y"] - efecto["y"]
            distancia = math.hypot(dx, dy)
            paso = VELOCIDAD_LASER * dt
            if distancia <= paso:
                x = efecto["destino_x"]
                y = efecto["destino_y"]
                vivos.append(crear_efecto("explosion", x, y, x, y, efecto["acierto"], ""))
                if efecto["acierto"]:
                    vivos.append(crear_efecto("texto", x, y - 60, x, y - 60, False, "¡IMPACTO!"))
                else:
                    vivos.append(crear_efecto("texto", x, y - 50, x, y - 50, False, "FALLO"))
            else:
                efecto["x"] += dx / distancia * paso
                efecto["y"] += dy / distancia * paso
                vivos.append(efecto)
        elif efecto["tipo"] == "explosion":
            if efecto["tiempo"] < NUM_CUADROS * DURACION_CUADRO:
                vivos.append(efecto)
        elif efecto["tipo"] == "texto":
            if efecto["tiempo"] < DURACION_TEXTO:
                efecto["y"] -= 35 * dt
                vivos.append(efecto)
    return vivos


def dibujar_centrado(pantalla, imagen, x, y):
    """Dibuja una imagen con su centro en (x, y)."""
    pantalla.blit(imagen, imagen.get_rect(center=[int(x), int(y)]))


def dibujar_efectos(pantalla, efectos):
    """Dibuja láseres, explosiones y textos flotantes."""
    for efecto in efectos:
        if efecto["tipo"] == "laser":
            dibujar_centrado(pantalla, IMAGENES["laser"], efecto["x"], efecto["y"])
        elif efecto["tipo"] == "explosion":
            cuadro = int(efecto["tiempo"] / DURACION_CUADRO)
            if cuadro > NUM_CUADROS - 1:
                cuadro = NUM_CUADROS - 1
            if efecto["acierto"]:
                imagen = EXPLOSIONES_GRANDES[cuadro]
            else:
                imagen = EXPLOSIONES[cuadro]
            dibujar_centrado(pantalla, imagen, efecto["x"], efecto["y"])
        elif efecto["tipo"] == "texto":
            color = COLORES["amarillo"]
            if efecto["texto"] == "¡IMPACTO!":
                color = COLORES["rojo"]
            superficie = FUENTES["grande"].render(efecto["texto"], True, color)
            superficie.set_alpha(int(255 * (1 - efecto["tiempo"] / DURACION_TEXTO)))
            dibujar_centrado(pantalla, superficie, efecto["x"], efecto["y"])


def lanzar_disparo(efectos, vista):
    """Agrega a 'efectos' la animación del último disparo de la vista."""
    ultimo = vista["ultimo"]
    if ultimo["columna"] == 0:
        efectos.append(crear_efecto("texto", ANCHO // 2, 325, ANCHO // 2, 325, False, "TURNO PERDIDO"))
        return
    if ultimo["jugador"] == vista["jugador"]:
        destino = rect_columna(ZONA_RIVAL, ultimo["columna"]).center
        inicio_x = rect_columna(ZONA_PROPIA, vista["mi_nave"]).centerx
        inicio_y = ZONA_PROPIA.centery - 30
    else:
        destino = rect_columna(ZONA_PROPIA, ultimo["columna"]).center
        inicio_x = destino[0]
        inicio_y = ZONA_RIVAL.bottom - 20
    efectos.append(crear_efecto("laser", inicio_x, inicio_y, destino[0], destino[1], ultimo["acierto"], ""))

# ---------------- Paso 8: controles ----------------
def crear_boton(texto, opcion, centro_x, centro_y):
    """Crea un botón del menú."""
    rect = pygame.Rect(0, 0, 340, 58)
    rect.center = [centro_x, centro_y]
    return {"texto": texto, "opcion": opcion, "rect": rect}


def dibujar_boton(pantalla, boton):
    """Dibuja el botón; cambia de color si el mouse está encima."""
    encima = boton["rect"].collidepoint(pygame.mouse.get_pos())
    relleno = [20, 28, 60]
    borde = COLORES["suave"]
    if encima:
        relleno = [35, 60, 120]
        borde = COLORES["azul"]
    pygame.draw.rect(pantalla, relleno, boton["rect"], border_radius=12)
    pygame.draw.rect(pantalla, borde, boton["rect"], 2, border_radius=12)
    escribir(pantalla, boton["texto"], "normal", COLORES["texto"], boton["rect"].center)


def boton_presionado(evento, boton):
    """True si se hizo clic izquierdo sobre el botón."""
    return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
            and boton["rect"].collidepoint(evento.pos))


def es_confirmar(evento):
    """True si se presionó ENTER o ESPACIO."""
    return evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]


def leer_eleccion(evento, zona, seleccion):
    """Devuelve lo que eligió el jugador SIN validarlo, o "" si no eligió nada."""
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        columna = columna_en_punto(zona, evento.pos)
        if columna != 0:
            return columna
    elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_LEFT:
            if seleccion == 0:
                return 3
            return max(1, seleccion - 1)
        if evento.key == pygame.K_RIGHT:
            if seleccion == 0:
                return 3
            return min(gl.NUM_POSICIONES, seleccion + 1)
        if es_confirmar(evento) or evento.key == pygame.K_ESCAPE:
            return ""
        return evento.unicode.strip()
    return ""

# ---------------- Paso 9: diccionario del turno ----------------
def crear_turno():
    """Datos del turno del jugador: selección, mensaje y temporizador."""
    return {"seleccion": 0, "mensaje": "", "es_error": False, "inicio": 0, "clave": []}


def clave_de(vista):
    """Identifica cada turno: cambia cuando cambia la fase, el turno o hay un disparo nuevo."""
    return [vista["fase"], vista["mi_turno"], vista["total_disparos"]]


def reiniciar_turno(turno, vista):
    """Empieza un turno nuevo: borra la selección y arranca el temporizador."""
    turno["clave"] = clave_de(vista)
    turno["inicio"] = pygame.time.get_ticks()
    turno["seleccion"] = 0
    turno["mensaje"] = ""
    turno["es_error"] = False


def turno_listo(turno, vista):
    """True si el turno actual ya empezó (terminaron las animaciones)."""
    return turno["clave"] == clave_de(vista)


def ms_transcurridos(turno):
    """Milisegundos desde que empezó el turno."""
    return pygame.time.get_ticks() - turno["inicio"]


def avisar(turno, mensaje):
    """Muestra un mensaje de error en rojo."""
    turno["mensaje"] = mensaje
    turno["es_error"] = True


def aplicar_validacion(turno, resultado, eleccion):
    """Usa el [True/False, mensaje] de una validación de game_logic."""
    turno["mensaje"] = resultado[1]
    turno["es_error"] = not resultado[0]
    if resultado[0]:
        turno["seleccion"] = gl.convertir_jugada(eleccion)

# ---------------- Paso 10: textos y dibujo de la partida ----------------
def texto_estado(vista):
    """Frase de arriba según la fase y el turno."""
    if vista["fase"] == "colocar":
        if vista["mi_nave"] == 0:
            return "Coloca tu nave: elige 1-5 y presiona ENTER"
        return "Esperando a que el rival coloque su nave..."
    if vista["fase"] == "fin":
        return gl.mensaje_final(vista["ganador"], vista["jugador"])
    if vista["mi_turno"]:
        return "¡TU TURNO! Apunta a una columna del rival"
    return "Turno del rival..."


def texto_ultimo(vista):
    """Frase que describe el último disparo."""
    if vista["ultimo"] is None:
        return ""
    ultimo = vista["ultimo"]
    quien = "El rival"
    if ultimo["jugador"] == vista["jugador"]:
        quien = "Tú"
    if ultimo["columna"] == 0:
        return quien + " perdió el turno"
    if ultimo["acierto"]:
        return quien + " acertó en la columna " + str(ultimo["columna"])
    return quien + " falló en la columna " + str(ultimo["columna"])


def dibujar_nave(pantalla, imagen, zona, posicion):
    """Dibuja una nave flotando en su columna."""
    x = rect_columna(zona, posicion).centerx
    y = zona.centery + math.sin(pygame.time.get_ticks() / 300) * 5
    dibujar_centrado(pantalla, imagen, x, y)


def dibujar_fallos(pantalla, disparos, zona, columna_acierto):
    """Dibuja una X en cada columna disparada que no fue acierto."""
    for columna in disparos:
        if columna != columna_acierto:
            centro = rect_columna(zona, columna).center
            dibujar_centrado(pantalla, IMAGENES["fallo"], centro[0], centro[1])


def dibujar_barra_tiempo(pantalla, segundos):
    """Barra de tiempo: verde, luego amarilla y al final roja."""
    fraccion = segundos / gl.TIEMPO_TURNO
    color = COLORES["rojo"]
    if fraccion > 0.25:
        color = COLORES["amarillo"]
    if fraccion > 0.5:
        color = COLORES["verde"]
    pygame.draw.rect(pantalla, [40, 45, 70], [ANCHO - 190, 14, 150, 20], border_radius=6)
    pygame.draw.rect(pantalla, color, [ANCHO - 190, 14, int(150 * fraccion), 20], border_radius=6)
    escribir(pantalla, str(math.ceil(segundos)) + " s", "normal", COLORES["texto"], [ANCHO - 20, 24])


def dibujar_final(pantalla, vista, texto_fin):
    """Pantalla de GANASTE / PERDISTE encima del tablero."""
    capa = pygame.Surface([ANCHO, ALTO], pygame.SRCALPHA)
    capa.fill([0, 0, 0, 160])
    pantalla.blit(capa, [0, 0])
    color = COLORES["rojo"]
    if vista["ganador"] == vista["jugador"]:
        color = COLORES["verde"]
    escribir(pantalla, gl.mensaje_final(vista["ganador"], vista["jugador"]), "titulo", color,
             [ANCHO // 2, ALTO // 2 - 30])
    escribir(pantalla, texto_fin, "normal", COLORES["texto"], [ANCHO // 2, ALTO // 2 + 40])


def dibujar_partida(pantalla, vista, turno, segundos, efectos, ayuda, texto_fin):
    """Dibuja todo el tablero a partir de la vista. segundos = -1 si no hay temporizador."""
    colocando = vista["fase"] == "colocar" and vista["mi_nave"] == 0

    # Zonas y marcas de fallos
    dibujar_zona(pantalla, ZONA_RIVAL, "Zona del rival", COLORES["rojo"], vista["mi_turno"])
    dibujar_zona(pantalla, ZONA_PROPIA, "Tu zona", COLORES["azul"], colocando)
    dibujar_fallos(pantalla, vista["mis_disparos"], ZONA_RIVAL, vista["nave_rival"])
    dibujar_fallos(pantalla, vista["disparos_rival"], ZONA_PROPIA, vista["mi_nave"])

    # Naves (al colocar se ve una vista previa en la columna elegida)
    posicion = vista["mi_nave"]
    if colocando:
        posicion = turno["seleccion"]
    if posicion != 0:
        dibujar_nave(pantalla, IMAGENES["nave"], ZONA_PROPIA, posicion)
    if vista["nave_rival"] != 0:
        dibujar_nave(pantalla, IMAGENES["nave_rival"], ZONA_RIVAL, vista["nave_rival"])

    # Mira sobre la columna elegida
    if vista["mi_turno"] and turno["seleccion"] != 0:
        centro = rect_columna(ZONA_RIVAL, turno["seleccion"]).center
        dibujar_centrado(pantalla, IMAGENES["mira"], centro[0], centro[1])

    dibujar_efectos(pantalla, efectos)

    # Textos de arriba y barra de tiempo
    escribir(pantalla, "RONDA " + str(vista["ronda"]), "normal", COLORES["suave"], [80, 24])
    color_estado = COLORES["texto"]
    if vista["mi_turno"]:
        color_estado = COLORES["verde"]
    escribir(pantalla, texto_estado(vista), "normal", color_estado, [ANCHO // 2, 24])
    if segundos >= 0:
        dibujar_barra_tiempo(pantalla, segundos)

    # Mensaje del centro
    if turno["mensaje"] != "":
        color_mensaje = COLORES["verde"]
        if turno["es_error"]:
            color_mensaje = COLORES["rojo"]
        escribir(pantalla, turno["mensaje"], "normal", color_mensaje, [ANCHO // 2, 325])
    else:
        escribir(pantalla, texto_ultimo(vista), "normal", COLORES["amarillo"], [ANCHO // 2, 325])

    escribir(pantalla, ayuda, "chica", COLORES["suave"], [ANCHO // 2, ALTO - 26])

    if vista["fase"] == "fin" and efectos == []:
        dibujar_final(pantalla, vista, texto_fin)

