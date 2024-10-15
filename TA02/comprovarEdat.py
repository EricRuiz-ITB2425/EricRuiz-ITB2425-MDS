"""
Eric Ruiz Fernandez
27/9/2024
ASIXcB MDS TA03
Descripció: Comprovar Edat
"""


#Programa que demana la edat i diu si ets major d'edat.

from datetime import datetime

AquestAny = datetime.now().year
AquestMes = datetime.now().month
AquestDia = datetime.now().day

dia = int(input("Quin dia vas neixer?"))
mes = int(input("Quin mes vas neixer?"))
any = int(input("Quin any vas neixer?"))

try:
    if any <= AquestAny:
        if mes >= 1 and mes <=12:
            if dia >= 1 and dia <= 31:
                print("Calculant...")
                edat = AquestAny-any
                if edat >= 16 and edat <= 65:
                    print("Pots treballar.")
                else:
                    print("No pots treballar.")
    else:
        print("Any no valid")

except:
    print("Error")

#PROVA COMMIT