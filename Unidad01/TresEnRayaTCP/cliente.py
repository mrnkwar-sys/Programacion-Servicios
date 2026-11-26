import socket 
from juego import jugar

#Para probar en 2 terminales del mismo PC
HOST = "127.0.0.1"
PUERTO = 50505

def main():
    try:
        #Crea el socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            #Se conecta al servidor
            cliente.connect((HOST, PUERTO))
            print(f"Jugador 2. Conectado a {HOST}:{PUERTO}")
            jugar(cliente, empieza=False)

    except (OSError, ConnectionError, ValueError) as error:
        print(f"Error de conexión o de partida: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nPartida interrumpida")

#Arranca el programa
if __name__ == "__main__":
    main()