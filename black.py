import random
from time import sleep

MINIMO = 10
MAXIMO = 100000
JUGANDO = True

palos = ['♥', '♦', '♠', '♣']
cartas = ['2', '3', '4', '5',
          '6', '7', '8', '9',
          '10', 'J', 'Q', 'K', 'A']
valores = {'2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8,
           '9': 9, '10': 10, 'J': 10,
           'Q': 10, 'K': 10, 'A': 11}


# Clase Cartas, donde creamos cada una de las cartas
class Cartas:

    # __init__ crea cada dato como una estructura
    def __init__(self, palo, carta):
        self.palo = palo
        self.carta = carta

    # __str__ Con ella modificamos el nombre del patron de bits,
    # por informacion visible para el usuario
    def __str__(self):
        return self.carta + ' ' + self.palo


# Clase Mazo, donde vamos a crear el mazo completo con todas las cartas
class Mazo:

    def __init__(self):
        self.mazo = []  # Estructura pila para ir creando el mazo,
        # y meter objeto carta adentro de cada posicion
        for palo in palos:
            for carta in cartas:
                self.mazo.append(Cartas(palo, carta))

    # Con esta funcion vamos a transformar el objeto en un string, que se pueda mostrar por pantalla
    def __str__(self):
        armado_mazo = ''
        for carta in self.mazo:
            armado_mazo += '\n ' + carta.__str__()
        return 'Mazo: ' + armado_mazo

    # Con random.shuffle vamos a mezclar el mazo completo
    def shuffle(self):
        random.shuffle(self.mazo)

    # Con pop vamos a retirar una carta del mazo y asi evitar dar cartas repetidas
    # quitando posiciones de la lista
    def repartir_cartas(self):
        carta_sacada = self.mazo.pop()
        return carta_sacada


# Clase Mano, Dentro de ella se van a ir insertando en la estructura pila
# de cada MANO del jugador o de la mesa,
# cada una de las cartas
class Mano:

    def __init__(self):
        self.vCartas = []
        self.numCarta = 0
        self.ases = 0

    # Con esta funcion, cargaremos en cada mano una carta del mazo
    # y sumamos los valores de cada una para el puntaje
    def agregar_cartas_a_la_mano(self, carta_mano):
        self.vCartas.append(carta_mano)
        self.numCarta += valores[carta_mano.carta]
        if carta_mano.carta == 'A':
            self.ases += 1

    def as_puntuacion_alta(self):
        for i in range(self.ases):
            if self.numCarta + 10 <= 21:
                self.numCarta += 10
    # def as_puntuacion_alta(self):
    #    while self.numCarta > 21 and self.ases > 1:
    #        self.numCarta -= 10
    #        self.ases -= 1


# Clase Apuesta, donde vamos a usarla para apostar al inicio del juego
class Apuesta:

    def __init__(self):
        self.unidad_apuesta = 0
        self.apuesta_mesa = random.randint(MINIMO, MAXIMO)


# Funcion donde vamos a preguntarle al usuario cuanto quiere
# apostar antes de comenzar el juego
def pedir_apuesta_jugador(apuesta_jugador, billetera):
    while True:
        try:
            apuesta_jugador.unidad_apuesta = int(input("Cuantas monedas quiere apostar? "
                                                       f"\nLe quedan disponible {billetera} -> "))
        except ValueError:
            print("Debe ingresar un numero...")
        else:
            if apuesta_jugador.unidad_apuesta < 0 or apuesta_jugador.unidad_apuesta > billetera:
                print("Apuesta no valida")
            else:
                break
    print(f"Mesa apuesta ${apuesta.apuesta_mesa}")


def agregar_carta_a_la_mano_del_jugador(mazo_de_cartas, mano_con_cartas):
    mano_con_cartas.agregar_cartas_a_la_mano(mazo_de_cartas.repartir_cartas())
    mano_con_cartas.as_puntuacion_alta()


# Funcion en la que vamos a determinar si le damos al jugar una carta o terminamos la jugada,
# para darle paso a la mesa que juegue
def accion_del_jugador(mazo_de_cartas, mano_con_cartas):
    global JUGANDO

    while True:
        opcion = input("Pedir o quedarse: ")

        if opcion.lower().replace(" ", "") == "pedir":
            agregar_carta_a_la_mano_del_jugador(
                mazo_de_cartas, mano_con_cartas)
        elif opcion.lower().replace(" ", "") == "quedarse":
            print("Mesa jugando")
            JUGANDO = False
        else:
            print("Palabra no admitida")
            continue
        break


# Funcion para mostrar en consola las cartas de cada uno de los jugadores
# que se vayan sacando en cada mano
def mostrar_mano_partida(jugador, mesa, nombre):
    print("\nCartas de la mesa:\n"
          "<Carta boca abajo> "
          "", mesa.vCartas[1],
          f"Cartas del jugador {nombre}:", *jugador.vCartas, sep='\n ')
    print(f"Puntos del jugador {nombre} = {jugador.numCarta}")


# Funcion donde se mostrará al finalizar la partida,
# todas las cartas dadas y sus puntuaciones
def mostrar_mano_final(jugador, mesa, nombre):
    print("\nCartas de la mesa: ", *mesa.vCartas, sep='\n ')
    print(f"Puntos de la mesa = {mesa.numCarta}")
    print(f"Cartas del jugador {nombre}:", *jugador.vCartas, sep='\n ')
    print(f"Puntos del jugador {nombre} = {jugador.numCarta}")


# Funcion para determinar a los ganadores, o si hay empate
def resultado(jugador, mesa, nombre):
    resultado_partida = 0
    if jugador.numCarta <= 21 and mesa.numCarta <= 21:
        if jugador.numCarta == mesa.numCarta:
            print("Empate")
        elif jugador.numCarta < mesa.numCarta:
            print("Mesa gana"
                  f"\njugador {nombre} pierde...")
            resultado_partida = 1
        else:
            print(f"Gana jugador {nombre}"
                  "\nMesa pierde")
            resultado_partida = 0
    elif jugador.numCarta > 21:
        print(f"Jugador {nombre} de pasa de 21"
              f"\nGana mesa")
        resultado_partida = 1
    else:
        print("Mesa de pasa de 21"
              f"\nGana jugador {nombre}")
        resultado_partida = 0
    return resultado_partida


def cargando_juego():
    for i in range(6):
        print(".", end="")
        sleep(random.random())


# Main del juego
resultado_partida = 0
vueltas_partidas = 0
print("Inicializando juego")
cargando_juego()
while True:
    JUGANDO = True

    if vueltas_partidas == 0:
        print("\nJuego de cartas - BlackJack - ")
        nombre_jugador = input("Cómo te llamas?? ").title().strip()
        while True:
            try:
                billetera = int(
                    input("Dinero que tiene disponible en la billetera? "))
            except ValueError:
                print("Debe ingresar un numero...")
            else:
                if billetera < 1:
                    print("Apuesta no valida")
                else:
                    break

    # Creamos el objeto Mazo y luego mezclamos
    mazo = Mazo()
    mazo.shuffle()

    mano_jugador = Mano()
    mano_jugador.agregar_cartas_a_la_mano(mazo.repartir_cartas())
    mano_jugador.agregar_cartas_a_la_mano(mazo.repartir_cartas())

    mano_mesa = Mano()
    mano_mesa.agregar_cartas_a_la_mano(mazo.repartir_cartas())
    mano_mesa.agregar_cartas_a_la_mano(mazo.repartir_cartas())

    # Creamos el objeto "apuesta" para el jugador y pedimos un valor
    print(f"Dinero en la cuenta {billetera}")
    apuesta = Apuesta()
    pedir_apuesta_jugador(apuesta, billetera)

    while JUGANDO:

        if mano_jugador.numCarta == 21:
            # if si en una partida se obtiene 21 en la primera mano, termine el juego
            mostrar_mano_partida(mano_jugador, mano_mesa, nombre_jugador)
            print(f"Jugador {nombre_jugador} obtiene Blackjack")
            billetera = billetera + apuesta.unidad_apuesta
            break
        elif mano_jugador.numCarta > 21:
            # if si en una partida se obtiene mas 21, termine el juego
            mostrar_mano_partida(mano_jugador, mano_mesa, nombre_jugador)
            resultado_partida = resultado(
                mano_jugador, mano_mesa, nombre_jugador)
            billetera = billetera - apuesta.unidad_apuesta
            break
        mostrar_mano_partida(mano_jugador, mano_mesa, nombre_jugador)
        accion_del_jugador(mazo, mano_jugador)

    if mano_jugador.numCarta < 21:
        while mano_mesa.numCarta < 17:
            # If para que mesa pueda sacar cartas hasta una cierta puntuacion,
            # en este caso si tiene menos de 17 puntos va a seguir sacando cartas
            agregar_carta_a_la_mano_del_jugador(mazo, mano_mesa)

        mostrar_mano_final(mano_jugador, mano_mesa, nombre_jugador)
        resultado_partida = resultado(mano_jugador, mano_mesa, nombre_jugador)

    if resultado_partida == 1:
        billetera = billetera - apuesta.unidad_apuesta
    elif resultado_partida == 0:
        billetera = billetera + apuesta.unidad_apuesta

    if billetera < 1:
        billetera = 0
        print(f"Tu billetera quedo en {billetera}"
              "\nEstas en bancarrota, suerte la proxima"
              "\nJuego comenzando nuevamente\n")
        cargando_juego()
        JUGANDO = False
        continue
    # Preguntamos si el jugador quiere volver a jugar, dandole nuevas cartas
    repetir_juego = input("\nJugar nuevamente? (si/no) ")
    if repetir_juego.lower().replace(" ", "") == "si":
        opcion_jugador = input(
            "Mismo jugador? si/no ").lower().replace(" ", "")
        if opcion_jugador == "si":
            vueltas_partidas = 1
            continue
        else:
            print("Se le pedira el nombre del nuevo jugador\n")
            vueltas_partidas = 0
            continue
    else:
        print("Saliendo",end="")
        cargando_juego()
        exit()
