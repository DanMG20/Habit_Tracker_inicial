"""
Logica de programacion para crear hábitos, etc
"""
import json
from datetime import datetime


# Lista donde se almacenan los hábitos misma que vamos a guardar en el archivo JSON
habitos = [
    {
        "nombre_habito":"Comer sano"
    },
]

def crear_habito(habitos, nombre_habito_nuevo ,dias_ejecucion):
    for habito in habitos:
        nombre2 = habito["nombre_habito"]
        for nombre_habito in habito:
            if nombre_habito_nuevo in nombre_habito:
                print("El habito ya existe")
            else:

                #guardar fecha
                Fecha_creacion = datetime.now().date()
                # Funcion para crear un hábito
                habito = {"nombre_habito":nombre_habito_nuevo,
                          "dias_ejecucion":dias_ejecucion,
                          "Fecha_creacion":Fecha_creacion
                          }
            print("el habito a sido creado")
        return habitos.append(habito)

nombre_habito_nuevo=input("Ingresa tu nuevo habito:")
dias_ejecucion =  [1,2,3,4,5]

crear_habito(habitos, nombre_habito_nuevo,dias_ejecucion)

print(habitos)