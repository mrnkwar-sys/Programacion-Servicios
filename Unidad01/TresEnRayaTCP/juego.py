TAMANO = 3
COLUMNAS = "ABC"

def crear_tablero():
    """_summary_

    Returns:
        _type_: _description_
    """
    tablero = []
    #Filas
    for i in range(TAMANO):
        fila = []
        
        #Columnas
        for j in range(TAMANO):
            fila.append(' ')
        tablero.append(fila)
    return tablero

def mostrar_tablero(tablero):
    #Imprime "  A B C", dejando un hueco delante para el numero de la fila
    print("  " + "   ".join(COLUMNAS))
    
    #numero es un contador que, gracias a start comienza en 1 en lugar de en 0
    #fila es la lista de 3 elementos de esa fila: [' ', ' ', ' ']
    for numero, fila in enumerate(tablero, start=1):
        #Imprime el numero de la fila seguido de un espacio
        #Separa cada elemento de la fila (los huecos) con " | "
        print(f"{numero} " + " | ".join(fila))
        
def coordenada_a_indice(coordenada):
    indices = None
    
    #strip elimina los espacios/saltos de linea/tabulaciones del inicio y final de la cadena
    #Convertimos a mayúscula en caso de que el cliente haya introducido la letra en minúscula
    coordenada = coordenada.strip().upper()
    
    #Comprueba que la longitud de la cadena sea igual a 2
    if len(coordenada) == 2:
        letra = coordenada[0]
        numero = coordenada[1]
        
        #Comprueba que tanto la letra como el numero guarden valores válidos
        #Si es así, los guarda como indices
        if letra in COLUMNAS and numero in "123":
            fila = int(numero) - 1
            columna = COLUMNAS.index(letra)
            indices = (fila, columna)
    return indices

def jugada_valida(tablero, coordenada):
    indices = coordenada_a_indice(coordenada)
    
    if indices == None:
        return False
    else:
        fila = indices[0]
        columna = indices[1]
        
        #Si el hueco está vacío, devuelve True
        if tablero[fila][columna] == " ":
            return True
        else:
            return False

def colocar_ficha(tablero, coordenada, ficha):
    indices = coordenada_a_indice(coordenada)
    
    if indices == None:
        return False
    else:
        fila = indices[0]
        columna = indices[1]
        
        #Modifica el hueco en el tablero para poner el valor de la ficha
        if tablero[fila][columna] == " ":
            tablero[fila][columna] = ficha
            return True
        else:
            return False

def comprobar_ganador(tablero, ficha):
    partidaGanada = False
    
    #Comprueba si se ha hecho 3 en raya horizontalmente
    for fila in range(TAMANO):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] == ficha:
            partidaGanada = True
    
    #Comprueba si se ha hecho 3 en raya verticalmente
    for col in range(TAMANO):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] == ficha:
            partidaGanada = True
    
    #Comprueba si se ha hecho 3 en raya diagonalmente (de izquierda-derecha)
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == ficha:
        partidaGanada = True
        
    #Comprueba si se ha hecho 3 en raya diagonalmente (de derecha-izquierda)
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == ficha:
        partidaGanada = True
    
    return partidaGanada

def tablero_lleno(tablero):
    lleno = True
    
    for fila in tablero:
        for espacio in fila:
            if espacio == " ":
                lleno = False
    
    return lleno

def enviar_mensaje(conexion, mensaje):
    