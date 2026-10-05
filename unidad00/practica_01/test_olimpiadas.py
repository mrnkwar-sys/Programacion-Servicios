from olimpiadas import *

def test_leer_fichero(registros):
    print()
    print("Test de la función leer_fichero")
    print("\tLeídos: ", len(registros), " registros")
    print("\tMostrando los 3 primeros:")
    # #[0:3] es lo mismo que [:3]
    # print(registros[:3])
    for r in registros[:3]:
        print("\t", r)
    
if __name__ == "__main__":
    print("Proyecto olimpiadas")
    registros = leer_fichero('unidad00/practica_01/atletas.txt')
    test_leer_fichero(registros)
    
    print(num_atletas_por_pais(registros))
    print(nombre_atletas_por_pais(registros))
    print(pais_mayor_peso_medio(registros))