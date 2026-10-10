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
def diccionario_diferencia_juegos_superficie(partidos, n=3):
    d1 = {}
    d2 = {}
    for p in partidos:
        #Las claves del d1 seran las superficies del registro
        clave = p.superficie

        #Si la clave ya se anadio al d1 en la iteracion anterior con su respectivo partido, le anadimos el de esta iteracion
        #Se anade como un elemento de lista (fijate en los corchetes de p)
        if clave in d1:
            d1[clave] += [p]
        #Si no fue asi, anadimos un nuevo par clave-valor
        else:
            d1[clave] = [p]

    #Recorremos cada clave del d1
    for clave in d1:
        #Le damos las mismas claves al d2 y, como valor, le damos el retorno de la funcion auxiliar
        d2[clave] = auxiliar(d1[clave], n)
    return d2

def auxiliar(lista, n):
    #Creamos una lista ordenada de mayor a menor siendo el criterio de ordenacion la diferencia entre ganados y perdidos
    lista_ordenada = sorted(lista, reverse=True, key=lambda t:t.juegos_ganados - t.juegos_perdidos)
    #Creamos otra lista que solo contenga los partidos solicitados en la funcion principal
    lista_ordenada_sub = lista_ordenada[:n]
    #Devolvemos la fecha de cada partido de la sublista ordenada
    return [r.fecha for r in lista_ordenada_sub]

'''
Ejercicio 3
Implementa rival_mayor_porcentaje_victorias(partidos, superficie). Debe devolver una tupla
(rival, porcentaje) con el rival frente al que se haya obtenido el mayor porcentaje de victorias en
la superficie indicada.
Ejemplo de interpretación
Si frente a un rival se han ganado 7 de 10 partidos en tierra, su porcentaje de victorias es 70.0.
'''
def rival_mayor_porcentaje_victorias(partidos, superficie):
    d1 = {}
    d2 = {}
    d3 = {}

    for p in partidos:
        #Revisamos que la superficie de la iteracion coincida con la introducida en la funcion
        if superficie == p.superficie:

            #Las claves del diccionario seran los nombres de cada rival
            clave = p.rival

            #Si el rival ya esta "registrado", anadimos 1 a la cantidad de partidos (valor) jugados contra ese rival
            #Si el rival no estaba ya en el diccionario, establecemos la cantidad de partidos a 1
            if clave in d1:
                d1[clave] += 1
            else:
                d1[clave] = 1

    for p in partidos:
        #Comprobamos ahora no solo que la superficie coincido, sino tambien que se trate de un partido ganado
        if superficie == p.superficie and p.ganado == True:
            clave = p.rival

            #Si ya se habia guardado un partido ganado contra ese rival antes, se le suma 1 a ese valor
            #Si no, se establece a 1
            if clave in d1:
                d1[clave] += 1
            else:
                d1[clave] = 1

    for clave in d1:
        #Calculamos el porcentaje de partidos ganados contra cada rival guardado
        d3[clave] = 100*(d2[clave]/d1[clave])

    #d3.items genera una lista de tuplas donde el indice 0 es el nombre del rival y el indice 1 el porcentaje de partidos ganados
    #Se establece como criterio de ordenacion el porcentaje (indice 1)
    return max(d3.items(), key=lambda t:t[1])
