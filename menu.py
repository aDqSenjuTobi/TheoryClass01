import base64
import heapq
import random
import hashlib
import os
from collections import Counter
from shannonfano import ShannonFano
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

    @staticmethod
    def generar_hash_mensaje_codificado(mensaje_codificado, clave_secreta):
        return hashlib.sha256((mensaje_codificado + clave_secreta).encode()).hexdigest()

    @staticmethod
    def comparar_hash_con_simbolos(hash_mensaje, simbolos_binarios):
        return all(bit in simbolos_binarios for bit in hash_mensaje)

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

class CanalComunicacion:
    NUM_CANALES = 4
    PROBABILIDAD_RUIDO = 0.1  # Probabilidad de ruido

    @staticmethod
    def detectar_ruido():
        return random.random() < CanalComunicacion.PROBABILIDAD_RUIDO

    @staticmethod
    def enviar_mensaje(mensaje_codificado):
        canal_actual = 1
        while canal_actual <= CanalComunicacion.NUM_CANALES:
            if CanalComunicacion.detectar_ruido():
                print(f"Ruido detectado en el canal {canal_actual}. Cambiando al siguiente canal...")
                canal_actual += 1
            else:
                print(f"Mensaje enviado correctamente a través del canal {canal_actual}.")
                return True
        print("No se pudo enviar el mensaje después de intentar en todos los canales.")
        return False

class Transmisor:
    def __init__(self, metodo, mensaje_original):
        self.metodo = metodo
        self.mensaje_original = mensaje_original
        self.mensaje_codificado = None

    def codificar_mensaje(self):
        if self.metodo == "Huffman":
            arbol_huffman = Huffman.construir_arbol_huffman(self.mensaje_original)
            codificacion = {}
            Huffman.generar_codificacion_huffman(arbol_huffman, codificacion=codificacion)
            self.mensaje_codificado = Huffman.codificar_mensaje(self.mensaje_original, codificacion)

        elif self.metodo == "Shannon-Fano":
            sf = ShannonFano()
            self.mensaje_codificado = sf.encode(self.mensaje_original)

        elif self.metodo == "Inversa":
            self.mensaje_codificado = Reversa.codificar_mensaje(self.mensaje_original)

        elif self.metodo == "Base64":
            self.mensaje_codificado = Base64.codificar_mensaje(self.mensaje_original)

    def enviar_mensaje(self):
            if self.mensaje_codificado is None:
                print("Mensaje no codificado. No se puede enviar.")
                return False
            return CanalComunicacion.enviar_mensaje(self.mensaje_codificado)
    
    def generar_firma(self):
            if self.mensaje_codificado:
                hash_mensaje = hashlib.sha256(self.mensaje_codificado.encode()).hexdigest()
                print(f"Hash del mensaje codificado en Transmisor: {hash_mensaje}")
                return hash_mensaje
            else:
                print("Mensaje no codificado. No se puede generar firma.")
                return None

class Receptor:
    def __init__(self, metodo, mensaje_codificado):
        self.metodo = metodo
        self.mensaje_codificado = mensaje_codificado
        self.firmas = {} 

    def verificar_firma(self, firma):
        hash_mensaje = hashlib.sha256(self.mensaje_codificado.encode()).hexdigest()
        print(f"Hash del mensaje codificado en Receptor: {hash_mensaje}")
        es_valida = firma == hash_mensaje
        self.firmas[hash_mensaje] = firma
        return es_valida

    def decodificar_mensaje(self):
        if self.metodo == "Huffman":
            arbol_huffman = Huffman.construir_arbol_huffman(self.mensaje_codificado)
            return Huffman.decodificar_mensaje(self.mensaje_codificado, arbol_huffman)

        elif self.metodo == "Shannon-Fano":
            sf = ShannonFano()
            return sf.decode(self.mensaje_codificado)

        elif self.metodo == "Inversa":
            return Reversa.decodificar_mensaje(self.mensaje_codificado)

        elif self.metodo == "Base64":
            return Base64.decodificar_mensaje(self.mensaje_codificado)

def generar_hash(mensaje, clave_secreta):
    mensaje_clave = mensaje + clave_secreta
    return hashlib.sha256(mensaje_clave.encode()).hexdigest()

def verificar_hash(mensaje, hash_recibido, clave_secreta):
    hash_generado = generar_hash(mensaje, clave_secreta)
    return hash_generado == hash_recibido


# Función principal
def main():
    personajes = obtener_personajes_marvel()
    mensaje_original = str(personajes)


    print("Selecciona un tipo de codificación:\n1 - Huffman\n2 - Shannon-Fano\n3 - Inversa\n4 - Base64")
    opcion = int(input("Opción: "))

    metodos = {1: "Huffman", 2: "Shannon-Fano", 3: "Inversa", 4: "Base64"}
    metodo_seleccionado = metodos.get(opcion, None)

    if metodo_seleccionado:
        transmisor = Transmisor(metodo_seleccionado, mensaje_original)
        transmisor.codificar_mensaje()
        firma = transmisor.generar_firma()

        if transmisor.enviar_mensaje():
            receptor = Receptor(metodo_seleccionado, transmisor.mensaje_codificado)
            
            
            if receptor.verificar_firma(firma):
                print("Firma verificada: True")
                mensaje_decodificado = receptor.decodificar_mensaje()

                print("\nMensaje Original:")
                print(mensaje_original)
                print(f"\nMensaje Codificado ({metodo_seleccionado}):")
                print(transmisor.mensaje_codificado)
                print("\nMensaje Decodificado:")
                print(mensaje_decodificado)
            else:
                print("Firma verificada: False. El mensaje no es confiable.")

        else:
            print("No se pudo enviar el mensaje. Verifica la clave del canal.")
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()