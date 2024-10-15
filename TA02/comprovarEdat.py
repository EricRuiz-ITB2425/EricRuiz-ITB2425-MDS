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


while True:
    if dia > 31:
        print("dia no valid")
    elif dia > 31:
        print("Dia no valid")
        break

    if mes > 12:
        print("mes no valid")
    elif mes > 12:
        print("Mes no valid")
        break

    if any > 2024:
        print("mes no valid")
        producte: int = any-AquestAny
    elif any > 2024:
        print("Any no valid")
        break

any - AquestAny = edat


print(edat)






'''
edat=int(input("Quina edat tens?"))
if edat>=18:
    print("Ets major d'edat")
print("Programa Finalitzat")


#PROVA COMMIT
'''