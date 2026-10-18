import csv
from collections import namedtuple
from datetime import datetime

'''
fecha, rival, superficie, duracion,juegos_ganados, juegos_perdidos, ganado
11/10/2020,Novak Djokovic,Tierra,160,19,7,True
'''

Partidos = namedtuple('Partidos', 'fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado')

def leer_fichero(nombre_fichero):
    registros = []
    with open(nombre_fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for partido in registros:
            fecha = datetime.strptime(partido[0], '%d/%m/%Y').date()
            rival = partido[1]
            superficie = partido[2]
            duracion = int(partido[3])
            juegos_ganados = int(partido[4])
            juegos_perdidos = int(partido[5])
            ganado = bool(partido[6])
            tupla_datos = Partidos(fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado)
            registros.append(tupla_datos)
    return registros

'''
Ejercicio 1
Implementa desviaciones_media(partidos, n). Debe devolver una lista de tuplas (desviacion,
partido) con los partidos cuya duración supere en n o más minutos la duración media de todos
los partidos. No se pueden usar bucles explícitos.
Ejemplo de interpretación
Si la duración media es 120 minutos y un partido dura 150, su desviación es 30. Para n=20 ese
partido debe aparecer en el resultado.
'''
def desviaciones_media(partidos, n):
    lista_partidos = []
    duracion_media = sum()