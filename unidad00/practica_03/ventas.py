import csv
from collections import namedtuple
from datetime import datetime

Ventas = namedtuple('Ventas', 'id, fecha, cliente, producto, cantidad, precio, beneficio')

def leer_fichero_ventas(fichero):
    registros_ventas = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for venta in lector:
            id = int(venta[0])
            fecha = datetime.strptime(venta[1], '%d/%m/%Y').date()
            cliente = venta[2]
            producto = venta[3]
            cantidad = int(venta[4])
            precio = float(venta[5])
            beneficio = float(venta[6])
    return registros_ventas

'''
Ejercicio 1
Implementa clientes_producto1_y_producto2(ventas, producto1, producto2). Recibe una lista de
objetos Venta y los nombres de dos productos. Debe devolver un conjunto con los nombres de
los clientes que hayan comprado ambos productos. No se pueden usar bucles explícitos; si
necesitas iterar, utiliza comprensiones.
Ejemplo de interpretación
Si para 'ProductoA' y 'ProductoC' se obtiene {'ClienteA', 'ClienteB'}, significa que esos clientes
aparecen como compradores de los dos productos.
'''
def clientes_producto1_producto2(registros_ventas, producto1, producto2):
    #Lista de clientes con cada cliente en registros donde el producto sea igual a producto1
    cliente_producto1 = {venta.cliente for venta in registros_ventas if venta.producto == producto1}

    #Lista de clientes con cada cliente en registros donde el producto sea igual a producto1
    cliente_producto2 = {venta.cliente for venta in registros_ventas if venta.producto == producto2}

    #& devuelve un conjunto solo con los elementos que aparecen en ambas listas
    return cliente_producto1 & cliente_producto2

'''
Ejercicio 2
Implementa diccionario_porcentaje_cantidad_producto(ventas). Debe devolver un diccionario
que relacione cada producto con el porcentaje de unidades vendidas de ese producto respecto
al total de unidades vendidas. Utiliza al menos una función auxiliar.
Ejemplo de interpretación
Si 'ProductoC' tiene asociado 3.56, sus unidades representan el 3,56 % del total de unidades
vendidas.
'''
def diccionario_porcentaje_cantidad_producto(registros_ventas):
    result = {}

    #Sumamos las cantidades de cada producto del fichero
    total = sum([venta.cantidad for venta in registros_ventas])

    #La funcion auxiliar nos da las cantidades vendidas de cada producto
    dict_productos_cantidades = obtener_cantidad_producto(registros_ventas)

    for clave in dict_productos_cantidades:
        result[clave] = dict_productos_cantidades[clave]/total*100.0
    return result

def obtener_cantidad_producto(registros_ventas):
    dict_cantidades = {}
    for venta in registros_ventas:
        clave = venta.producto
        if clave in dict_cantidades:
            dict_cantidades[clave] += venta.cantidad
        else:
            dict_cantidades[clave] = venta.cantidad
    return dict_cantidades

'''
Ejercicio 3
Implementa producto_mas_vendido(ventas, clientes, n=3). Recibe una lista de ventas, un
conjunto de nombres de clientes y un entero n. Debe devolver el nombre del producto más
frecuente entre las n compras con mayor número de unidades realizadas por cualquiera de esos
clientes.
Ejemplo de interpretación
Si entre las 5 compras de mayor cantidad de ClienteA y ClienteF el producto que más se repite
es ProductoC, la función debe devolver 'ProductoC'.
'''
def producto_mas_vendido(registros_ventas, clientes, n=3):
    lista_compras = compras_solicitadas_clientes(registros_ventas, clientes, n)
    productos_frecuentes = frecuencia_productos(lista_compras)
    return max(productos_frecuentes.items(), key=lambda t:t[1][0])

def compras_solicitadas_clientes (registros_ventas, clientes, n=3):
    #Selecciona solo los clientes cuyos nombres se encuentran en la lista de clientes
    clientes_solicitados = [venta for venta in registros_ventas if venta.cliente in clientes]

    #Ordena la lista de los clientes por las cantidades compradas de cada producto de mayor a menor
    clientes_ordenados = sorted(clientes_solicitados, reverse=True, key=lambda t:t.cantidad)

    #Devuelve el numero solicitado de compras de cada cliente
    return clientes_ordenados[:n]

def frecuencia_productos(lista_compras_solicitadas):
    dict_productos = {}
    for cliente in lista_compras_solicitadas:
        clave = cliente.producto
        if clave in dict_productos:
            dict_productos[clave] += 1
        else:
            dict_productos[clave] = 1
    return dict_productos