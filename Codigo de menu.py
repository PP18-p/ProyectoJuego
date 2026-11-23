# RF-01: menú principal con los modos de juego
menu = (
    "SPACE WAZE\n"
    "1. Modo local (contra el CPU)\n"
    "2. Modo multijugador (red LAN)\n"
    "3. Salir\n"
    "Elige una opción: "
)

opcion = 0

while opcion != 3:
    texto = input(menu)

    while texto not in ("1", "2", "3"):
        print("Opción inválida. Elige 1, 2 o 3.")
        texto = input(menu)
    opcion = int(texto)

    if opcion == 1:

        print("Modo local: juegas contra el CPU en esta PC.")
        print("La partida se programa en la Fase 4.")
    elif opcion == 2:

        print(
            "Modo multijugador en red LAN: el Jugador 1 crea la partida "
            "(servidor) y el Jugador 2 se une desde otra PC (cliente)."
        )
        print(
            "Servidor: IP 192.168.56.10, puerto 5000, conexión TCP."
        )  # La siguiente Ip es de ejemplo para poder realizar la ejecución del juego en red LAN, se puede cambiar por la IP de la máquina que haga de servidor..
        print("La conexión se programa en la Fase 4.")


print("Gracias por jugar Space Waze.")
