"""
Aqui se va a ejecutar lo principal del programa
"""
#-----------------------------Librerias-------------------------------------
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import calendar
from calendar import weekday
from datetime import timedelta
from tkinter import font, Toplevel



#--------------------------Ventana Grafica & configuraciones-----------------------------
ventana_principal=tk.Tk()
#Configuracion de la ventana principal
ventana_principal.geometry("1536x815+0+0")
#ventana_principal.maxsize(1536,816)
ventana_principal.maxsize(1920,1080)
ventana_principal.minsize(1280,720)
ventana_principal.iconbitmap("icono_principal.ico")
ventana_principal.config(bg="#212121")
ventana_principal.title("Ventana principal")
#para quitar la barra de las pestaña blanca fea
ventana_principal.overrideredirect(False)
ventana_principal.attributes("-topmost", False)
ventana_principal.attributes("-fullscreen", False)
#__________________________________________variables------------------------------------------------------
frame_dias = None
#-----------------------Creacion de los frames---------------------------------------------------
# Frame barra principal
Barra_principal_ventana = tk.Frame (ventana_principal, bg="#212121", bd=2, height= 30)
Barra_principal_ventana.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Titulo del programa
Titulo_Programa= tk.Label(Barra_principal_ventana,
                          text= "Habit Tracker- by Edmolinz ", fg="white", bg="#212121", font= ("Inter",12))
Titulo_Programa.pack(side="left", padx=5)
# Botones
Boton_cerrar = tk.Button(Barra_principal_ventana, text="✖", bg="#212121", fg="white",
                         font= ("Inter",12), command= ventana_principal.destroy, borderwidth=0)
Boton_cerrar.pack(side="right", padx=5)
# Botón de minimizar
#def minimizar():
   # ventana_principal.state("iconic")

#btn_minimizar = tk.Button(Barra_principal_ventana, text="_", bg="yellow", command=minimizar)
#btn_minimizar.pack(side="right", padx=5)
# --------------------Frame barra titulo----------------------------------
Frame_Barra_titulo = tk.Frame (ventana_principal, bg="#171717", bd=0, width=100, height=10)
Frame_Barra_titulo.grid(column=0, row = 1, columnspan= 2,  sticky="new" )
#Labels
# Agregar icono
imagen_icono = Image.open("icono_principal.png")
redimension= imagen_icono.resize((120,120), Image.Resampling.LANCZOS)
icono_app = ImageTk.PhotoImage(redimension)
icono_label = tk.Label(Frame_Barra_titulo, image=icono_app, bg="#171717")
icono_label.pack(side="left",padx=5)
#titulo
titulo_app = tk.Label(Frame_Barra_titulo,
                          text= "Habit Tracker",
                      fg="white", bg="#171717", font= ("Inter",50), height = 2)
titulo_app.pack(side="left")

#------------------------------------- Frames-appp ------------------------------------

#-----------------------------------Frame lista habitos------------------------------
Frame_habitos = tk.Frame (ventana_principal, bg="white", width= 1536/3)
Frame_habitos.grid(column=0, row = 2,  sticky="nsew" )





#-----------------------------------Frame grafico semanal------------------------------
Frame_grafico_semanal = tk.Frame (ventana_principal,bg="blue", width=1536/3*2)
Frame_grafico_semanal.grid (column=1, row =2, sticky ="nsew")
Frame_semanal_fecha = tk.Frame(Frame_grafico_semanal,bg="#171717")
Frame_semanal_fecha.pack(fill="x")
#---------------------------------Fechas---------------------------------------------
"""
Este es el codigo para crear las fechas de la semana en corriente en la
interfaz gráfica
"""
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
if dia_semana_domingo == 0:
    dia =" Domingo "
elif dia_semana_domingo == 1:
    dia = " Lunes "
elif dia_semana_domingo == 2:
    dia = " Martes "
elif dia_semana_domingo == 3:
    dia = " Miercoles "
elif dia_semana_domingo == 4:
    dia = " Jueves "
elif dia_semana_domingo == 5:
    dia = " Viernes "

elif dia_semana_domingo == 6:
    dia = " Sábado "
texto_semana_encabezado = "Semana " + str(semana_corriente)
texto_dia_encabezado = "HOY" + dia + str(dia_hoy)

label_fecha_hoy = tk.Label(Frame_semanal_fecha, text=texto_dia_encabezado, bg="#171717", fg="white",
                         font= ("Inter",25))
label_fecha_hoy.pack(side="left" ,  pady=5,padx=5)
label_semana_corriente = tk.Label(Frame_semanal_fecha, text=texto_semana_encabezado, bg="#171717", fg="white",
                         font= ("Inter",25))
label_semana_corriente.pack(side="right",padx=30, pady=5)
#-------------------------------Tabla dias semana-------------------------------------------
Frame_dias_actuales = tk.Frame(Frame_grafico_semanal,bg="pink" )
#-------------------------------Boton añadir habito & funcion para abrir nueva ventana------

def abrir_ventana_crear_habito(icono_app):
    #Creamos una ventana top level y lo creamos en la ventana principal
    ventana_crear_habito = Toplevel(ventana_principal)
    ventana_crear_habito.title("Habit Tracker-Crear habito")
    ventana_crear_habito.geometry("1536x815+0+0")
    # ventana_principal.maxsize(1536,816)
    ventana_crear_habito.maxsize(1920, 1080)
    ventana_crear_habito.minsize(1280, 720)
    ventana_crear_habito.iconbitmap("icono_principal.ico")
    ventana_crear_habito.config(bg="#212121")
    ventana_crear_habito.overrideredirect(True)

    # -----------------------Creacion de los frames--- ventana habito--------------------------------------------------
    # Frame barra principal
    Barra_principal_ventana_crear_habito = tk.Frame(ventana_crear_habito, bg="#212121", bd=2, height=30)
    Barra_principal_ventana_crear_habito.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Titulo del programa
    Titulo_Programa = tk.Label(Barra_principal_ventana_crear_habito,
                               text="Habit Tracker- by Edmolinz ", fg="white", bg="#212121", font=("Inter", 12))
    Titulo_Programa.pack(side="left", padx=5)
    # Botones Regresar*
    Boton_cerrar = tk.Button(Barra_principal_ventana_crear_habito, text="⬅", bg="#212121", fg="white",
                             font=("Inter", 12), command=ventana_crear_habito.destroy, borderwidth=0)
    Boton_cerrar.pack(side="right", padx=5)
    #----------------------Frame icono y titulo-------------------------------------------------------------------
    Frame_Barra_titulo_v_crear_habito = tk.Frame(ventana_crear_habito, bg="#171717", bd=0, width=100, height=10)
    Frame_Barra_titulo_v_crear_habito.grid(column=0, row=1, columnspan=2, sticky="new")
    # Labels
    # Agregar icono
    #imagen_icono = Image.open("icono_principal.png")
    #redimension = imagen_icono.resize((120, 120), Image.Resampling.LANCZOS)
    #icono_app = ImageTk.PhotoImage(redimension)
    icono_label = tk.Label(Frame_Barra_titulo_v_crear_habito, image=icono_app, bg="#171717")
    icono_label.pack(side="left", padx=5)
    # titulo
    titulo_app = tk.Label(Frame_Barra_titulo_v_crear_habito,
                          text="Habit Tracker",
                          fg="white", bg="#171717", font=("Inter", 50), height=2)
    titulo_app.pack(side="left")
    ventana_crear_habito.grid_columnconfigure(0, weight=1)
    ventana_crear_habito.grid_columnconfigure(1, weight=1)
    ventana_crear_habito.grid_rowconfigure(0, weight=0)
    ventana_crear_habito.grid_rowconfigure(2, weight=1)

    #-------------------------Crear habito frame-------------------------------------------------------------------

    Frame_crear_habito = tk.Frame(ventana_crear_habito, bg="#171717")
    Frame_crear_habito.grid(column= 0, row =2, sticky= "nsew")

    # label texto crear habito
    label_crear_habito = tk.Label(Frame_crear_habito,  text = "Crear habito",fg="white", bg="#171717", font=("Inter", 25), height=2)
    label_crear_habito.pack(anchor ="nw" , padx = 10, pady= 5 )
    # Entrada de como se llamara el habito
    def on_entry_click(event):
        if Entrada_nombre_nuevo_habito.get() == default_text:
            Entrada_nombre_nuevo_habito.delete(0, tk.END)  # Borra el texto
            Entrada_nombre_nuevo_habito.config(fg="white")  # Cambia el color del texto

    def on_focus_out(event):
        if Entrada_nombre_nuevo_habito.get() == "":
            Entrada_nombre_nuevo_habito.insert(0, default_text)  # Restaura el texto predeterminado
            Entrada_nombre_nuevo_habito.config(fg="gray")  # Cambia el color del texto

    default_text ="Nombre de tu habito"
    Entrada_nombre_nuevo_habito= tk.Entry(Frame_crear_habito, text ="Nombre de habito", fg= "white", bg="#2f2f2f",
                                          font=("Inter", 20))
    Entrada_nombre_nuevo_habito.insert(0, default_text)
    Entrada_nombre_nuevo_habito.bind("<FocusIn>", on_entry_click)
    Entrada_nombre_nuevo_habito.bind("<FocusOut>", on_focus_out)
    Entrada_nombre_nuevo_habito.pack(anchor="nw", padx =20, pady=5)
    #-----------------------------------Configuracion de habito frame--------------------------------------------------
    Frame_config_habito =tk.Frame(ventana_crear_habito, bg="red")
    Frame_config_habito.grid(column=1,row =2, sticky ="nsew")
    #label elegir dias
    label_seleccionar_dias =tk.Label(Frame_config_habito,  text = "Selecciona los dias que quieres realizar el habito",
                                     fg="white", bg="#171717", font=("Inter", 25), height=2)
    label_seleccionar_dias.pack(anchor= "nw", padx= 10, pady=5 )
    opcion =tk.IntVar(value=0)
    opcion_valor = opcion.get()
    Radio_boton_opcion_dias =tk.Radiobutton(Frame_config_habito, text= "Todos los días" ,fg="white", bg="#171717",
                                            font=("Inter", 25), variable=opcion, value=1,selectcolor="#171717")
    Radio_boton_opcion_dias.pack(anchor ="nw", padx= 10, pady =5)
    #-----------------------------------------funcion para mostrar los dias a seleccionar-------------------------------

    def mostrar_frame_dias():
        global frame_dias
        if  frame_dias is None:

            frame_dias = tk.Frame(Frame_config_habito, bg="#171717")
            frame_dias.pack(anchor="nw", padx=10, pady=5)
            dias_semana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            # tabla para guardar el valro de las variable seleccionadas
            variables = []
            for indice, dia in enumerate(dias_semana):
                # definir que la variable es un entero y se guardara en "variable"
                variable = tk.IntVar(value=0)
                # agregamos "variable" a la tabla
                variables.append(variable)
                tk.Checkbutton(frame_dias, text=dia, variable=variable).grid(column=indice, row=0)


    #-----------------------------------------------Radiobotones para seleccionar dias----------------------------------
    Radio_boton_opcion_dias_esp = tk.Radiobutton(Frame_config_habito,text= "Dias especificos" ,fg="white", bg="#171717",
                                                 font=("Inter", 25),variable=opcion, value=2,selectcolor="#171717",
                                                 command= mostrar_frame_dias )
    Radio_boton_opcion_dias_esp.pack(anchor ="nw", padx= 10, pady =5)

    #------------------------------------------Boton guardar------------------------------------------------------------
    Boton_guardar_habito = tk.Button(Frame_config_habito, text= "Guardar" ,fg="white", bg="#171717",
                                            font=("Inter", 25))
    Boton_guardar_habito.pack(anchor="sw", pady=5,padx=10)

#--------------------------------------------Boton------------------------------------------------------------------
Boton_añadir_habito = tk.Button(Frame_dias_actuales, text="+",fg="white", bg="#171717",
                                font= ("Inter",10), height = 2 , width= 17, command =lambda :abrir_ventana_crear_habito(icono_app))
Boton_añadir_habito.grid(column=0,row=0, sticky ="w")

#ahora que ya tenemos el inicio de la semana simplemente hay que iterar
# Los dias de la semana corriente
fuente_negritas = font.Font(family="Inter", size= 13, weight= "bold")
dias_semana_corriente =  [  domingo + timedelta(days=i) for i in range(7)]
for i, Dia in enumerate(dias_semana_corriente):
    label_dia = tk.Label(Frame_dias_actuales, text=Dia.day, width=12, font=fuente_negritas, bg="#171717", fg="white")
    label_dia.grid(row=0, column= i+1, sticky ="nsew")
    label_dia.grid_columnconfigure(i+1, weight=1)
label_dia.grid_rowconfigure(0,weight=1)
# se crea el frame
Frame_dias_actuales.pack(fill="x")



#-----------Columnas redimensionable----------------------------
ventana_principal.grid_columnconfigure(0,weight=1)
ventana_principal.grid_columnconfigure(1,weight=1)
ventana_principal.grid_rowconfigure(0,weight=0)
ventana_principal.grid_rowconfigure(2,weight=1)


ventana_principal.mainloop()