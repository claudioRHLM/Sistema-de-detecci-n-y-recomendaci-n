import json
import re
import unicodedata

def cargar_palabras_riesgo(ruta="palabras_riesgo.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""

    texto = texto.lower()
    texto = quitar_tildes(texto)
    texto = re.sub(r'[^a-zñ\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def detectar_riesgo(texto, palabras_riesgo):
    alertas = []

    texto_normalizado = normalizar_texto(texto)

    for tipo, lista_palabras in palabras_riesgo.items():
        for palabra in lista_palabras:

            palabra_norm = normalizar_texto(palabra)

            if re.search(rf'\b{re.escape(palabra_norm)}\b', texto_normalizado):
                alertas.append((tipo, palabra))

    alertas = list(set(alertas))

    return alertas