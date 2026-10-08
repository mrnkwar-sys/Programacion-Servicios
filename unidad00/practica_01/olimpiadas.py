import csv
from collections import namedtuple

Atleta = namedtuple('Atleta', 'nombre, edad, pais, peso')

def leer_fichero(nombre_fichero):
    registros = []
    #Con with el fichero se cierra automáticamente al salir del bloque
    with open(nombre_fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        #Se salta la primera línea del fichero (cabecera)
        next(lector)
        for atleta in lector:
            nombre = atleta[0]
            edad = int(atleta[1])
            pais = atleta[2]
            peso = float(atleta[3])
            tupla = Atleta(nombre, edad, pais, peso)
            registros.append(tupla)
    return registros

# def edad_media(registros):
#     resultado = 0.0
#     for atleta in registros:
#         resultado += atleta[1]
#     return resultado / len(registros)

def edad_media(registros):
    resultado = 0.0
    for atleta in registros:
        resultado += atleta.edad
    return resultado / len(registros)

"""
Ejercicio 3 · Número de atletas por país
Implementa num_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves sean
los países y cuyos valores indiquen cuántos atletas pertenecen a cada país.
"""
def num_atletas_por_pais(registros):
    diccionario = {}
    for atleta in registros:
        clave = atleta.pais
        if clave in diccionario:
            diccionario[clave] += 1
        else:
            diccionario[clave] = 1
    return diccionario

'''
Ejercicio 4 · Nombres de atletas por país
Implementa nombre_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves
sean los países y cuyos valores sean listas con los nombres de los atletas de cada país.
'''
def nombre_atletas_por_pais(registros):
    diccionario = {}
    for atleta in registros:
        clave = atleta.pais
        if clave in diccionario:
            diccionario[clave].append(atleta.nombre)
        else:
            diccionario[clave] = [atleta.nombre]
    return diccionario

'''
Ejercicio 5 · Atleta de mayor peso 
Implementa atleta_mayor_peso(registros). Debe devolver el nombre del atleta con mayor peso.
'''
def atleta_mayor_peso(registros):
    return max(registros, key=lambda t:t.peso).nombre

'''
Ejercicio 6 · País con mayor peso medio 
Implementa pais_mayor_peso_medio(registros). Debe calcular el peso medio de los atletas de 
cada país y devolver el nombre del país cuyo peso medio sea mayor.
'''
def pais_mayor_peso_medio(registros):
    diccionario = {}
    peso_medio = 0.0
    for atleta in registros:
        clave = atleta.pais
        if clave in diccionario:
            diccionario[clave].append(atleta.peso)
        else:
            diccionario[clave] = [atleta.peso]
    for clave in diccionario:
        diccionario[clave] = [sum(diccionario[clave]) / len(diccionario[clave])]
    return diccionario

'''
OTRA MANERA, LA DEL PROFESOR
def pais_mayor_peso_medio(registros):
    d1 = {}
    for r in registros:
        clave = r.pais
        if clave in d1:
            d1[clave]+=[r.peso]
        else:
            d1[clave]=[r.peso]
    d2 = {}
    for clave in d1:
        d2[clave]=sum(d1[clave]/len(d1[clave]))
    return max(d2.items(), key=lambda t:t[1])[0]
'''


'''
Ejercicio 7 · Mayor diferencia de edad 
Implementa metodozip(registros). Ordena los atletas por edad, calcula la diferencia de edad 
entre cada pareja de atletas consecutivos en esa ordenación y devuelve la mayor de esas 
diferencias. Debes utilizar zip para emparejar elementos consecutivos.
'''
def metodozip(registros):
    #Se declara una lista vacia
    lis = []

    #Sorted toma la lista registros y crea una nueva con los elementos ordenados de menor a mayor
    #key=lambda t:t.edad le dice al programa que no lo ordene de cualquier manera, sino que tome como referencia el atributo .edad de cada atleta (t)
    registros = sorted(registros, key=lambda t:t.edad)

    '''
    registros_ordenados[1:] crea una copia de la lista pero empezando por el segundo elemento
    El metodo zip() junta el primer elemento de una lista con el primero del segundo, por lo que aqui estamos
    juntando al atleta1 con el atleta2, al atleta2 con el atleta3...

    for a,b asigna a la variable 'a' a la pareja mas joven y a la variable 'b' a la siguiente mas mayor
    '''
    for a,b in zip(registros, registros[1:]):
        # Obtiene la diferencia de edad entre los atletas y la anade a la lista
        lis.append(b.edad - a.edad)

        #El metodo max() revisa todas las diferencias de edad de la lista y se queda con el valor mas alto
    return max(lis)