from collections import Counter
from api import obtener_personajes_marvel

def string_a_binario(s):
    return ' '.join(f'{ord(i):08b}' for i in s)

nombres_personajes = obtener_personajes_marvel()

personajes_binarios = {}
for personaje in nombres_personajes:
    personajes_binarios[personaje] = string_a_binario(personaje)

for personaje, binario in personajes_binarios.items():
    print(f"{personaje}: {binario}\n")

class ShannonFano:
    def __init__(self): 
        self.codes = {}

    def build_tree(self, freq):
        nodes = []
        for char, f in freq.items():
            nodes.append([f, [char, ""]])

        while len(nodes) > 1:
            nodes.sort(key=lambda item: item[0], reverse=True)
            left = nodes.pop()
            right = nodes.pop()

            for pair in left[1:]:
                pair[1] = '0' + pair[1]

            for pair in right[1:]:
                pair[1] = '1' + pair[1]
            nodes.append([left[0] + right[0]] + left[1:] + right[1:])
            
        return nodes[0]

    def assign_codes(self, node):
        if len(node) == 2:
            char = node[0]
            code = node[1]
            self.codes[char] = code

        else:
            for n in node[1:]:
                self.assign_codes(n)
    def encode(self, data):
        freq = {}
        for char in data:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1
        tree = self.build_tree(freq)
        self.assign_codes(tree)
        encoded = ''
        for char in data:
            encoded += self.codes[char]

        return encoded

    def decode(self, encoded_data):
        decoded = ''
        while encoded_data:
            for char, code in self.codes.items():
                if encoded_data.startswith(code):
                    decoded += char
                    encoded_data = encoded_data[len(code):]

        return decoded
