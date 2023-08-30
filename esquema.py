import hashlib
import random

# Fuente de información
mensaje_original = "Si puedes leer esto, felicidades. Funcionó."

# Transmisor
def codificar_mensaje(mensaje):
    # Calcular el hash SHA-256 del mensaje
    hash_obj = hashlib.sha256()
    hash_obj.update(mensaje.encode('utf-8'))
    mensaje_hash = hash_obj.hexdigest()
    return mensaje_hash

mensaje_codificado = codificar_mensaje(mensaje_original)
print("Mensaje codificado (hash):", mensaje_codificado)

# Canal con afectación por ruido
def introduce_ruido(cadena_hash, probabilidad):
    # Simulación de ruido en el hash
    mensaje_ruidoso = ""
    for char in cadena_hash:
        if random.random() < probabilidad:
            mensaje_ruidoso += chr(random.randint(0, 255))
        else:
            mensaje_ruidoso += char
    return mensaje_ruidoso

probabilidad_ruido = 0.1  # Probabilidad de ruido (ejemplo: 0.1 significa 10% de probabilidad)
mensaje_con_ruido = introduce_ruido(mensaje_codificado, probabilidad_ruido)
print("Mensaje con ruido:", mensaje_con_ruido)

# Receptor
def decodificar_mensaje(cadena_hash):
    # Simplemente mostrar el hash recibido
    return cadena_hash

mensaje_decodificado = decodificar_mensaje(mensaje_con_ruido)
print("Mensaje decodificado:", mensaje_decodificado)

# Destino de información
print("Mensaje original:", mensaje_original)

