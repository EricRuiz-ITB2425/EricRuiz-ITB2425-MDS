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
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

init(autoreset=True)


def llegir_i_mostrar_dades(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    incidencies = []

    for i, row in enumerate(root.findall('row')):
        print(f"{Fore.YELLOW + Style.BRIGHT}Incidència {i + 1}{Style.RESET_ALL}")
        incidencia = {}
        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text if element.text else "No disponible"

            incidencia[etiqueta] = valor

            if etiqueta == "Nivell urgencia de solució":
                color = Fore.RED if "Molt Urgent" in valor else Fore.YELLOW if "Urgent" in valor else Fore.GREEN
                print(f"\t{color}{etiqueta}: {valor}{Style.RESET_ALL}")
            else:
                print(f"\t{Fore.CYAN}{etiqueta}: {Fore.WHITE}{valor}{Style.RESET_ALL}")
        print("-" * 80)

        incidencies.append(incidencia)

    guardar_dades_json(incidencies)


def seleccionar_archivo():
    Tk().withdraw()
    archivo_seleccionado = askopenfilename(
        title="Selecciona un archivo XML",
        filetypes=[("Archivos XML", "*.xml")]
    )
    return archivo_seleccionado


def guardar_dades_json(incidencies):

    Tk().withdraw()
    json_file = asksaveasfilename(
        title="Guardar archivo como...",
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        initialfile="hobbies.json"
    )

    if json_file:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(incidencies, f, ensure_ascii=False, indent=4)
        print(f"{Fore.GREEN}Dades guardades correctament a {json_file}{Style.RESET_ALL}")
    else:
        print("No se ha seleccionado ningún archivo para guardar.")


xml_file = seleccionar_archivo()

if xml_file:
    llegir_i_mostrar_dades(xml_file)
else:
    print("No se ha seleccionado ningún archivo.")