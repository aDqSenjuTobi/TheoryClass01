import requests
import hashlib
import time

def obtener_personajes_marvel():
# Credenciales de la API de Marvel
    API_KEY = 'a39680773895633d37b9c3d07412b249'
    PRIVATE_KEY = '05a59cdadf383311e5f50b436732915cd305a425'
    base_url = "https://gateway.marvel.com/v1/public/characters"

    timestamp = str(time.time())
    hash_str = hashlib.md5(f"{timestamp}{PRIVATE_KEY}{API_KEY}".encode()).hexdigest()

    params = {'ts': timestamp, 'apikey': API_KEY, 'hash': hash_str}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        characters = data['data']['results']
        character_names = [character['name'] for character in characters]
        return character_names
    else:
        print("Error al realizar la solicitud:", response.status_code)
        return None