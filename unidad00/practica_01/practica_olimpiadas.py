import csv
from collections import namedtuple

Atleta = namedtuple('Atleta', 'nombre, edad, pais, peso')

def leer_fichero(nombre_fichero):
    #Creamos una lista vacia
    atletas = []
    #Abrimos el fichero y lo denominamos f
    with open (nombre_fichero, encoding='utf-8') as f:
        #Guardamos el fichero para su lectura
        registros = csv.reader(f)
        #Nos saltamos la primera linea del fichero
        next (registros)
        #Por cada linea (atleta) del fichero guardamos los datos del atleta
        for atleta in registros:
            nombre = atleta[0]
            edad = int(atleta[1])
            pais = atleta[2]
            peso = float(atleta[3])
            #Creamos una tupla con los datos recogidos
            tupla = Atleta(nombre, edad, pais, peso)
            #Guardamos la tupla en una lista
            atletas.append(tupla)
    #La funcion devuelve la lista con todas las tuplas
    return atletas

'''
Ejercicio 2 · Edad media
Implementa edad_media(registros). Debe devolver la edad media de todos los atletas.
'''
def edad_media(registros):
    suma_edades = 0.0
    for atleta in registros:
        suma_edades += atleta.edad
    return suma_edades/len(registros)

'''
Ejercicio 3 · Número de atletas por país
Implementa num_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves sean
los países y cuyos valores indiquen cuántos atletas pertenecen a cada país.
'''
def num_atletas_por_pais(registros):
    dict_paises_atletas = {}
    for atleta in registros:
        clave = atleta.pais
        if clave in dict_paises_atletas:
            dict_paises_atletas[clave] += 1
        else:
            dict_paises_atletas[clave] = 1
    return dict_paises_atletas

'''
Ejercicio 4 · Nombres de atletas por país
Implementa nombre_atletas_por_pais(registros). Debe devolver un diccionario cuyas claves
sean los países y cuyos valores sean listas con los nombres de los atletas de cada país.
'''
def nombre_atletas_por_pais(registros):
    dict_paises_nombres = {}
    for atleta in registros:
        clave = atleta.pais
        if clave in dict_paises_nombres:
            dict_paises_nombres[clave].append(atleta.nombre)
        else:
            dict_paises_nombres[clave] = [atleta.nombre]
    return dict_paises_nombres

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
    dict_paises_peso = {}
    for atleta in registros:
        clave = atleta.pais
        if clave in dict_paises_peso:
            dict_paises_peso[clave].append(atleta.peso)
        else:
            dict_paises_peso[clave] = [atleta.peso]
    for pais in dict_paises_peso:
        dict_paises_peso[pais] = [sum(dict_paises_peso[pais])/len(dict_paises_peso[pais])]
    #return max(dict_paises_peso, key=lambda k: dict_paises_peso.get(k))
    #return max(dict_paises_peso, key=lambda k: dict_paises_peso[k])
    return max(dict_paises_peso, key=dict_paises_peso.get)

'''
Ejercicio 7 · Mayor diferencia de edad
Implementa metodozip(registros). Ordena los atletas por edad, calcula la diferencia de edad
entre cada pareja de atletas consecutivos en esa ordenación y devuelve la mayor de esas
diferencias. Debes utilizar zip para emparejar elementos consecutivos.
'''
def metodozip(registros):
    list_diferencia_edades = []
    edades_ordenadas = sorted(registros, key=lambda t:t.edad)

    for a,b in zip(edades_ordenadas, edades_ordenadas[1:]):
        list_diferencia_edades.append(b.edad - a.edad)

    return max(list_diferencia_edades)