
import random
from collections import Counter

# ==================================================
# PROYECTO: YAHTZEE PARA DOS JUGADORES CON MONTECARLO
# ==================================================

# Lista de las 13 categorias donde se pueden anotar puntos
CATEGORIAS = [
    "Unos", "Doses", "Treses", "Cuatros", "Cincos", "Seises",
    "Tres iguales", "Cuatro iguales", "Full house",
    "Escalera pequena", "Escalera grande", "Yahtzee", "Azar"
]


# ==================================================
# FUNCION PARA LANZAR LOS CINCO DADOS
# ==================================================

def lanzar_dados():
    # Genera cinco numeros aleatorios entre 1 y 6
    # Cada numero representa el resultado de un dado
    return [random.randint(1, 6) for _ in range(5)]


# ==================================================
# FUNCION PARA MOSTRAR LOS DADOS
# ==================================================

def mostrar_dados(dados):
    # Muestra en pantalla los valores de los cinco dados
    print("Dados:", dados)


# ==================================================
# FUNCION PARA CALCULAR LOS PUNTOS DE UNA CATEGORIA
# ==================================================

def calcular_puntos(dados, categoria):
    # Cuenta cuantas veces aparece cada numero
    conteo = Counter(dados)

    # Suma el valor de los cinco dados
    total = sum(dados)

    # Guarda los numeros diferentes que salieron
    valores = set(dados)

    # Ordena las cantidades de veces que aparece cada numero
    frecuencias = sorted(conteo.values())

    # Si la categoria es de Unos, Doses, Treses, etc.
    if categoria in CATEGORIAS[:6]:
        # Obtiene el numero correspondiente a la categoria
        numero = CATEGORIAS.index(categoria) + 1

        # Suma el valor de los dados que tengan ese numero
        return dados.count(numero) * numero

    # Tres iguales: al menos tres dados deben tener el mismo numero
    if categoria == "Tres iguales":
        if max(conteo.values()) >= 3:
            return total
        return 0

    # Cuatro iguales: al menos cuatro dados deben tener el mismo numero
    if categoria == "Cuatro iguales":
        if max(conteo.values()) >= 4:
            return total
        return 0

    # Full house: tres dados iguales y otros dos iguales
    if categoria == "Full house":
        if frecuencias == [2, 3]:
            return 25
        return 0

    # Escalera pequena: debe existir una secuencia de cuatro numeros
    if categoria == "Escalera pequena":
        escaleras = [
            {1, 2, 3, 4},
            {2, 3, 4, 5},
            {3, 4, 5, 6}
        ]

        # Comprueba si los dados contienen alguna escalera pequena
        for escalera in escaleras:
            if escalera.issubset(valores):
                return 30

        return 0

    # Escalera grande: cinco numeros consecutivos sin repetir
    if categoria == "Escalera grande":
        if valores in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
            return 40
        return 0

    # Yahtzee: los cinco dados deben mostrar el mismo numero
    if categoria == "Yahtzee":
        if max(conteo.values()) == 5:
            return 50
        return 0

    # Azar: se suman todos los dados, sin exigir una combinacion
    if categoria == "Azar":
        return total

    # Si no se reconoce la categoria, no se asignan puntos
    return 0


# ==================================================
# FUNCION PARA JUGAR EL TURNO DE UN JUGADOR
# ==================================================

def jugar_turno(nombre, puntuaciones):
    # Informa a quien le corresponde jugar
    print("\n--------------------------------")
    print("Turno de", nombre)
    print("--------------------------------")

    # El jugador empieza con cinco dados aleatorios
    dados = lanzar_dados()

    # Permite un maximo de tres lanzamientos por turno
    for intento in range(3):
        print("\nLanzamiento", intento + 1)
        mostrar_dados(dados)

        # En el tercer lanzamiento ya no se pueden relanzar dados
        if intento == 2:
            break

        # Pregunta cuales dados quiere volver a lanzar
        respuesta = input(
            "Escribe las posiciones de los dados que quieres relanzar "
            "(1-5), separadas por espacios, o pulsa Enter para conservarlos: "
        )

        # Si el jugador pulsa Enter, conserva todos los dados
        if respuesta.strip() == "":
            break

        try:
            # Convierte las posiciones escritas en numeros
            posiciones = [int(x) for x in respuesta.split()]

            # Comprueba que las posiciones esten entre 1 y 5
            if any(p < 1 or p > 5 for p in posiciones):
                print("Las posiciones deben estar entre 1 y 5.")
                continue

            # Evita que se escriba dos veces la misma posicion
            if len(set(posiciones)) != len(posiciones):
                print("No repitas una posicion.")
                continue

        except ValueError:
            # Informa si se escriben letras u otros valores incorrectos
            print("Escribe numeros separados por espacios.")
            continue

        # Vuelve a lanzar solamente los dados seleccionados
        for posicion in posiciones:
            dados[posicion - 1] = random.randint(1, 6)

    # Muestra los dados definitivos del turno
    print("\nCombinacion final:")
    mostrar_dados(dados)

    # Busca las categorias que el jugador aun no ha utilizado
    disponibles = [
        categoria for categoria in CATEGORIAS
        if categoria not in puntuaciones
    ]

    # Muestra las categorias disponibles con un numero
    print("\nCategorias disponibles:")
    for i, categoria in enumerate(disponibles, start=1):
        print(i, "-", categoria)

    # Solicita al jugador que elija una categoria valida
    while True:
        try:
            opcion = int(input("Selecciona una categoria: "))

            if 1 <= opcion <= len(disponibles):
                categoria = disponibles[opcion - 1]
                break

            print("Selecciona una opcion de la lista.")

        except ValueError:
            print("Debes escribir un numero.")

    # Calcula los puntos de la combinacion seleccionada
    puntos = calcular_puntos(dados, categoria)

    # Guarda la categoria y sus puntos para ese jugador
    puntuaciones[categoria] = puntos

    # Informa el resultado del turno
    print("\nCategoria elegida:", categoria)
    print("Puntos obtenidos:", puntos)


# ==================================================
# FUNCION PARA CALCULAR LA PUNTUACION TOTAL
# ==================================================

def calcular_total(puntuaciones):
    # Suma los puntos anotados en todas las categorias
    total = sum(puntuaciones.values())

    # Las primeras seis categorias forman la seccion superior
    categorias_superiores = CATEGORIAS[:6]

    # Suma los puntos obtenidos en esa seccion
    puntos_superiores = sum(
        puntuaciones.get(categoria, 0)
        for categoria in categorias_superiores
    )

    # Agrega 35 puntos de bono si se alcanzan al menos 63
    if puntos_superiores >= 63:
        total += 35

    # Devuelve la puntuacion final del jugador
    return total


# ==================================================
# FUNCION PRINCIPAL DEL JUEGO YAHTZEE
# ==================================================

def jugar_yahtzee():
    # Cada jugador tiene su propio registro de puntuaciones
    jugadores = {
        "Jugador 1": {},
        "Jugador 2": {}
    }

    print("\n================================")
    print("   YAHTZEE PARA DOS JUGADORES")
    print("================================")

    # Hay 13 categorias, por lo tanto cada jugador tiene 13 turnos
    for ronda in range(3):
        print("\n========== RONDA", ronda + 1, "==========")

        # En cada ronda juega primero el Jugador 1 y luego el Jugador 2
        for nombre in jugadores:
            input(
                "\nTurno de " + nombre +
                ". Pulsa Enter para comenzar."
            )

            # Ejecuta el turno del jugador actual
            jugar_turno(nombre, jugadores[nombre])

    # Cuando terminan las 13 rondas, muestra los resultados finales
    print("\n========== RESULTADOS FINALES ==========")

    # Guarda los puntos finales de ambos jugadores
    resultados = {}

    for nombre, puntuaciones in jugadores.items():
        print("\n", nombre)

        # Muestra los puntos de cada categoria
        for categoria in CATEGORIAS:
            puntos = puntuaciones.get(categoria, 0)
            print(categoria, ":", puntos)

        # Calcula el total incluyendo el posible bono
        total = calcular_total(puntuaciones)
        resultados[nombre] = total

        print("Total final:", total)

    # Compara las puntuaciones para anunciar al ganador
    if resultados["Jugador 1"] > resultados["Jugador 2"]:
        print("\n¡Gana el Jugador 1!")

    elif resultados["Jugador 2"] > resultados["Jugador 1"]:
        print("\n¡Gana el Jugador 2!")

    else:
        print("\n¡La partida termina en empate!")


# ==================================================
# SIMULADOR DE MONTECARLO
# ==================================================

def simulacion_montecarlo():
    # Explica que se estudiaran lanzamientos aleatorios
    print("\n================================")
    print(" SIMULACION DE MONTECARLO")
    print("================================")

    # Cada experimento consiste en lanzar cinco dados una vez
    print("Se simulan lanzamientos iniciales de cinco dados.")

    # Solicita la cantidad de experimentos
    while True:
        try:
            cantidad = int(
                input("Cuantos lanzamientos deseas simular? ")
            )

            # La cantidad debe ser mayor que cero
            if cantidad > 0:
                break

            print("Escribe un numero mayor que cero.")

        except ValueError:
            print("Debes escribir un numero entero.")

    # Guarda cuantas veces aparece cada cara del dado
    caras = [0] * 6

    # Guarda cuantas veces aparece cada combinacion
    combinaciones = {
        "Tres iguales o mas": 0,
        "Cuatro iguales o mas": 0,
        "Full house": 0,
        "Escalera pequena": 0,
        "Escalera grande": 0,
        "Yahtzee": 0
    }

    # Secuencias que cuentan como escalera pequena
    escaleras_pequenas = [
        {1, 2, 3, 4},
        {2, 3, 4, 5},
        {3, 4, 5, 6}
    ]

    # Repite el experimento la cantidad de veces solicitada
    for i in range(cantidad):
        # Lanza cinco dados
        dados = lanzar_dados()

        # Cuenta cada cara de los cinco dados
        for dado in dados:
            caras[dado - 1] += 1

        # Cuenta las repeticiones de cada valor
        conteo = Counter(dados)

        # Ordena las cantidades de repeticiones
        frecuencias = sorted(conteo.values())

        # Obtiene los valores diferentes de los dados
        valores = set(dados)

        # Cuenta si hay tres dados iguales o mas
        if max(conteo.values()) >= 3:
            combinaciones["Tres iguales o mas"] += 1

        # Cuenta si hay cuatro dados iguales o mas
        if max(conteo.values()) >= 4:
            combinaciones["Cuatro iguales o mas"] += 1

        # Cuenta si hay tres dados iguales y dos iguales
        if frecuencias == [2, 3]:
            combinaciones["Full house"] += 1

        # Cuenta si hay cuatro numeros consecutivos
        if any(
            escalera.issubset(valores)
            for escalera in escaleras_pequenas
        ):
            combinaciones["Escalera pequena"] += 1

        # Cuenta si hay cinco numeros consecutivos distintos
        if valores in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
            combinaciones["Escalera grande"] += 1

        # Cuenta si los cinco dados son iguales
        if max(conteo.values()) == 5:
            combinaciones["Yahtzee"] += 1

    # Muestra los resultados de las seis caras
    print("\n--- RESULTADOS DE LAS CARAS ---")

    # En cada experimento se lanzan cinco dados
    total_dados = cantidad * 5

    for numero in range(1, 7):
        # Obtiene cuantas veces aparecio la cara
        frecuencia = caras[numero - 1]

        # Calcula su probabilidad experimental en porcentaje
        porcentaje = frecuencia / total_dados * 100

        # Muestra la frecuencia experimental y la teorica
        print(
            "Cara", numero,
            "| Apariciones:", frecuencia,
            "| Probabilidad experimental:", round(porcentaje, 2), "%",
            "| Probabilidad teorica: 16.67%"
        )

    # Muestra las frecuencias de las combinaciones
    print("\n--- RESULTADOS DE LAS COMBINACIONES ---")

    for nombre, veces in combinaciones.items():
        # Divide las apariciones entre el numero de experimentos
        porcentaje = veces / cantidad * 100

        print(
            nombre,
            "| Veces:", veces,
            "| Probabilidad experimental:", round(porcentaje, 4), "%"
        )

    # Explica que representan los resultados
    print("\n--- CONCLUSION DE MONTECARLO ---")
    print("Los resultados experimentales pueden variar en cada ejecucion.")
    print("Con mas experimentos, suelen acercarse a la probabilidad teorica.")
    print("Esto permite observar la Ley de los Grandes Numeros.")


# ==================================================
# MENU PRINCIPAL DEL PROGRAMA
# ==================================================

def main():
    # Mantiene el menu abierto hasta que el usuario decida salir
    while True:
        print("\n================================")
        print("       PROYECTO YAHTZEE")
        print("================================")

        # Opcion para jugar una partida entre dos jugadores
        print("1. Jugar Yahtzee para dos jugadores")

        # Opcion para estudiar probabilidades mediante Montecarlo
        print("2. Simulacion de Montecarlo")

        # Opcion para cerrar el programa
        print("3. Salir")

        # Lee la opcion que selecciona el usuario
        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            # Inicia el juego
            jugar_yahtzee()

        elif opcion == "2":
            # Inicia la simulacion estadistica
            simulacion_montecarlo()

        elif opcion == "3":
            # Finaliza el programa
            print("Gracias por utilizar el programa.")
            break

        else:
            # Informa si se selecciona una opcion incorrecta
            print("Opcion no valida. Intenta nuevamente.")


# ==================================================
# PUNTO DE INICIO DEL PROGRAMA
# ==================================================

# Ejecuta el menu solo cuando se abre directamente este archivo
if __name__ == "__main__":
    main()
