import xml.etree.ElementTree as ET
import json
from collections import Counter
from datetime import datetime
import unicodedata
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

def quitar_acentos(texto):
    """Elimina los acentos de un texto."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def llegir_i_mostrar_dades(xml_file):
    # Llegeix i analitza l'arxiu XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Diccionari per emmagatzemar el resum de les incidències
    resum = {
        "Data i hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Numero de incidències vàlides": 0,
        "Numero de incidències invàlides": 0,
        "Tipus incidència més sol·licitat": "",
        "Correu més freqüent": "",
        "Nom més freqüent": "",
        "Data més freqüent": ""
    }

    tipus_incidencia_counter = Counter()
    correus_counter = Counter()
    noms_counter = Counter()
    dates_counter = Counter()

    # Itera sobre cada fila (row) en l'XML
    for row in root.findall('row'):
        nombre = ""
        fecha_incidencia = ""
        correo = ""
        tipus_incidencia = ""

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
            elif etiqueta == "Tipus incidència":
                tipus_incidencia = valor

        # Validar el correu
        correo_valido = "@" in correo and correo.endswith("@itb.cat")

        # Comprobar si falta informació clau
        if any(not campo for campo in [nombre, fecha_incidencia, tipus_incidencia]):
            resum["Numero de incidències invàlides"] += 1
            continue
        elif any(char.isdigit() for char in nombre):
            resum["Numero de incidències invàlides"] += 1
            continue
        elif not correo_valido:
            resum["Numero de incidències invàlides"] += 1
            continue

        # Normalizar nombre y correo para comparar
        nombre_normalizado = quitar_acentos(nombre.lower()).replace(" ", ".")
        correo_usuario = quitar_acentos(correo.split('@')[0].lower())
        if nombre_normalizado not in correo_usuario:
            resum["Numero de incidències invàlides"] += 1
            continue

        # Contar incidències vàlides
        resum["Numero de incidències vàlides"] += 1
        tipus_incidencia_counter[tipus_incidencia] += 1
        correus_counter[correo] += 1
        noms_counter[nombre] += 1
        dates_counter[fecha_incidencia] += 1

    # Determinar els més freqüents
    if tipus_incidencia_counter:
        resum["Tipus incidència més sol·licitat"] = tipus_incidencia_counter.most_common(1)[0][0]
    if correus_counter:
        resum["Correu més freqüent"] = correus_counter.most_common(1)[0][0]
    if noms_counter:
        resum["Nom més freqüent"] = noms_counter.most_common(1)[0][0]
    if dates_counter:
        resum["Data més freqüent"] = dates_counter.most_common(1)[0][0]

    # Calcular el percentatge d'incidències vàlides
    total_incidencies = resum["Numero de incidències vàlides"] + resum["Numero de incidències invàlides"]
    percentatge_valides = (resum["Numero de incidències vàlides"] / total_incidencies * 100) if total_incidencies > 0 else 0

    # Guarda el resum en JSON
    guardar_dades_json(resum)

    # Imprimir el resum amb color
    print(f"{Fore.BLUE + Style.BRIGHT}Resum de les incidències:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Data i hora: {Fore.YELLOW}{resum['Data i hora']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Numero de incidències vàlides: {Fore.GREEN}{resum['Numero de incidències vàlides']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Numero de incidències invàlides: {Fore.RED}{resum['Numero de incidències invàlides']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Tipus incidència més sol·licitat: {Fore.GREEN}{resum['Tipus incidència més sol·licitat']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Correu més freqüent: {Fore.GREEN}{resum['Correu més freqüent']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Nom més freqüent: {Fore.GREEN}{resum['Nom més freqüent']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Data més freqüent: {Fore.GREEN}{resum['Data més freqüent']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Percentatge d'incidències vàlides: {Fore.GREEN}{percentatge_valides:.2f}%{Style.RESET_ALL}")

def guardar_dades_json(resum):
    """Guarda el resum en un fitxer JSON anomenat incidencies.json"""
    json_file = 'incidencies.json'

    try:
        # Intentar carregar el contingut existent
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                data = json.loads(content) if content else []  # Manejo del contingut buit
        except FileNotFoundError:
            data = []  # Si no existeix, crear nova estructura

        # Afegir la nova execució al fitxer
        data.append(resum)

        # Escriure el contingut actualitzat al fitxer JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"{Fore.YELLOW}Dades guardades correctament a {json_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error en guardar les dades a l'arxiu JSON: {e}{Style.RESET_ALL}")

# Ruta de l'arxiu XML
xml_file = './datos.xml'

# Executa la funció per llegir, mostrar i guardar les dades
llegir_i_mostrar_dades(xml_file)
