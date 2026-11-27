"""
juego.py - Punto de entrada de Space Waze (Equipo Nova).
Solo maneja el menú y la interacción; las reglas están en game_logic.py y el dibujo en ui.py.
"""

import pygame
import game_logic as gl
import ui

# import server   <- quita el # cuando Jhair suba su parte
# import client

ESPERA_CPU = 1000  # milisegundos que el CPU "piensa" antes de disparar
AYUDA = "1-5 / flechas / clic: elegir   ENTER: confirmar   ESC: menú"
TEXTO_FIN = "R: jugar otra vez     ESC: menú"


# ---------------- Paso 12: menú ----------------
def menu_principal(pantalla, reloj, estrellas):
    """Muestra el menú y devuelve la opción elegida."""
    centro = ui.ANCHO // 2
    botones = [
        ui.crear_boton("Jugar contra el CPU", "local", centro, 300),
        ui.crear_boton("Crear partida en red", "servidor", centro, 375),
        ui.crear_boton("Unirse a partida", "cliente", centro, 450),
        ui.crear_boton("Salir", "salir", centro, 525),
    ]
    while True:
        dt = reloj.tick(ui.FPS) / 1000
        for evento in pygame.event.get():
            ui.revisar_cierre(evento)
            for boton in botones:
                if ui.boton_presionado(evento, boton):
                    return boton["opcion"]

        ui.mover_estrellas(estrellas, dt)
        ui.dibujar_estrellas(pantalla, estrellas)
        ui.escribir(pantalla, "SPACE WAZE", "titulo", ui.COLORES["azul"], [centro, 120])
        ui.escribir(
            pantalla, "Equipo Nova", "normal", ui.COLORES["suave"], [centro, 180]
        )
        ui.dibujar_centrado(pantalla, ui.IMAGENES["nave"], centro, 235)
        for boton in botones:
            ui.dibujar_boton(pantalla, boton)
        pygame.display.flip()


# ---------------- Paso 13: partida local contra el CPU ----------------
def jugar_local(pantalla, reloj, estrellas):
    """Partida contra el CPU. Devuelve "otra" (R) o "menu" (ESC)."""
    estado = gl.crear_estado()
    gl.colocar_nave(estado, 2, gl.elegir_posicion_cpu())  # el CPU esconde su nave
    turno = ui.crear_turno()  # selección, mensaje y temporizador del jugador
    efectos = []  # animaciones en pantalla
    disparos_vistos = 0  # cuántos disparos ya se animaron

    while True:
        # a) Tiempo y vista
        dt = reloj.tick(ui.FPS) / 1000
        vista = gl.vista_para(estado, 1)
        listo = ui.turno_listo(turno, vista)

        # b) Eventos del jugador
        for evento in pygame.event.get():
            ui.revisar_cierre(evento)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"

            if vista["fase"] == "fin":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    return "otra"

            elif vista["fase"] == "colocar":
                if ui.es_confirmar(evento):
                    if turno["seleccion"] == 0:
                        ui.avisar(turno, "Primero elige una posición")
                    else:
                        gl.colocar_nave(estado, 1, turno["seleccion"])
                else:
                    eleccion = ui.leer_eleccion(
                        evento, ui.ZONA_PROPIA, turno["seleccion"]
                    )
                    if eleccion != "":
                        ui.aplicar_validacion(
                            turno, gl.validar_posicion(eleccion), eleccion
                        )

            elif vista["mi_turno"] and listo:
                if ui.es_confirmar(evento):
                    if turno["seleccion"] == 0:
                        ui.avisar(turno, "Primero elige una columna")
                    else:
                        gl.procesar_disparo(estado, 1, turno["seleccion"])
                else:
                    eleccion = ui.leer_eleccion(
                        evento, ui.ZONA_RIVAL, turno["seleccion"]
                    )
                    if eleccion != "":
                        ui.aplicar_validacion(
                            turno, gl.validar_disparo(estado, 1, eleccion), eleccion
                        )

        # c) Animar el disparo nuevo
        vista = gl.vista_para(estado, 1)
        if vista["total_disparos"] > disparos_vistos:
            disparos_vistos = vista["total_disparos"]
            ui.lanzar_disparo(efectos, vista)
        efectos = ui.actualizar_efectos(efectos, dt)
        ui.mover_estrellas(estrellas, dt)

        # d) Empezar un turno nuevo (solo cuando terminaron las animaciones)
        if efectos == [] and not ui.turno_listo(turno, vista):
            ui.reiniciar_turno(turno, vista)
        listo = ui.turno_listo(turno, vista)
        transcurrido = ui.ms_transcurridos(turno)

        # e) Se acabó tu tiempo: dispara la última columna elegida (0 = pierde el turno)
        if vista["mi_turno"] and listo and gl.turno_terminado(transcurrido):
            gl.procesar_disparo(estado, 1, turno["seleccion"])
        # f) Turno del CPU
        elif (
            vista["fase"] == "disparo"
            and not vista["mi_turno"]
            and listo
            and transcurrido >= ESPERA_CPU
        ):
            gl.procesar_disparo(estado, 2, gl.elegir_disparo_cpu(estado, 2))

        # g) Dibujar
        vista = gl.vista_para(estado, 1)
        segundos = -1
        if vista["mi_turno"] and ui.turno_listo(turno, vista):
            segundos = gl.tiempo_restante(ui.ms_transcurridos(turno))
        ui.dibujar_estrellas(pantalla, estrellas)
        ui.dibujar_partida(pantalla, vista, turno, segundos, efectos, AYUDA, TEXTO_FIN)
        pygame.display.flip()


# ---------------- Paso 14: main ----------------
def main():
    pantalla = ui.iniciar_ventana()
    reloj = pygame.time.Clock()
    estrellas = ui.crear_estrellas(110)
    jugando = True
    while jugando:
        opcion = menu_principal(pantalla, reloj, estrellas)
        if opcion == "local":
            resultado = "otra"
            while resultado == "otra":
                resultado = jugar_local(pantalla, reloj, estrellas)
        elif opcion == "servidor":
            pass  # cuando Jhair termine: server.ejecutar(pantalla, reloj, estrellas)
        elif opcion == "cliente":
            pass  # cuando Jhair termine: client.ejecutar(pantalla, reloj, estrellas)
        else:
            jugando = False
    pygame.quit()


if __name__ == "__main__":
    main()
