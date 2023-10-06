import time
import random
import json
import heapq
from collections import defaultdict, Counter

class FuenteDeInformacion:
    def generar_mensaje(self):
        mensaje = {
            "mensaje": "Puros corridos tumbados"
        }
        return json.dumps(mensaje)

class Transmisor:
    def mensaje_a_binario(self, mensaje):
        mensaje_binario = ''.join(format(ord(char), '08b') for char in mensaje)
        return mensaje_binario

    def transmitir_mensaje(self, mensaje):
        mensaje_binario = self.mensaje_a_binario(mensaje)
        return mensaje_binario

class Receptor:
    def recibir_mensaje(self, mensaje_binario):
        grupos = self.agrupar_en_grupos(mensaje_binario, 8)
        return grupos

    def agrupar_en_grupos(self, mensaje_binario, tamano_grupo):
        grupos = {f'Grupo_{i+1}': mensaje_binario[i:i+tamano_grupo] for i in range(0, len(mensaje_binario), tamano_grupo)}
        return grupos

class DestinoDeInformacion:
    def mostrar_mensaje(self, mensaje_binario):
        print("Mensaje recibido en el destino (en binario):")
        print(mensaje_binario)
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
    
#Codificación Huffman

def construir_arbol_huffman(datos):
    frecuencias = Counter(datos)
    cola_prioridad = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(cola_prioridad)

    while len(cola_prioridad) > 1:
        izquierda = heapq.heappop(cola_prioridad)
        derecha = heapq.heappop(cola_prioridad)
        nodo_intermedio = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nodo_intermedio.izquierda = izquierda
        nodo_intermedio.derecha = derecha
        heapq.heappush(cola_prioridad, nodo_intermedio)

    return cola_prioridad[0]

def generar_codificacion_huffman(arbol_huffman, prefijo="", codificacion={}):
    if arbol_huffman.caracter is not None:
        codificacion[arbol_huffman.caracter] = prefijo
    if arbol_huffman.izquierda is not None:
        generar_codificacion_huffman(arbol_huffman.izquierda, prefijo + "0", codificacion)
    if arbol_huffman.derecha is not None:
        generar_codificacion_huffman(arbol_huffman.derecha, prefijo + "1", codificacion)

def codificar_mensaje(mensaje, codificacion):
    mensaje_codificado = ""
    for caracter in mensaje:
        mensaje_codificado += codificacion[caracter]
    return mensaje_codificado

def decodificar_mensaje(mensaje_codificado, arbol_huffman):
    mensaje_decodificado = ""
    nodo_actual = arbol_huffman
    for bit in mensaje_codificado:
        if bit == "0":
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.caracter is not None:
            mensaje_decodificado += nodo_actual.caracter
            nodo_actual = arbol_huffman
    return mensaje_decodificado


if __name__ == "__main__":
    fuente = FuenteDeInformacion()
    transmisor = Transmisor()
    receptor = Receptor()
    destino = DestinoDeInformacion()

    # Generar el mensaje en la fuente
    mensaje_original = fuente.generar_mensaje()
    print("Mensaje original:", mensaje_original)

    # Transmitir el mensaje a través del transmisor (transformado a binario)
    mensaje_transmitido = transmisor.transmitir_mensaje(mensaje_original)
    print("Mensaje transmitido (binario):", mensaje_transmitido)

    # Recibir el mensaje en el receptor (en binario)
    mensaje_recibido = receptor.recibir_mensaje(mensaje_transmitido)
    
    # Almacenar los grupos en una variable
    grupos = mensaje_recibido
    
    for key, value in grupos.items():
        print(key, ":", value)

    # Mostrar el mensaje en el destino (en binario)
    destino.mostrar_mensaje(mensaje_recibido)

        # Construir el árbol de Huffman
    arbol_huffman = construir_arbol_huffman(mensaje_original)
    
    # Generar la codificación Huffman
    codificacion = {}
    generar_codificacion_huffman(arbol_huffman, codificacion=codificacion)
    
    # Codificar el mensaje original
    mensaje_codificado = codificar_mensaje(mensaje_original, codificacion)
    
    # Decodificar el mensaje codificado
    mensaje_decodificado = decodificar_mensaje(mensaje_codificado, arbol_huffman)
    
    print("Mensaje Original:", mensaje_original)
    print("Mensaje Codificado:", mensaje_codificado)
    print("Mensaje Decodificado:", mensaje_decodificado)