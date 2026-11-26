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

def pedir_jugada(tablero):
    coordenada = ""
    correcto = False
    
    while not correcto:
        #Pide una coordenada al cliente/servidor
        coordenada = input("Introduce coordenada (ej. B2): ").strip().upper()
        
        #Comprueba si la coordenada introducida es válida
        if not jugada_valida(tablero, coordenada):
            print("Coordenada no válida o casilla ocupada")
        else:
            correcto = True
    
    return coordenada

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
    #Envia un mensaje terminado en salto de linea
    datos = (mensaje + "\n").encode("utf-8")
    conexion.sendall(datos)

def recibir_mensaje(conexion):
    #Lista mutable de bytes vacía donde se acumularan las letras segun vayan llegando
    datos = bytearray()
    terminado = False

    while not terminado:
        #Espera a recibir 1 byte del socket
        fragmento = conexion.recv(1)

        #Si recv devuelve una cadena vacía significa que el otro extremo se ha desconectado/caido
        if not fragmento:
            raise ConnectionError("El otro jugador se ha desconectado")
        #Comprueba si el byte recibido es el salto de linea (en formato bytes, por eso la b)
        #Si lo es, ya tenemos el mensaje entero y salimos del bucle
        if fragmento == b"\n":
            terminado = True
        else:
            #Si no es el salto del línea (final del mensaje), guarda el byte en datos
            datos.extend(fragmento)
            #Medida de seguridad para evitar que que se llene la memoria si alguien envía un mensaje demasiado largo
            if len(datos) > 64:
                raise ValueError("Mensaje demasiado largo")

    #Convierte la lista de bytes en una cadena de texto normal Python
    return datos.decode("utf-8")

def jugar(conexion, empieza):
    tablero = crear_tablero()
    #Define que empieza moviendo
    mi_turno = empieza
    #Controla el bucle principal
    partida_terminada = False
    
    if (empieza):
        mi_ficha = "X"
        ficha_rival = "O"
    else:
        mi_ficha = "O"
        ficha_rival = "X"
    
    while not partida_terminada:
        if mi_turno:
            print("\n--- TU TURNO ---")
            mostrar_tablero(tablero)
            print(f"Tu ficha es {mi_ficha}")
            
            #Pide una jugada al cliente/servidor
            coordenada = pedir_jugada(tablero)
            
            #Coloca en la coordenada introducida la ficha en el tablero
            colocar_ficha(tablero, coordenada, mi_ficha)
            
            #Envia el movimiento realizado al otro jugador
            enviar_mensaje(conexion, f"JUGADA|{coordenada}")
            
            #Comrpueba si el servidor/cliente ha ganado
            if comprobar_ganador(tablero, mi_ficha):
                mostrar_tablero(tablero)
                print("\n¡HAS GANADO!")
                partida_terminada = True
            #Comprueba si el tablero se ha llenado sin que nadie haya ganado
            elif tablero_lleno(tablero):
                mostrar_tablero(tablero)
                print("\n¡HA HABIDO UN EMPATE - NADIE GANA!")
                partida_terminada = True
            else:
                mi_turno = False
        else:
            print("\n--- TURNO DEL RIVAL ---")
            mostrar_tablero(tablero)
            print("Esperando su jugada...")
            
            #Se recibe la jugada del rival
            mensaje = recibir_mensaje(conexion)
            
            #Se divide el mensaje en dos partes
            partes = mensaje.split("|")
            
            #Comprueba que las partes del mensaje de la jugada sean coherentes "JUGADA" y la jugada en sí
            if len(partes) == 2 and partes[0] == "JUGADA":
                #Guarda la coordenada introducida
                coordenada = partes[1]
                #Comprueba si la coordenada introducida por el rival es válida
                if colocar_ficha(tablero, coordenada, ficha_rival) == False:
                    raise ValueError("Jugada rival inválida")
                
                #Comrpueba si el servidor/cliente ha ganado
                if comprobar_ganador(tablero, ficha_rival):
                    mostrar_tablero(tablero)
                    print("\n¡HAS PERDIDO!")
                    partida_terminada = True
                #Comprueba si el tablero se ha llenado sin que nadie haya ganado
                elif tablero_lleno(tablero):
                    mostrar_tablero(tablero)
                    print("\n¡HA HABIDO EMPATE - NINGUNO GANA!")
                    partida_terminada = True
                #Si nadie ha ganado ni se ha llenado el tablero continúa el siguiente turno
                else:
                    mi_turno = True
            else:
                raise ValueError("Mensaje inesperado: " + mensaje)