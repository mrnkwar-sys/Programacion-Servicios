import csv
from collections import namedtuple
from datetime import datetime

Tenista = namedtuple('Tenista', 'fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado')

def leer_datos(nombre_fichero):
    registros = []
    with open(nombre_fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for tenista in lector:
            fecha = datetime.strptime(tenista[0], '%dd/%mm/%Y').date()
            rival = tenista[1]
            superficie = tenista[2]
            duracion = int(tenista[3])
            juegos_ganados = int(tenista[4])
            juegos_perdidos = int(tenista[5])
            ganado = bool(tenista[6])
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