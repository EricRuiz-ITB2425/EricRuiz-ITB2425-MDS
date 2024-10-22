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
from PyQt5.QtWidgets import QApplication, QFileDialog

# Inicializa colorama para los colores en la consola
init(autoreset=True)


import xml.etree.ElementTree as ET
from colorama import init, Fore, Style

# Inicialitza colorama per als colors en la consola
init(autoreset=True)


def llegir_i_mostrar_dades(xml_file):
    # Llegeix i analitza l'arxiu XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Itera sobre cada fila (row) en l'XML
    for i, row in enumerate(root.findall('row')):
        print(f"{Fore.YELLOW + Style.BRIGHT}Incidència {i + 1}{Style.RESET_ALL}")
        for element in row:
            etiqueta = element.tag.replace('_', ' ').capitalize()
            valor = element.text if element.text else "No disponible"

            # Afegeix color segons el tipus d'informació
            if etiqueta == "Nivell urgencia de solució":
                color = Fore.RED if "Molt Urgent" in valor else Fore.YELLOW if "Urgent" in valor else Fore.GREEN
                print(f"\t{color}{etiqueta}: {valor}{Style.RESET_ALL}")
            else:
                print(f"\t{Fore.CYAN}{etiqueta}: {Fore.WHITE}{valor}{Style.RESET_ALL}")
        print("-" * 80)


# Ruta de l'arxiu XML
xml_file = './datos.xml'

# Executa la funció per llegir i mostrar les dades
llegir_i_mostrar_dades(xml_file)

def seleccionar_archivo():
    """
    Permite al usuario seleccionar un archivo XML usando PyQt.
    """
    app = QApplication([])  # Crear la aplicación de PyQt
    archivo_seleccionado, _ = QFileDialog.getOpenFileName(
        None,
        "Selecciona un archivo XML",
        "",
        "Archivos XML (*.xml)"
    )
    return archivo_seleccionado


def guardar_dades_json(incidencias):
    """
    Guarda las incidencias en un archivo JSON seleccionado por el usuario.
    """
    app = QApplication([])  # Crear la aplicación de PyQt para el diálogo de guardado
    json_file, _ = QFileDialog.getSaveFileName(
        None,
        "Guardar archivo como...",
        "hobbies.json",
        "Archivos JSON (*.json)"
    )

    if json_file:  # Comprobar si se ha seleccionado un archivo
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(incidencias, f, ensure_ascii=False, indent=4)
            print(f"{Fore.GREEN}Datos guardados correctamente en {json_file}{Style.RESET_ALL}")
            mostrar_json(json_file)  # Mostrar el contenido del JSON después de guardarlo
        except Exception as e:
            print(f"Se ha producido un error al guardar el archivo: {e}")
    else:
        print("No se ha seleccionado ningún archivo para guardar.")


def mostrar_json(json_file):
    """
    Muestra el contenido del archivo JSON de manera amigable.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not data:
                print("El archivo JSON está vacío.")
                return

            print("\nContenido del archivo JSON:\n")
            for i, incidencia in enumerate(data, start=1):
                print(f"Incidencia {i}:")
                for key, value in incidencia.items():
                    print(f"  {key}: {value}")
                print("-" * 40)  # Línea separadora
    except FileNotFoundError:
        print(f"El archivo {json_file} no se ha encontrado.")
    except json.JSONDecodeError:
        print(f"Error al leer el archivo JSON {json_file}. Asegúrate de que está bien formado.")


# Pedir al usuario que seleccione el archivo XML
xml_file = seleccionar_archivo()

# Ejecutar la función para leer y mostrar los datos si se ha seleccionado un archivo
if xml_file:
    llegir_i_mostrar_dades(xml_file)
else:
    print("No se ha seleccionado ningún archivo.")