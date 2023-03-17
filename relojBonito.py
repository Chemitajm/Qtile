import datetime
import os

def relojito_bonito():
    while True:
        # Obtenemos la hora actual
        ahora = datetime.datetime.now()
        hora = ahora.hour
        minutos = ahora.minute
        segundos = ahora.second

        # Creamos una lista con los valores de cada posición
        valores = [32, 16, 8, 4, 2, 1]

        # Creamos la matriz a partir de la hora actual
        matriz = []
        for num in [hora, minutos, segundos]:
            fila = []
            for valor in valores:
                if num >= valor:
                    fila.append('1')
                    num -= valor
                else:
                    fila.append('0')
            matriz.append(fila)

        # Limpiamos la pantalla y mostramos la matriz
        os.system('cls' if os.name == 'nt' else 'clear')
        for fila in matriz:
            print(fila)

relojito_bonito()
