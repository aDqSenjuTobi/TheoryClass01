import base64
import heapq
from collections import Counter
import requests
from api import obtener_personajes_marvel

class Huffman:
    class NodoHuffman:
        def __init__(self, caracter, frecuencia):
            self.caracter = caracter
            self.frecuencia = frecuencia
            self.izquierda = None
            self.derecha = None

        def __lt__(self, otro):
            return self.frecuencia < otro.frecuencia

    @classmethod
    def construir_arbol_huffman(cls, datos):
        frecuencias = Counter(datos)
        cola_prioridad = [cls.NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
        heapq.heapify(cola_prioridad)

        while len(cola_prioridad) > 1:
            izquierda = heapq.heappop(cola_prioridad)
            derecha = heapq.heappop(cola_prioridad)
            nodo_intermedio = cls.NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
            nodo_intermedio.izquierda = izquierda
            nodo_intermedio.derecha = derecha
            heapq.heappush(cola_prioridad, nodo_intermedio)

        return cola_prioridad[0]

    @classmethod
    def generar_codificacion_huffman(cls, arbol_huffman, prefijo="", codificacion={}):
        if arbol_huffman.caracter is not None:
            codificacion[arbol_huffman.caracter] = prefijo
        if arbol_huffman.izquierda is not None:
            cls.generar_codificacion_huffman(arbol_huffman.izquierda, prefijo + "0", codificacion)
        if arbol_huffman.derecha is not None:
            cls.generar_codificacion_huffman(arbol_huffman.derecha, prefijo + "1", codificacion)

    @classmethod
    def codificar_mensaje(cls, mensaje, codificacion):
        mensaje_codificado = ""
        for caracter in mensaje:
            mensaje_codificado += codificacion[caracter]
        return mensaje_codificado

    @classmethod
    def decodificar_mensaje(cls, mensaje_codificado, arbol_huffman):
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

class ShannonFano:
    @staticmethod
    def shannon_fano_encoding(data):
        freq = Counter(data)
        freq = {k: v / len(data) for k, v in freq.items()}

        nodes = sorted(list(freq.items()), key=lambda x: x[1], reverse=True)
        nodes = [[node] for node in nodes]

        while len(nodes) > 1:
            e1 = sum(nodes[0][0][1] for node in nodes[0])
            e2 = sum(nodes[0][0][1] for node in nodes[1])

            if e1 >= e2:
                group = nodes.pop(0)
                for k in group:
                    k[0] = '0' + k[0]
                nodes[0].extend(group)
            else:
                group = nodes.pop(1)
                for k in group:
                    k[0] = '1' + k[0]
                nodes[0].extend(group)
            nodes[0] = sorted(nodes[0], key=lambda x: x[1], reverse=True)

        encoding = {v[0]: k for k, v in nodes[0]}
        return ''.join([encoding[i] for i in data])

    @staticmethod
    def shannon_fano_decoding(encoded_string, encoding):
        reverse_encoding = {v: k for k, v in encoding.items()}
        start = 0
        result = ''
        for i in range(1, len(encoded_string) + 1):
            substr = encoded_string[start:i]
            if substr in reverse_encoding:
                result += reverse_encoding[substr]
                start = i
        return result

class Reversa:
    @staticmethod
    def codificar_mensaje(mensaje):
        return mensaje[::-1]

    @staticmethod
    def decodificar_mensaje(mensaje):
        return mensaje[::-1]

class Base64:
    @staticmethod
    def codificar_mensaje(mensaje):
        mensaje_bytes = mensaje.encode('ascii')
        base64_bytes = base64.b64encode(mensaje_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    @staticmethod
    def decodificar_mensaje(mensaje):
        base64_bytes = mensaje.encode('ascii')
        mensaje_bytes = base64.b64decode(base64_bytes)
        mensaje = mensaje_bytes.decode('ascii')
        return mensaje

print("Selecciona un tipo de codificación:\n1 - Huffman\n2 - Shannon-Fano\n3 - Inversa\n4 - Base64")
opcion = int(input("Opción: "))
personajes = obtener_personajes_marvel()  # Aquí obtienes los personajes desde la API

mensaje_original = str(personajes) 

if opcion == 1:
    arbol_huffman = Huffman.construir_arbol_huffman(mensaje_original)
    codificacion = {}
    Huffman.generar_codificacion_huffman(arbol_huffman, codificacion=codificacion)
    mensaje_codificado = Huffman.codificar_mensaje(mensaje_original, codificacion)
    mensaje_decodificado = Huffman.decodificar_mensaje(mensaje_codificado, arbol_huffman)
    metodo = "Huffman"
elif opcion == 2:
    mensaje_codificado = ShannonFano.shannon_fano_encoding(mensaje_original)
    encoding = {k: v for k, v in Counter(mensaje_original).items()}
    mensaje_decodificado = ShannonFano.shannon_fano_decoding(mensaje_codificado, encoding)
    metodo = "Shannon-Fano"
elif opcion == 3:
    mensaje_codificado = Reversa.codificar_mensaje(mensaje_original)
    mensaje_decodificado = Reversa.decodificar_mensaje(mensaje_codificado)
    metodo = "Inversa"
elif opcion == 4:
    mensaje_codificado = Base64.codificar_mensaje(mensaje_original)
    mensaje_decodificado = Base64.decodificar_mensaje(mensaje_codificado)
    metodo = "Base64"
else:
    print("Opción no válida")

print("\nMensaje Original:")
print(mensaje_original)
print(f"\nMensaje Codificado ({metodo}):")
print(mensaje_codificado)
print("\nMensaje Decodificado:")
print(mensaje_decodificado)