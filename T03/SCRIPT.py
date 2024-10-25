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

    # Data actual per validar la data de la incidència
    data_actual = datetime.now()

    # Itera sobre cada fila (row) en l'XML
    for i, row in enumerate(root.findall('row')):
        print(f"{Fore.YELLOW + Style.BRIGHT}Incidència {i + 1}{Style.RESET_ALL}")

        # Diccionari per emmagatzemar cada incidència
        incidencia = {}
        motius_no_valides = []  # Llista per motius de no validesa

        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text.strip() if element.text else "No disponible"
            incidencia[etiqueta] = valor  # Emmagatzema l'etiqueta i el valor al diccionari

        # Comprovació de validacions
        correu = incidencia.get('Adreça electrònica', '')
        nom_cognoms = incidencia.get('Nom i cognoms', '')
        aula = incidencia.get('Lloc aula ex aula 208 ', '')
        data_incidencia = incidencia.get('Data de la incidència', '')

        # Comprovar si el correu electrònic és vàlid
        if not correu.endswith('@itb.cat') or not correu.split('@')[0].replace('.', ' ').strip().lower() == nom_cognoms.lower():
            motius_no_valides.append("Correu electrònic no vàlid.")

        # Comprovar si l'aula és vàlida
        if aula not in aules_valides:
            motius_no_valides.append("Aula no vàlida.")

        # Comprovar si la data de la incidència és vàlida
        try:
            data_incidencia_dt = datetime.strptime(data_incidencia, '%d/%m/%Y')
            if data_incidencia_dt > data_actual or data_incidencia_dt < (data_actual.replace(year=data_actual.year - 1)):
                motius_no_valides.append("Data de la incidència no vàlida.")
        except ValueError:
            motius_no_valides.append("Format de data incorrecte.")

        # Afegir motius no vàlids i imprimir la informació
        if motius_no_valides:
            print(f"Incidència {i + 1} no vàlida: {', '.join(motius_no_valides)}")
            print(f"Detalls: {incidencia}")  # Mostrar informació de la incidència
        else:
            print(f"{Fore.GREEN}Incidència {i + 1} vàlida.{Style.RESET_ALL}")

        print("-" * 80)

    # Després de processar totes les incidències, guarda-les en un fitxer JSON
    guardar_dades_json(incidencies)


def guardar_dades_json(incidencies):
    """
    Guarda les dades en un fitxer JSON anomenat incidencies.json.
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