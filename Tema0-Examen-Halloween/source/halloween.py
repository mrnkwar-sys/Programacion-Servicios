import csv
from collections import namedtuple
from datetime import datetime

'''
codigo,fecha,grupo,recorrido,personas,minutos,sustos,precio
H001,22/10/2026,Cuervos,Cripta,6,28,33,5.00
'''

Visitas = namedtuple('Visita', 'codigo, fecha, grupo, recorrido, personas, minutos, sustos, precio')

'''
Ejercicio 1 · Carga de visitas (2 puntos) 
Implementa leer_visitas(ruta). Debe abrir el fichero en UTF-8, ignorar la cabecera, convertir 
los tipos indicados (incluida fecha a date) y devolver una lista de objetos Visita. Con el 
fichero entregado deben obtenerse 24 registros. 
'''
def leer_visitas(ruta):
    visitas = []
    with open(ruta, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for visita in lector:
            codigo = visita[0]
            fecha = datetime.strptime(visita[1], '%d/%m/%Y').date()
            grupo = visita[2]
            recorrido = visita[3]
            personas = int(visita[4])
            minutos = int(visita[5])
            sustos = int(visita[6])
            precio = float(visita[7])
            tupla = Visitas(codigo, fecha, grupo, recorrido, personas, minutos, sustos, precio)
            visitas.append(tupla)
    return visitas

'''
Ejercicio 2 · Recaudación de un recorrido (2 puntos) 
Implementa recaudacion(visitas, recorrido). Devuelve el importe total recaudado por el 
recorrido indicado, calculado como la suma de personas × precio de cada visita de ese 
recorrido. Si no existe, devuelve 0.
'''
def recaudacion(visitas, recorrido):
    importe_total = 0.0
    for visita in visitas:
        if recorrido == visita.recorrido:
            importe_total += visita.personas*visita.precio
    return importe_total

'''
Ejercicio 3 · Visitas rápidas y aterradoras (2 puntos) 
Implementa visitas_rapidas(visitas, sustos_minimos, duracion_maxima). Devuelve una lista 
con los códigos de las visitas que registraron al menos sustos_minimos sustos y duraron 
como máximo duracion_maxima minutos. La lista debe estar ordenada por código de menor a 
mayor. Si ninguna visita cumple ambas condiciones, devuelve []. 
'''
def visitas_rapidas(visitas, sustos_minimos, duracion_maxima):
    lista_codigos = []
    for visita in visitas:
        if visita.sustos >= sustos_minimos and visita.minutos <= duracion_maxima:
            lista_codigos.append(visita.codigo)
    return sorted(lista_codigos)

'''
Ejercicio 4 · Asistencia por recorrido (2 puntos) 
Implementa asistencia_por_recorrido(visitas). Devuelve un diccionario que asocie cada 
recorrido con el número total de personas que lo han realizado. Debes sumar personas; no se 
trata de contar líneas del fichero. 
'''
def asistencia_por_recorrido(visitas):
    dict_recorrido_personas = {}
    for visita in visitas:
        clave = visita.recorrido
        if clave in dict_recorrido_personas:
            dict_recorrido_personas[clave] += visita.personas
        else:
            dict_recorrido_personas[clave] = visita.personas
    return dict_recorrido_personas

'''
Ejercicio 5 · Grupos que repiten experiencia (2 puntos) 
Implementa grupos_repetidores(visitas). Devuelve un conjunto con los nombres de los 
grupos que han visitado al menos dos recorridos distintos. Varias visitas del mismo grupo a 
un único recorrido NO son suficientes. Un grupo debe aparecer una sola vez en el resultado. 
'''
def grupos_repetidores(visitas):
    set_grupos = set()
    dict_recorridos_grupos = {}
    for visita in visitas:
        clave = visita.grupo
        if clave in dict_recorridos_grupos:
             dict_recorridos_grupos[clave].append(visita.recorrido)
        else:
            dict_recorridos_grupos[clave] = [visita.recorrido]
    
    for clave in dict_recorridos_grupos:
        set(dict_recorridos_grupos[clave])
        if len(dict_recorridos_grupos[clave]) > 1:
            set_grupos.add(clave)
    return set_grupos