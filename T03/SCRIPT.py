import xml.etree.ElementTree as ET
import json
from colorama import init, Fore, Style
from datetime import datetime

# Inicialitza colorama per als colors en la consola
init(autoreset=True)

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
    Llegeix i analitza l'arxiu XML, mostra les dades per consola i les guarda en un fitxer JSON.
    """
    # Llegeix i analitza l'arxiu XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Llista per emmagatzemar les incidències
    incidencies = []
    resum = {}

    # Itera sobre cada fila (row) en l'XML
    for i, row in enumerate(root.findall('row')):
        print(f"{Fore.YELLOW + Style.BRIGHT}Incidència {i + 1}{Style.RESET_ALL}")

        # Diccionari per emmagatzemar cada incidència
        incidencia = {}
        nivell_urgencia = ""
        aula = ""

        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text if element.text else "No disponible"
            incidencia[etiqueta] = valor  # Emmagatzema l'etiqueta i el valor al diccionari

            # Afegeix color segons el tipus d'informació
            if etiqueta == "Nivell urgencia de solució":
                nivell_urgencia = valor
                color = Fore.RED if "Molt Urgent" in valor else Fore.YELLOW if "Urgent" in valor else Fore.GREEN
                print(f"\t{color}{etiqueta}: {valor}{Style.RESET_ALL}")
            else:
                print(f"\t{Fore.CYAN}{etiqueta}: {Fore.WHITE}{valor}{Style.RESET_ALL}")

            if etiqueta == "Aula":
                aula = valor

        # Validar incidència
        if nivell_urgencia and aula in aules_valides:
            incidencies.append(incidencia)
            # Actualitzar resum
            data = datetime.now().strftime("%Y-%m-%d")
            if data not in resum:
                resum[data] = {"total": 0, "urgentes": 0}
            resum[data]["total"] += 1
            if "Molt Urgent" in nivell_urgencia or "Urgent" in nivell_urgencia:
                resum[data]["urgentes"] += 1

        print("-" * 80)

    # Guarda el resum en JSON
    guardar_dades_json(resum)


def guardar_dades_json(resum):
    """
    Guarda el resum en un fitxer JSON anomenat resum_incidencies.json
    """
    json_file = 'resum_incidencies.json'

    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(resum, f, ensure_ascii=False, indent=4)
        print(f"{Fore.GREEN}Dades guardades correctament a {json_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error en guardar les dades a l'arxiu JSON: {e}")


# Ruta de l'arxiu XML
xml_file = './datos.xml'

# Executa la funció per llegir, mostrar i guardar les dades
llegir_i_mostrar_dades(xml_file)
