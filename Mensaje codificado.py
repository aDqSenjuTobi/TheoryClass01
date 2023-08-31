import hashlib
import random

class Transmisor:
    def codificar_mensaje(self, mensaje):
        hash_obj = hashlib.sha256()
        hash_obj.update(mensaje.encode('utf-8'))
        mensaje_hash = hash_obj.hexdigest()
        return mensaje_hash

class Canal:
    def introduce_ruido(self, cadena_hash, probabilidad):
        caracteres_posibles = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-"
        mensaje_ruidoso = ""
        for char in cadena_hash:
            if random.random() < probabilidad:
                mensaje_ruidoso += random.choice(caracteres_posibles)
            else:
                mensaje_ruidoso += char
        return mensaje_ruidoso

class Receptor:
    def decodificar_mensaje_con_ruido(self, cadena_ruidosa, probabilidad_ruido):
        cadena_limpia = ""
        for char in cadena_ruidosa:
            if random.random() < probabilidad_ruido:
                pass
            else:
                cadena_limpia += char
        return cadena_limpia

# Fuente de información
mensaje_original = "Si puedes leer esto, felicidades. Funcionó."
print("Mensaje original:", mensaje_original)

transmisor = Transmisor()
mensaje_codificado = transmisor.codificar_mensaje(mensaje_original)
print("Mensaje codificado (hash):", mensaje_codificado)

# Canal
probabilidad_ruido = 0.9  # Probabilidad de ruido (ejemplo: 0.1 significa 10% de probabilidad)
canal = Canal()
mensaje_con_ruido = canal.introduce_ruido(mensaje_codificado, probabilidad_ruido)
print("Mensaje con ruido:", mensaje_con_ruido)

# Receptor
receptor = Receptor()
mensaje_sin_ruido = receptor.decodificar_mensaje_con_ruido(mensaje_con_ruido, probabilidad_ruido)
print("Mensaje decodificado sin ruido:", mensaje_sin_ruido)