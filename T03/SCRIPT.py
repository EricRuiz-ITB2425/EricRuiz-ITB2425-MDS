import xml.etree.ElementTree as ET
import json
from collections import Counter

# Aules vàlides
aules_valides = {
    "1", "2", "3", "4", "5", "9", "12", "13", "14", "15", "16", "17", "18", "19",
    "24", "25", "99", "101", "102", "103", "105", "106", "107", "108", "109",
    "201", "202", "205", "206", "207", "208", "209", "301", "302", "305", "306",
    "307", "308", "309", "001", "002", "003", "004", "005", "009", "01", "02",
    "03", "04", "05", "09", "012", "013", "014", "015", "016", "017", "018",
    "019", "024", "025", "099"
}

def llegir_i_mostrar_dades(xml_file):
    """
    Llegeix i analitza l'arxiu XML, aplica filtres i guarda un resum en un fitxer JSON.
    """
    # Llegeix i analitza l'arxiu XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Diccionari per emmagatzemar el resum de les incidències
    resum = {
        "Numero de incidències vàlides": 0,
        "Nombre": 0,
        "Fecha de la incidència": 0,
        "Adreça electrònica": 0,
        "Tipus incidència més sol·licitat": "",
        "Correu més freqüent": "",
        "Nom més freqüent": "",
        "Data més freqüent": "",
        "Dates": []
    }

    descripciones_procesadas = set()
    tipus_incidencia_counter = Counter()
    correus_counter = Counter()
    noms_counter = Counter()
    dates_counter = Counter()

    # Itera sobre cada fila (row) en l'XML
    for row in root.findall('row'):
        nombre = ""
        fecha_incidencia = ""
        correo = ""

        # Extraure informació necessària
        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text.strip() if element.text else ""

            if etiqueta == "Nom i cognoms":
                nombre = valor
            elif etiqueta == "Data de la incidència":
                fecha_incidencia = valor
            elif etiqueta == "Adreça electrònica":
                correo = valor

        # Aplicar filtres
        if any(not campo for campo in [nombre, fecha_incidencia, correo]):
            continue  # Ignorar si falta informació clau

        if any(char.isdigit() for char in nombre):
            continue  # Ignorar si el nom conté números

        # Si passa tots els filtres, comptar les incidències vàlides
        resum["Numero de incidències vàlides"] += 1
        resum["Nombre"] += 1 if nombre else 0
        resum["Fecha de la incidència"] += 1 if fecha_incidencia else 0
        resum["Adreça electrònica"] += 1 if correo else 0

        # Actualitzar counters
        noms_counter[nombre] += 1
        correus_counter[correo] += 1
        dates_counter[fecha_incidencia] += 1
        resum["Dates"].append(fecha_incidencia)

    # Determinar els més freqüents
    if noms_counter:
        resum["Nom més freqüent"] = noms_counter.most_common(1)[0][0]
    if correus_counter:
        resum["Correu més freqüent"] = correus_counter.most_common(1)[0][0]
    if dates_counter:
        resum["Data més freqüent"] = dates_counter.most_common(1)[0][0]
    if tipus_incidencia_counter:
        resum["Tipus incidència més sol·licitat"] = tipus_incidencia_counter.most_common(1)[0][0]

    # Guarda el resum en JSON
    guardar_dades_json(resum)

    # Imprimir el resum a la consola
    print("Resum de les incidències vàlides:")
    for key, value in resum.items():
        print(f"{key}: {value}")


def guardar_dades_json(resum):
    """
    Guarda el resum en un fitxer JSON anomenat resum_incidencies.json
    """
    json_file = 'resum_incidencies.json'

    try:
        # Intentar carregar el contingut existent
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"ejecuciones": []}  # Si no existeix, crear nova estructura

        # Afegir la nova execució al fitxer
        data["ejecuciones"].append(resum)

        # Escriure el contingut actualitzat al fitxer JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Dades guardades correctament a {json_file}")
    except Exception as e:
        print(f"Error en guardar les dades a l'arxiu JSON: {e}")


# Ruta de l'arxiu XML
xml_file = './datos.xml'

# Executa la funció per llegir, mostrar i guardar les dades
llegir_i_mostrar_dades(xml_file)
