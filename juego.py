# juego.py · Space Waze
# Traduce DF1 Partida completa (solo el menú) · RF-01, RF-02, RF-10

# RF-01: menú principal con los modos de juego
menu = (
    "SPACE WAZE\n"
    "1. Modo local (contra el CPU)\n"
    "2. Modo multijugador (red LAN)\n"
    "3. Salir\n"
    "Elige una opción: "
)

opcion = 0

# El menú se repite hasta elegir «3. Salir»
while opcion != 3:
    texto = input(menu)

    # Validación de la opción: se vuelve a pedir mientras no sea 1, 2 o 3
    while texto not in ("1", "2", "3"):
        print("Opción inválida. Elige 1, 2 o 3.")
        texto = input(menu)
    opcion = int(texto)

    # RF-01, RF-10: modo local contra el CPU
    if opcion == 1:
        print("Modo local: juegas contra el CPU en esta PC.")
        print("La partida se programa en la Fase 4.")

    # RF-01, RF-02: modo multijugador en red LAN (Jugador 1 = servidor, Jugador 2 = cliente)
    elif opcion == 2:
        print(
            "Modo multijugador en red LAN: el Jugador 1 crea la partida "
            "(servidor) y el Jugador 2 se une desde otra PC (cliente)."
        )
        # IP de ejemplo: se cambia por la IP de la PC que haga de servidor
        print("Servidor: IP 192.168.56.10, puerto 5000, conexión TCP.")
        print("La conexión se programa en la Fase 4.")

print("Gracias por jugar Space Waze.")