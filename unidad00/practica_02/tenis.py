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
            fecha = datetime.strptime(tenista[0], '%d/%m/%Y').date()
            rival = tenista[1]
            superficie = tenista[2]
            duracion = int(tenista[3])
            juegos_ganados = int(tenista[4])
            juegos_perdidos = int(tenista[5])
            ganado = bool(tenista[6])
            tupla = Tenista(fecha, rival, superficie, duracion, juegos_ganados, juegos_perdidos, ganado)
            registros.append(tupla)
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
#def desviaciones_media(partidos: list, n: int):

#    def partidos_validos(a):
#        if a >= media_mas_minutos:
#            return True
#        else:
#            return False
        
#    lista = []
#    media_partidos = sum(partidos.duracion) / len(partidos)
#    media_mas_minutos = media_partidos + n

#    partidos_desviados = filter(partidos_validos, partidos)
#    dato_partido_desviado = filter(partidos_validos, partidos.rival)

def desviaciones_media(partidos: list, n: int):
    # 1. Calcular la media extrayendo la duración de cada partido
    media = sum(partidos.duracion for partidos.duracion in partidos) / len(partidos)
        
    # 2. Obtener la desviación de cada partido
    desviaciones = map(lambda p: p.duracion - media, partidos)
        
    # 3. Emparejar con zip() cada desviación con su partido original
    parejas = zip(desviaciones, partidos)
        
    # 4. Filtrar solo las parejas cuya desviación sea >= n
    resultado = filter(lambda par: par[0] >= n, parejas)
        
    # Devolverlo en forma de lista
    return list(resultado)

'''
Ejercicio 2
Implementa diccionario_diferencia_juegos_superficie(partidos, n=3). Debe devolver un
diccionario que relacione cada superficie con las fechas de los n partidos jugados en esa
superficie con mayor diferencia entre juegos ganados y juegos perdidos, ordenados de mayor a
menor diferencia. Utiliza al menos una función auxiliar.
Ejemplo de interpretación
Para una superficie, los partidos con diferencias 8, 6 y 3 deben aparecer antes que uno con
diferencia 1
'''