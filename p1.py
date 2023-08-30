import random
import requests

# Fuente de información
mensaje_original = "Si puedes leer esto, felicidades. Funcionó."

# Transmisor
def codificar_mensaje(mensaje):
    mensaje_binario = ' '.join(format(ord(c), '08b') for c in mensaje)
    return mensaje_binario

mensaje_codificado = codificar_mensaje(mensaje_original)
print("Mensaje codificado:", mensaje_codificado)

# Canal con afectación por ruido
def introduce_ruido(cadena_binaria, probabilidad):
    mensaje_ruidoso = ""
    for bit in cadena_binaria:
        if random.random() < probabilidad:
            mensaje_ruidoso += '0' if bit == '1' else '1'
        else:
            mensaje_ruidoso += bit
    return mensaje_ruidoso

probabilidad_ruido = 0.1  # Probabilidad de ruido (ejemplo: 0.1 significa 10% de probabilidad)
mensaje_con_ruido = introduce_ruido(mensaje_codificado, probabilidad_ruido)
print("Mensaje con ruido:", mensaje_con_ruido)

def decodificar_mensaje(cadena_binaria):
    caracteres = []
    for byte in cadena_binaria.split():
        byte = byte.replace(" ", "")  # Eliminar espacios en blanco
        caracteres.append(chr(int(byte, 2)))
    mensaje_decodificado = ''.join(caracteres)
    print("Mensaje decodificado:")
    print(mensaje_decodificado)

mensaje_decodificado = decodificar_mensaje(mensaje_con_ruido)
print("Mensaje decodificado:", mensaje_decodificado)

# Destino de información
print("Mensaje original:", mensaje_original)