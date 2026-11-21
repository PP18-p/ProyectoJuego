# DF2_validacion.rap: DF2: RF-06, RF-07, RF-09 y RF-04
# game_logic.py . Space Waze
# Estado de ejemplo (Igual que en Raptor)

turno = 1
nave_j1 = 2
nave_j2 = 4
eleccion = 0
entrada = -1

# RF-04: muestra de quién es el turno y el tiempo
print(
    f"Turno del Jugador {turno}: tienes 10 segundos. Elige un espacio del 1 al 5 (0 = se acabó el tiempo)."
)

# RF-06: el jugador puede cambiar su elección mientras hay tiempo
# RF-07: se ignoran los valores inválidos (por formato y fuera de rango)
# Escribir 0 = se acabó el tiempo y termina el bucle

while entrada != 0:
    texto = input(f"Jugador {turno}, elige un espacio: ")

    # RF-07: validación por formato (letras, decimales o vacío no son válidos)
    if texto.isdigit():
        entrada = int(texto)
    else:
        entrada = -1

    # RF-06, RF-07: validación por las reglas (solo espacios del 1 al 5)
    if entrada >= 1 and entrada <= 5:
        eleccion = entrada
        print(f"Objetivo: espacio {eleccion}")
    elif entrada != 0:
        print("Elige un espacio del 1 al 5")

# RF-09: si no eligió ningún espacio válido, se acabó el tiempo y pierde el turno
if eleccion == 0:
    print("Tiempo agotado: pierdes el turno.")
else:
    print(f"Disparo del Jugador {turno} al espacio {eleccion}")
