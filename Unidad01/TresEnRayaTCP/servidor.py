import socket 
from juego import jugar

#Acepta conexiones desde cualquier interfaz de red
HOST = "0.0.0.0"
PUERTO = 50505

def main():
    try:
        #Crea el socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            #Activa la reutilizacion de direccion para reiniciar el servidor sin esperar a que se libere el puerto
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #Asocia IP y puerto
            servidor.bind((HOST, PUERTO))
            #Pone el socket a escuchar
            servidor.listen(1)

            conexion, direccion = servidor.accept()

            with conexion:
                print(f"Jugador 2 conectado desde {direccion[0]}")
                jugar(conexion, empieza=True)
                
    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida")

#Arranca el programa
if __name__ == "__main__":
    main()