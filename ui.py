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