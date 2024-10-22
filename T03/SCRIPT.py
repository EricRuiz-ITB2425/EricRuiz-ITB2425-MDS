"""
Eric Ruiz Fernandez, Manuel Reyes Chinga, Ernesto Martinez Argueta, Izan Fernandez Arrea.
18/10/2024
ASIXcB MDS TA03
Descripció: Script Processar les dades
"""

# Aquest programa ens ajudara a processar les dades d'un XML en pantalla.


import xml.etree.ElementTree as ET
import json
from colorama import init, Fore, Style

# Inicialitza colorama per als colors en la consola
init(autoreset=True)


def llegir_i_mostrar_dades(xml_file):
    """
    Llegeix i analitza l'arxiu XML, mostra les dades per consola i les guarda en un fitxer JSON.
    """
    # Llegeix i analitza l'arxiu XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Llista per emmagatzemar les incidències
    incidencies = []

    # Itera sobre cada fila (row) en l'XML
    for i, row in enumerate(root.findall('row')):
        print(f"{Fore.YELLOW + Style.BRIGHT}Incidència {i + 1}{Style.RESET_ALL}")

        # Diccionari per emmagatzemar cada incidència
        incidencia = {}

        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text if element.text else "No disponible"
            incidencia[etiqueta] = valor  # Emmagatzema l'etiqueta i el valor al diccionari

            # Afegeix color segons el tipus d'informació
            if etiqueta == "Nivell urgencia de solució":
                color = Fore.RED if "Molt Urgent" in valor else Fore.YELLOW if "Urgent" in valor else Fore.GREEN
                print(f"\t{color}{etiqueta}: {valor}{Style.RESET_ALL}")
            else:
                print(f"\t{Fore.CYAN}{etiqueta}: {Fore.WHITE}{valor}{Style.RESET_ALL}")

        # Afegeix la incidència a la llista d'incidències
        incidencies.append(incidencia)

        print("-" * 80)

    # Després de processar totes les incidències, guarda-les en un fitxer JSON
    guardar_dades_json(incidencies)


def guardar_dades_json(incidencies):
    """
    Guarda les dades en un fitxer JSON anomenat incidencies.json
    """
    json_file = 'incidencies.json'

    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(incidencies, f, ensure_ascii=False, indent=4)
        print(f"{Fore.GREEN}Dades guardades correctament a {json_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error en guardar les dades a l'arxiu JSON: {e}")


# Ruta de l'arxiu XML
xml_file = './datos.xml'

# Executa la funció per llegir, mostrar i guardar les dades
llegir_i_mostrar_dades(xml_file)