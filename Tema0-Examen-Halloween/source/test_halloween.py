from halloween import *

def test_leer_fichero(registros):
    print()
    print("Test de la función leer_fichero")
    print("\tLeídos: ", len(registros), " registros")
    for r in registros:
        print("\t", r)
    
if __name__ == "__main__":
    registros = leer_visitas('Tema0-Examen-Halloween/data/visitas_halloween.txt')
    test_leer_fichero(registros)
    
    print(recaudacion(registros, 'Mansion'))
    print(visitas_rapidas(registros, 30, 29))
    print(asistencia_por_recorrido(registros))
    print(grupos_repetidores(registros))