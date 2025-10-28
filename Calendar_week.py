"""
Este es el codigo para crear las fechas de la semana en corriente en la
interfaz gráfica
Clase calendario
"""
import datetime
import calendar
from calendar import weekday
from datetime import timedelta

#Guardamos la fecha del dia de hoy completa
fecha_hoy=datetime.datetime.now()
#guardamos UNICAMENTE la fecha del DIA de hoy
dia_hoy= fecha_hoy.day
# Guardamos UNICAMENTE el numero de semana en el que nos encontramos
semana_corriente= fecha_hoy.isocalendar().week
#Guardamos el nombre o indice del dia donde Lunes = 0,----- Domingo =6
numero_dia = fecha_hoy.weekday()

#Aqui cambiamos el inicio de la semana a domingo
dia_semana_domingo= (fecha_hoy.weekday()+1) % 7
# aqui calculamos el dia de inicio de semana que seria el domingo
domingo = fecha_hoy-timedelta(days=dia_semana_domingo)
#print(domingo.day)
#print(domingo.isocalendar().week)

#ahora que ya tenemos el inicio de la semana simplemente hay que iterar
# Los dias de la semana corriente

dias_semana_corriente =  [  domingo + timedelta(days=i) for i in range(7)]
def imprimir_fechas():
        print("Estamos en la semana :")
        print( dias_semana_corriente[1].isocalendar().week)
        print("Los dias de la semana actual son: ")
        for dia_semana_corriente in dias_semana_corriente :

            print(dia_semana_corriente.day)


imprimir_fechas()