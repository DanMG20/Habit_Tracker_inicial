import tkinter as tk
import time
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import json
import os
from time import strftime
import calendar
import sys
from calendar import weekday
from datetime import timedelta
from tkinter import font, Toplevel, messagebox


class GUI:



    # -----------------------------------actualizar programa--------------------------------------------------------
    def actualizar_programa(self):
        print("El programa se ha actualizado")

        # Actualizar la fecha actual
        self.fecha_hoy = datetime.now()
        self.fecha_manana = self.fecha_hoy + timedelta(days=1)
        self.fecha_hoy_2 = datetime.now()

        # Actualizar encabezado de fecha y lista de hábitos
        self.show_week_days()
        self.lista_habitos_frame_semana()

        # Reprogramar la ejecución después de 60,000 ms (60 segundos)
        self.ventana_principal.after(60000, self.actualizar_programa)

    def calcular_rendimiento_semanal(self):
        """
        Calcula y guarda el rendimiento semanal de cumplimiento de hábitos en porcentaje.
        """
        ejecuciones = self.cargar_ejecuciones()

        # Ajustar el inicio de la semana al domingo
        inicio_semana = self.fecha_hoy - timedelta(days=(self.fecha_hoy.weekday() + 1) % 7)
        fin_semana = inicio_semana + timedelta(days=6)

        habitos_totales = 0
        habitos_cumplidos = 0

        for habit in self.habitos:
            # Iterar por cada día de la semana
            for dia_indic in range(7):
                dia_semana = inicio_semana + timedelta(days=dia_indic)
                dia_semana_str = dia_semana.strftime("%Y-%m-%d")
                dia_ejecucion = habit["dias_ejecucion"][dia_indic]

                if dia_ejecucion == 1:  # Día en el que el hábito debe ejecutarse
                    habitos_totales += 1
                    # Verificar si se cumplió
                    ejecucion = next(
                        (e for e in ejecuciones if
                         e["nombre_habito"] == habit["nombre_habito"] and e["fecha_ejecucion"] == dia_semana_str),
                        None
                    )
                    if ejecucion and ejecucion["completado"]:
                        habitos_cumplidos += 1

        # Calcular el porcentaje de cumplimiento
        rendimiento = (habitos_cumplidos / habitos_totales * 100) if habitos_totales > 0 else 0

        # Guardar el rendimiento semanal
        rendimiento_data = {
            "inicio_semana": inicio_semana.strftime("%Y-%m-%d"),
            "fin_semana": fin_semana.strftime("%Y-%m-%d"),
            "rendimiento": rendimiento
        }

        self.guardar_rendimiento_semanal(rendimiento_data)
        print(f"Rendimiento semanal: {rendimiento:.2f}%")
        return rendimiento

    def guardar_rendimiento_semanal(self, rendimiento_data):
        """
        Guarda el rendimiento semanal en un archivo JSON.
        """
        try:
            with open("rendimiento_semanal.json", "r") as file:
                rendimientos = json.load(file)
        except FileNotFoundError:
            rendimientos = []

        # Agregar el nuevo rendimiento
        rendimientos.append(rendimiento_data)

        # Guardar en el archivo
        with open("rendimiento_semanal.json", "w") as file:
            json.dump(rendimientos, file, indent=4)
        #--------------------------------funciones para el registro de ejecuciones---------------------------------------
    def cargar_ejecuciones(self):
        if not os.path.exists(("registro_habitos.json")):
            return[]
        try:
            with open('registro_habitos.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_ejecuciones(self,ejecuciones):
        with open('registro_habitos.json', 'w') as f:
            json.dump(ejecuciones, f, indent=4)

    def registrar_ejecucion_habito(self, nombre_habito):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        ejecuciones = self.cargar_ejecuciones()

        # Verificar si el hábito ya fue registrado hoy
        if any(ejec["nombre_habito"] == nombre_habito and ejec["fecha_ejecucion"] == fecha_actual for ejec in
               ejecuciones):
            messagebox.showinfo("Información", f"El hábito '{nombre_habito}' ya fue completado hoy.")
            return

        # Agregar nuevo registro
        nuevo_registro = {
            "nombre_habito": nombre_habito,
            "fecha_ejecucion": fecha_actual,
            "completado": True
        }
        ejecuciones.append(nuevo_registro)

        # Guardar actualizaciones
        self.guardar_ejecuciones(ejecuciones)
        self.lista_habitos_frame_semana()
        messagebox.showinfo("Éxito", f"Se registró como completado el hábito '{nombre_habito}' para hoy.")

    def registrar_ejecucion_habito_dia_anterior(self, nombre_habito):
        fecha_dia_anterior = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
        ejecuciones = self.cargar_ejecuciones()

        # Verificar si el hábito ya fue registrado hoy
        if any(ejec["nombre_habito"] == nombre_habito and ejec["fecha_ejecucion"] == fecha_dia_anterior for ejec in
               ejecuciones):
            messagebox.showinfo("Información", f"El hábito '{nombre_habito}' ya fue completado hoy.")
            return

        # Agregar nuevo registro
        nuevo_registro = {
            "nombre_habito": nombre_habito,
            "fecha_ejecucion": fecha_dia_anterior,
            "completado": True
        }
        ejecuciones.append(nuevo_registro)

        # Guardar actualizaciones
        self.guardar_ejecuciones(ejecuciones)
        self.lista_habitos_frame_semana()
        messagebox.showinfo("Éxito", f"Se registró como completado el hábito '{nombre_habito}' para el día de ayer.")

    #-------------------------------Para cargar la base de datos-----------------------------------------------------
    def cargar_habitos(self):
        if not os.path.exists("Base_de_datos_habitos.json"):
            return []
        with open("Base_de_datos_habitos.json", "r") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                print("Archivo corrupto, voy a reescribir el archivo")
                return []

    # Guarda la información en el archivo JSON
    def guardar_habitos(self,habitos):
        with open("Base_de_datos_habitos.json", "w") as archivo:
            json.dump(habitos, archivo, indent=4)

    # Función para crear un hábito
    def crear_habito(self,habitos, nombre_habito_nuevo, dias_ejecucion):
        # Guardar fecha
        fecha_creacion = datetime.now().date()
        fecha_creacion_string = str(fecha_creacion)
        dias_ejecucion_valores = [var.get() for var in dias_ejecucion]

        # Verificamos si el hábito ya existe
        for habito in habitos:
            if nombre_habito_nuevo == habito["nombre_habito"]:
                print("Este hábito ya existe, intenta con otro nombre.")

                return

        # Si el hábito no existe, lo creamos
        habito = {
            "nombre_habito": nombre_habito_nuevo,
            "dias_ejecucion": dias_ejecucion_valores,
            "Fecha_creacion": fecha_creacion_string
        }
        habitos.append(habito)
        self.guardar_habitos(habitos)
        self.lista_habitos()
        self.lista_habitos_frame_semana()

        print(f"El hábito '{nombre_habito_nuevo}' ha sido creado con éxito.")
    #----------------------------------------------------GUI-----------------------------------------------------------
    def abrir_ventana_eliminar_habito(self):

        self.ventana_borrar_habito = Toplevel(self.ventana_principal)
        self.ventana_borrar_habito.state("zoomed")
        self.ventana_borrar_habito.title("Habit Tracker-Crear habito")
        self.ventana_borrar_habito.geometry("1536x815")
        # ventana_principal.maxsize(1536,816)
        self.ventana_borrar_habito.maxsize(1920, 1080)
        self.ventana_borrar_habito.minsize(1280, 720)
        self.ventana_borrar_habito.config(bg=self.color_fondo)
        self.ventana_borrar_habito.overrideredirect(True)
        # -----------------------Creacion de los frames--- ventana habito--------------------------------------------------
        # Frame barra principal
        Barra_principal_ventana_borrar_habito = tk.Frame(self.ventana_borrar_habito, bg=self.color_fondo, bd=2, height=30)
        Barra_principal_ventana_borrar_habito.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Titulo del programa
        Titulo_Programa = tk.Label(Barra_principal_ventana_borrar_habito,
                                   text="Habit Tracker- by Edmolinz ", fg=self.color_texto, bg=self.color_fondo,
                                   font=self.font_body)
        Titulo_Programa.pack(side="left", padx=5)
        # Botones Regresar*
        Boton_cerrar = tk.Button(Barra_principal_ventana_borrar_habito, text="⬅", bg=self.color_fondo,
                                 fg=self.color_texto,
                                 font=self.font_body, command=self.ventana_borrar_habito.destroy, borderwidth=0)
        Boton_cerrar.pack(side="right", padx=5)
        # ----------------------Frame icono y titulo-------------------------------------------------------------------
        Frame_Barra_titulo_v_borrar_habito = tk.Frame(self.ventana_borrar_habito, bg=self.color_encabezado, bd=0,
                                                     width=100, height=10)
        Frame_Barra_titulo_v_borrar_habito.grid(column=0, row=1, columnspan=2, sticky="new")
        # Labels
        # Agregar icono
        # imagen_icono = Image.open("icono_principal.png")
        # redimension = imagen_icono.resize((120, 120), Image.Resampling.LANCZOS)
        # icono_app = ImageTk.PhotoImage(redimension)
        icono_label = tk.Label(Frame_Barra_titulo_v_borrar_habito, image=self.icono_app, bg=self.color_encabezado)
        icono_label.pack(side="left", padx=5)
        # titulo
        titulo_app = tk.Label(Frame_Barra_titulo_v_borrar_habito,
                              text="Habit Tracker",
                              fg=self.color_texto, bg=self.color_encabezado, font=self.font_title, height=2)
        titulo_app.pack(side="left")
        self.ventana_borrar_habito.grid_columnconfigure(0, weight=1)
        self.ventana_borrar_habito.grid_columnconfigure(1, weight=1)
        self.ventana_borrar_habito.grid_rowconfigure(0, weight=0)
        self.ventana_borrar_habito.grid_rowconfigure(2, weight=1)

        # -------------------------Crear habito frame-------------------------------------------------------------------
        # Frame principal para eliminar hábito
        frame_borrar_habito = tk.Frame(self.ventana_borrar_habito, bg=self.color_encabezado,
                                       borderwidth=1,
                                       highlightbackground=self.color_borde,
                                       highlightthickness=1)
        frame_borrar_habito.grid(column=0, row=2, sticky="nsew")

        # Label para indicar acción
        label_borrar_habito = tk.Label(frame_borrar_habito, text="Elige el hábito que quieres borrar",
                                       fg=self.color_texto,
                                       bg=self.color_encabezado, font=self.font_body, height=2)
        label_borrar_habito.pack(fill="x")

        # Listar hábitos con botones para eliminar
        if not self.habitos:
            tk.Label(frame_borrar_habito, text="No hay hábitos registrados.",
                     bg=self.color_celda_activa, fg=self.color_texto,
                     font=self.font_subtitle_helvetica).pack(pady=5)
        else:
            for habit in self.habitos:
                tk.Button(
                    frame_borrar_habito,
                    text=habit["nombre_habito"],
                    bg=self.color_celda_activa,
                    fg=self.color_texto,
                    font=self.font_subtitle_helvetica,
                    activebackground=self.color_celda_activa,
                    relief="flat",
                    command=lambda h=habit["nombre_habito"]: self.eliminar_habito_directo(h)
                ).pack(fill="x", pady=1, padx=2)
        #--------------------------------------------------------------------------------------------------------
    def eliminar_habito_directo(self, habit_seleccionado):
        """Elimina directamente el hábito seleccionado."""
        confirmacion = messagebox.askyesno(
            "Confirmación",
            f"¿Estás seguro de que deseas eliminar el hábito '{habit_seleccionado}'?"
        )
        if confirmacion:
            self.habitos = [habito for habito in self.habitos if habito["nombre_habito"] != habit_seleccionado]
            self.guardar_habitos(self.habitos)
            self.lista_habitos()
            self.ventana_borrar_habito.destroy()
            messagebox.showinfo("Éxito", f"El hábito '{habit_seleccionado}' ha sido eliminado.")

    def resource_path(self,relative_path):
        """Obtén la ruta de un recurso, compatible con PyInstaller."""
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def __init__(self,ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Habbit Tracker - By Edmolinz")

        self.ventana_principal.geometry("1536x815")
        self.font_title = ("Inter",50,"bold")
        # Guardamos la fecha del dia de hoy completa
        self.fecha_hoy = datetime.now()
        self.fecha_hoy_2 =datetime.now()
        self.fecha_manana = datetime.now()+ timedelta ( days =1) # para corregir la semana
        self.font_body =("Times New Roman", 12)
        self.color_fondo = "#121212"  # Fondo principal
        self.color_texto = "#FFFFFF"  # Texto principal
        self.color_encabezado = "#1F1F1F"  # Fondo de encabezados
        self.color_borde = "#0078D7"  # Bordes azules
        self.color_celda_activa = "#333333"  # Celdas activas
        self.color_celda_inactiva = "#1E1E1E"  # Celdas inactivas
        self.color_completado = "#03DAC6"  # Color para celdas completadas
        self.color_boton_activo = "#0078D7"  # Fondo de botones activos
        self.color_boton_hover = "#005EA6"  # Fondo de botones al pasar el mouse
        self.color_fondo_inferior = "#1A1A1A"  # Fondo inferior
        self.font_subtitle= ("Inter",30,"bold")
        self.font_subtitle_helvetica = ("Helvetica", 12, "bold")



        # Usa la función para acceder al archivo
        self.icono = self.resource_path('icono_principal.png')

        self.habitos = self.cargar_habitos()
        self.configuracion()

        # Inicia la función de actualización periódica
        self.actualizar_programa()

    def lista_habitos(self):
        """Lista los nombres de los hábitos en el marco."""
        # Limpiar el marco para evitar duplicados
        for widget in self.frame_habitos.winfo_children():
            widget.destroy()

        if not self.habitos:
            tk.Button(
                self.frame_habitos,
                text="No hay hábitos registrados.",
                bg=self.color_celda_activa,
                fg=self.color_texto,
                font=self.font_subtitle_helvetica
            ).pack(pady=5)
        else:
            for habit in self.habitos:
                tk.Button(
                    self.frame_habitos,
                    text=habit["nombre_habito"],
                    bg=self.color_celda_activa,
                    fg=self.color_texto,
                    font=self.font_subtitle_helvetica,
                    activebackground=self.color_celda_activa,
                    relief="flat",
                    command=lambda h=habit["nombre_habito"]: self.registrar_ejecucion_habito(h)
                ).pack(fill= "x",pady=1,padx=2)

    def lista_habitos_frame_semana(self):
        """
        Muestra los hábitos junto con los días de la semana.
        Los días se marcan como ✔ si el hábito se ejecutó, X si no se ejecutó,
        un espacio vacío si aún no se registra, y - si no aplica el día.
        """
        ejecuciones = self.cargar_ejecuciones()


        # Ajustar el inicio de la semana al domingo
        inicio_semana = self.fecha_hoy - timedelta(days=(self.fecha_hoy.weekday() + 1) % 7)

        # Limpiar el marco para evitar duplicados, pero no destruir los encabezados
        for widget in self.frame_habitos_lista_ejec.winfo_children():
            if widget.winfo_class() != "Label":  # Asegurarse de no destruir los encabezados
                widget.destroy()

        # Crear los hábitos en la fila correspondiente (empieza desde fila 1)
        for indic, habit in enumerate(self.habitos):
            # Mostrar el nombre del hábito
            tk.Label(
                self.frame_habitos_lista_ejec,
                text=habit["nombre_habito"],
                bg=self.color_encabezado,
                fg=self.color_texto,
                font=("Helvetica", 12, "bold"),
                relief="solid",
                borderwidth=1,
                highlightbackground=self.color_borde,
                highlightthickness=1,
                width= 35,
            ).grid(column=0, row=indic + 1, padx=1, sticky="nsew")  # Fila indic + 1 para empezar desde la fila 1

            # Mostrar los días de ejecución para cada hábito
            for dia_indic in range(7):  # Del domingo (0) al sábado (6)
                dia_semana = inicio_semana + timedelta(days=dia_indic)
                dia_semana_str = dia_semana.strftime("%Y-%m-%d")
                dia_ejecucion = habit["dias_ejecucion"][dia_indic]

                # Inicializar font_style antes de cualquier uso
                font_style = ("Helvetica", 12, "normal")  # Por defecto

                # Comparar con las ejecuciones registradas
                if dia_ejecucion == 0:
                    texto = "-"  # Día en el que no se ejecuta el hábito
                    color_celda = self.color_celda_inactiva
                    color_texto = self.color_texto
                    font_style = ("Helvetica", 14, "bold")  # Guiones más anchos
                else:
                    ejecucion = next(
                        (e for e in ejecuciones if
                         e["nombre_habito"] == habit["nombre_habito"] and e["fecha_ejecucion"] == dia_semana_str),
                        None
                    )
                    if ejecucion:
                        if ejecucion["completado"]:
                            texto = "✔"  # Palomita verde
                            color_celda = self.color_celda_activa
                            color_texto = "green"  # Color verde para la palomita
                        else:
                            texto = "✖"  # Tacha roja
                            color_celda = self.color_celda_activa
                            color_texto = "red"  # Color rojo para la tacha
                    else:
                        texto = "" if dia_semana >= self.fecha_hoy_2 else "✖"  # Sin registrar hoy o en el pasado
                        color_celda = self.color_celda_activa
                        color_texto = "red"  # Tacha roja para los no registrados

                # Crear las celdas con los estilos definidos, con altura más grande
                tk.Label(
                    self.frame_habitos_lista_ejec,
                    text=texto,
                    bg=color_celda,
                    fg=color_texto,
                    font=font_style,
                    relief="solid",
                    borderwidth=1,
                    highlightbackground=self.color_borde,
                    highlightthickness=1,
                    height=2  # Aumentar la altura del recuadro
                ).grid(column=dia_indic + 1, row=indic + 1, padx=1,
                       sticky="nsew")  # Fila indic + 1 para empezar desde la fila 1

    def configuracion(self):
        self.ventana_principal.columnconfigure(0, weight=1)
        self.ventana_principal.columnconfigure(1, weight=1)
        self.ventana_principal.columnconfigure(2, weight=1)
        # Frame barra principal
        frame_barra_titulo = tk.Frame(self.ventana_principal, bg=self.color_fondo, height=40,
                                      highlightbackground=self.color_borde, highlightthickness=1)
        frame_barra_titulo.grid(row=0,column=0,columnspan =3, sticky ="nsew")

        # Configurar el peso de las filas
        self.ventana_principal.rowconfigure(0, weight=0)  # Fila de la barra (altura fija)
        self.ventana_principal.rowconfigure(1, weight=1)  # Resto del contenido (altura expandible)

        # Labels
        # Agregar icono
        img_icono = Image.open(self.icono)
        redimension = img_icono.resize((120, 120), Image.Resampling.LANCZOS)
        self.icono_app = ImageTk.PhotoImage(redimension)
        icono_label = tk.Label(frame_barra_titulo, image=self.icono_app, bg=self.color_fondo)
        icono_label.pack(side="left", padx=5)
        # titulo
        titulo_app = tk.Label(frame_barra_titulo, text="Habit Tracker", fg="white", bg=self.color_fondo,
                              font=self.font_title, height=2)
        titulo_app.pack(side="left")
        #Frames secundarios (Lista de habitos / calendario )


        # -----------------------------------Frame lista habitos------------------------------
        self.frame_habitos = tk.Frame(self.ventana_principal, bg=self.color_encabezado,borderwidth=1,
            highlightbackground=self.color_borde,
            highlightthickness=1)
        self.frame_habitos.grid(column=0, row=1, sticky="nsew")
        #-----------------------------------Crear la lista de los habitos existentes----------
        self.lista_habitos()
        # -----------------------------------Frame grafico semanal------------------------------
        self.frame_grafico_semanal = tk.Frame(self.ventana_principal, bg=self.color_encabezado,
                                              highlightbackground=self.color_borde, highlightthickness=1,
                                              borderwidth=0)
        self.frame_grafico_semanal.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.show_week_days()



    def show_week_days(self):
        # Limpia el contenido del frame actual
        for widget in self.frame_grafico_semanal.winfo_children():
            widget.destroy()
        fecha_hoy =  datetime.now().day
        # guardamos UNICAMENTE la fecha del DIA de hoy
        dia_hoy = (fecha_hoy)
        # Guardamos UNICAMENTE el numero de semana en el que nos encontramos
        semana_corriente = self.fecha_manana.isocalendar().week
        # Guardamos el nombre o indice del dia donde Lunes = 0,----- Domingo =6
        numero_dia = self.fecha_hoy.weekday()
        # Aqui cambiamos el inicio de la semana a domingo
        dia_semana_domingo = (self.fecha_hoy.weekday() + 1) % 7
        # aqui calculamos el dia de inicio de semana que seria el domingo
        domingo = self.fecha_hoy - timedelta(days=dia_semana_domingo)
        if dia_semana_domingo == 0:
            dia = " Domingo "
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
        frame_fecha =tk.Frame  (self.frame_grafico_semanal,bg=self.color_fondo,borderwidth=1,
            highlightbackground=self.color_borde,
            highlightthickness=1)
        frame_fecha.pack(fill="x")
        label_fecha_hoy = tk.Label(frame_fecha, text=texto_dia_encabezado, bg=self.color_fondo, fg=self.color_texto,
                                   font=self.font_subtitle)

        label_semana_corriente = tk.Label(frame_fecha, text=texto_semana_encabezado, bg=self.color_fondo, fg=self.color_texto,
                                          font=(self.font_subtitle))
        label_fecha_hoy.pack(side= tk.LEFT )
        label_semana_corriente.pack(side=tk.RIGHT, padx= 20 )
        # -------------------------------Tabla dias semana-------------------------------------------
        frame_dias_actuales = tk.Frame(self.frame_grafico_semanal, bg=self.color_encabezado, borderwidth=1,
                                      highlightbackground=self.color_borde,
                                      highlightthickness=1)
        #Frame botones
        frame_botones = tk.Frame(frame_dias_actuales, bg ="pink", width = 35)
        frame_botones.grid (column=0 , row= 0, sticky = "nsew")
        # Botón de añadir hábito
        Boton_añadir_habito = tk.Button(frame_botones, text="+", fg=self.color_texto,
                                        bg=self.color_celda_inactiva,
                                        font=("Helvetica", 12, "bold"), height=2,
                                        width =10,
                                        activebackground=self.color_borde,
                                        command=self.abrir_ventana_crear_habito)
        Boton_añadir_habito.grid(column=0, row=0, sticky="nsew")  # Ubicado en la primera columna
        Boton_borrar_habito = tk.Button(frame_botones, text="-", fg=self.color_texto,
                                        bg=self.color_celda_inactiva,
                                        font=("Helvetica", 12, "bold"), height=2,
                                        width =10,
                                        activebackground=self.color_borde,
                                        command=self.abrir_ventana_eliminar_habito)
        Boton_borrar_habito.grid(column=1, row=0, sticky="nsew")  # Ubicado en la primera columna
        # Botón de cambiar a semana pasada(s)
        boton_semana_pasada = tk.Button(frame_botones, text="<", fg=self.color_texto,
                                        bg=self.color_celda_inactiva,
                                        font=("Helvetica", 12, "bold"), height=2,
                                        width=6,
                                        activebackground=self.color_borde,
                                        command=self.mostrar_semana_anterior

                                        )
        boton_semana_pasada.grid(column=2, row=0, sticky="nsew")  # Ubicado en la primera columna
        # Botón de cambiar a semana siguiente
        boton_semana_siguiente = tk.Button(frame_botones, text=">", fg=self.color_texto,
                                        bg=self.color_celda_inactiva,
                                        font=("Helvetica", 12, "bold"), height=2,
                                           width=6,
                                        activebackground=self.color_borde,
                                           command=self.mostrar_semana_siguiente

                                        )
        boton_semana_siguiente.grid(column=3, row=0, sticky="nsew")  # Ubicado en la primera columna
        # Deshabilita el botón de semana siguiente si la fecha actual es mayor o igual a hoy
        if self.fecha_hoy >= datetime.now():
            boton_semana_siguiente.config(state=tk.DISABLED)
        #-------------------------------------------------TERMINA BOTONES---------------------------------------------


        # Configurar las columnas dentro de frame_dias_actuales para que se expandan uniformemente
        frame_dias_actuales.columnconfigure(0, weight=0)  # Botón ocupa un tamaño fijo
        for i in range(1, 8):  # Las siguientes 7 columnas son para los días de la semana
            frame_dias_actuales.columnconfigure(i, weight=1)

        # Configurar la fila dentro de frame_dias_actuales para que también se expanda
        frame_dias_actuales.rowconfigure(0, weight=1)

        # Lista de días de la semana corriente
        dias_semana_corriente = [domingo + timedelta(days=i) for i in range(7)]
        self.fuente_negritas = font.Font(family="Inter", size=13, weight="bold")

        # Crear y ubicar los labels para los días
        for i, Dia in enumerate(dias_semana_corriente):
            label_dia = tk.Label(frame_dias_actuales, text=Dia.day, font=self.fuente_negritas,
                                 width=5, bg=self.color_fondo, fg=self.color_texto,
                                 borderwidth=1,
                                 highlightbackground=self.color_borde,
                                 highlightthickness=1
                                 )
            label_dia.grid(row=0, column=i + 1, sticky="nsew")  # Los labels comienzan en la columna 1

        # Empaquetar el frame_dias_actuales
        frame_dias_actuales.pack(fill="x")
        #------------------------------------------------------ Frame lista de habitos con ejecuciones------------------
        # Crear el frame para los hábitos
        self.frame_habitos_lista_ejec = tk.Frame(self.frame_grafico_semanal, bg=self.color_encabezado)
        self.frame_habitos_lista_ejec.pack(fill="x")



        # Definir los encabezados
        encabezados = ["Actividad", "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

        # Crear los encabezados
        for indice, encabezado in enumerate(encabezados):
            tk.Label(self.frame_habitos_lista_ejec, text=encabezado, bg=self.color_fondo, fg=self.color_texto,
                     borderwidth=1,
                     highlightbackground=self.color_borde,
                     highlightthickness=1,
                     font=self.font_subtitle_helvetica).grid(
                column=indice, row=0, padx=1, sticky="nsew"
            )
            self.frame_habitos_lista_ejec.grid_columnconfigure(indice, weight=1)
        self.frame_habitos_lista_ejec.grid_columnconfigure(0,weight=0)
        self.lista_habitos_frame_semana()
        rendimiento =self.calcular_rendimiento_semanal()
        frame_calculo_rendimiento = tk.Frame(self.frame_grafico_semanal, bg=self.color_borde, borderwidth=1,
                                       highlightbackground=self.color_borde,
                                       highlightthickness=1)
        frame_calculo_rendimiento.pack(fill = "x")

        self.label_rendimiento = tk.Label(frame_calculo_rendimiento, text="Rendimiento: 0%",
                                          fg=self.color_texto, bg=self.color_fondo, font=self.font_body)
        self.label_rendimiento.pack(side=tk.RIGHT)

        # Actualización en actualizar_programa
        self.label_rendimiento.config(text=f"Rendimiento logrado esta semana: {rendimiento:.2f}%")
        #-----------------------------------------------TERMINA--------------------------------------------------------
    def mostrar_semana_anterior(self):
        self.fecha_hoy -= timedelta(weeks=1)
        self.fecha_manana -= timedelta(weeks=1)
        self.show_week_days()

    def mostrar_semana_siguiente(self):
        self.fecha_hoy += timedelta(weeks=1)
        self.fecha_manana += timedelta(weeks=1)
        self.show_week_days()

    def abrir_ventana_crear_habito(self):
        self.ventana_crear_habito = Toplevel(self.ventana_principal)
        self.ventana_crear_habito.state("zoomed")
        self.ventana_crear_habito.title("Habit Tracker-Crear habito")
        self.ventana_crear_habito.geometry("1536x815")
        # ventana_principal.maxsize(1536,816)
        self.ventana_crear_habito.maxsize(1920, 1080)
        self.ventana_crear_habito.minsize(1280, 720)
        self.ventana_crear_habito.config(bg=self.color_fondo)
        self.ventana_crear_habito.overrideredirect(True)
        # -----------------------Creacion de los frames--- ventana habito--------------------------------------------------
        # Frame barra principal
        Barra_principal_ventana_crear_habito = tk.Frame(self.ventana_crear_habito, bg=self.color_fondo, bd=2, height=30)
        Barra_principal_ventana_crear_habito.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Titulo del programa
        Titulo_Programa = tk.Label(Barra_principal_ventana_crear_habito,
                                   text="Habit Tracker- by Edmolinz ", fg=self.color_texto, bg=self.color_fondo, font=self.font_body)
        Titulo_Programa.pack(side="left", padx=5)
        # Botones Regresar*
        Boton_cerrar = tk.Button(Barra_principal_ventana_crear_habito, text="⬅", bg=self.color_fondo, fg=self.color_texto,
                                 font=self.font_body, command=self.ventana_crear_habito.destroy, borderwidth=0)
        Boton_cerrar.pack(side="right", padx=5)
        # ----------------------Frame icono y titulo-------------------------------------------------------------------
        Frame_Barra_titulo_v_crear_habito = tk.Frame(self.ventana_crear_habito, bg=self.color_encabezado, bd=0, width=100, height=10)
        Frame_Barra_titulo_v_crear_habito.grid(column=0, row=1, columnspan=2, sticky="new")
        # Labels
        # Agregar icono
        # imagen_icono = Image.open("icono_principal.png")
        # redimension = imagen_icono.resize((120, 120), Image.Resampling.LANCZOS)
        # icono_app = ImageTk.PhotoImage(redimension)
        icono_label = tk.Label(Frame_Barra_titulo_v_crear_habito, image=self.icono_app, bg=self.color_encabezado)
        icono_label.pack(side="left", padx=5)
        # titulo
        titulo_app = tk.Label(Frame_Barra_titulo_v_crear_habito,
                              text="Habit Tracker",
                              fg=self.color_texto, bg=self.color_encabezado, font=self.font_title, height=2)
        titulo_app.pack(side="left")
        self.ventana_crear_habito.grid_columnconfigure(0, weight=1)
        self.ventana_crear_habito.grid_columnconfigure(1, weight=1)
        self.ventana_crear_habito.grid_rowconfigure(0, weight=0)
        self.ventana_crear_habito.grid_rowconfigure(2, weight=1)

        # -------------------------Crear habito frame-------------------------------------------------------------------

        Frame_crear_habito = tk.Frame(self.ventana_crear_habito, bg=self.color_encabezado,
                                      borderwidth=1,
                                      highlightbackground=self.color_borde,
                                      highlightthickness=1,
                                      )
        Frame_crear_habito.grid(column=0, row=2, sticky="nsew")


        # label texto crear habito
        label_crear_habito = tk.Label(Frame_crear_habito, text="Crear habito", fg=self.color_texto, bg=self.color_encabezado,
                                      borderwidth=1,
                                      highlightbackground=self.color_borde,
                                      highlightthickness=1,
                                      font=self.font_body, height=2)
        label_crear_habito.pack(fill="x")

        # Entrada de como se llamara el habito
        def on_entry_click(event):
            if Entrada_nombre_nuevo_habito.get() == default_text:
                Entrada_nombre_nuevo_habito.delete(0, tk.END)  # Borra el texto
                Entrada_nombre_nuevo_habito.config(fg=self.color_texto)  # Cambia el color del texto

        def on_focus_out(event):
            if Entrada_nombre_nuevo_habito.get() == "":
                Entrada_nombre_nuevo_habito.insert(0, default_text)  # Restaura el texto predeterminado
                Entrada_nombre_nuevo_habito.config(fg="gray")  # Cambia el color del texto

        default_text = "Nombre de tu habito"
        Entrada_nombre_nuevo_habito = tk.Entry(Frame_crear_habito, fg="gray", bg="#2f2f2f",
                                               font=self.font_body)
        Entrada_nombre_nuevo_habito.insert(0, default_text)
        Entrada_nombre_nuevo_habito.bind("<FocusIn>", on_entry_click)
        Entrada_nombre_nuevo_habito.bind("<FocusOut>", on_focus_out)
        Entrada_nombre_nuevo_habito.pack(fill="x", padx=20, pady=5)
        #---------------------------Obtener nombre del habito ingresado-----------------------------------------------------

        # -----------------------------------Configuracion de habito frame--------------------------------------------------
        Frame_config_habito = tk.Frame(self.ventana_crear_habito, bg=self.color_encabezado,
                                       borderwidth=1,
                                       highlightbackground=self.color_borde,
                                       highlightthickness=1
                                       )
        Frame_config_habito.grid(column=1, row=2, sticky="nsew")
        # label elegir dias
        label_seleccionar_dias = tk.Label(Frame_config_habito,
                                          text="SELECCIONA LOS DIAS QUE QUIERES REALIZAR EL HABITO",
                                          fg=self.color_texto, bg=self.color_encabezado, font=self.font_body, height=2,
                                          borderwidth=1,
                                          highlightbackground=self.color_borde,
                                          highlightthickness=1
                                          )
        label_seleccionar_dias.pack(fill= "x")
        #---------------------------------------codigo para iterar los botones de seleccion--------------------------------
        frame_dias = tk.Frame(Frame_config_habito, bg=self.color_encabezado,
                              borderwidth=1,
                              highlightbackground=self.color_borde,
                              highlightthickness=1
                              )
        frame_dias.pack(anchor="nw", fill ="x")

        dias_semana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        # Lista para guardar el valor de las variables seleccionadas
        self.variables = []

        for indice, dia in enumerate(dias_semana):
            frame_dias.grid_columnconfigure(indice, weight =1)
            # Definir que la variable es un entero y se guardará en "variable"
            variable = tk.IntVar(value=0)
            # Agregar la variable a la lista
            self.variables.append(variable)
            # Crear los botones de selección (checkbox) directamente
            tk.Checkbutton(
                frame_dias,
                text=dia,
                variable=variable,
                bg=self.color_encabezado,
                fg=self.color_texto,
                selectcolor=self.color_celda_activa,
                font=self.font_body
            ).grid(row=0, column=indice, padx=5, pady=5, sticky="w")

        # Botón para guardar el hábito
        boton_guardar = tk.Button(self.ventana_crear_habito, text="Crear hábito", fg="white", bg=self.color_celda_inactiva,
                                  font=self.font_body,
                                  bd =1,
                                  relief = "flat",
                                  highlightbackground=self.color_borde,
                                  highlightthickness=1,
                                  activebackground=self.color_borde,
                                  command=lambda :self.crear_habito(self.habitos,Entrada_nombre_nuevo_habito.get(),self.variables))
        boton_guardar.grid(row=3, column=0, columnspan=1, pady=10)
        #------------------------------------------------registro extemporaneo--------------------------------------------------

        label_registrar_habito_dia_anterior = tk.Label(Frame_config_habito,
                                          text="SI OLVIDASTE REGISTRAR EL HABITO AYER, AQUI PUEDES REGISTRAR EL HABITO (SOLO UN DIA ANTERIOR)",
                                          fg=self.color_texto, bg=self.color_encabezado, font=self.font_body, height=2,
                                          borderwidth=1,
                                          highlightbackground=self.color_borde,
                                          highlightthickness=1
                                          )
        label_registrar_habito_dia_anterior.pack(fill= "x")
        #----------------------------------------------------------


        if not self.habitos:
            tk.Button(
                Frame_config_habito,
                text="No hay hábitos registrados.",
                bg=self.color_celda_activa,
                fg=self.color_texto,
                font=self.font_subtitle_helvetica
            ).pack(pady=5)
        else:
            for habit in self.habitos:
                tk.Button(
                    Frame_config_habito,
                    text=habit["nombre_habito"],
                    bg=self.color_celda_activa,
                    fg=self.color_texto,
                    font=self.font_subtitle_helvetica,
                    activebackground=self.color_celda_activa,
                    relief="flat",
                    command=lambda h=habit["nombre_habito"]: self.registrar_ejecucion_habito_dia_anterior(h)
                ).pack(fill="x", pady=1, padx=2)


if __name__ == "__main__":
    import tkinter as tk
    import os
    import json


    # Función para guardar la posición de la ventana
    def save_window_position(window):
        # Obtener las coordenadas de la ventana
        x = window.winfo_x()
        y = window.winfo_y()

        # Guardar las coordenadas en un archivo JSON
        position = {"x": x, "y": y}
        with open("window_position.json", "w") as f:
            json.dump(position, f)


    # Función para cargar la posición de la ventana
    def load_window_position(window):
        # Verificar si el archivo existe
        if os.path.exists("window_position.json"):
            with open("window_position.json", "r") as f:
                position = json.load(f)
                # Colocar la ventana en la posición guardada
                window.geometry(f"+{position['x']}+{position['y']}")
        else:
            # Si no existe el archivo, centrar la ventana
            window.update_idletasks()  # Asegura que se obtengan los valores correctos de tamaño
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            window.geometry(
                f"800x600+{(screen_width - 800) // 2}+{(screen_height - 600) // 2}")  # Ajusta el tamaño predeterminado si es necesario


    # Crear la ventana principal
    ventana_principal = tk.Tk()

    # Cargar la posición de la ventana al iniciar
    load_window_position(ventana_principal)

    # Crear la aplicación GUI
    app = GUI(ventana_principal)

    # Maximizar la ventana
    ventana_principal.state("zoomed")

    # Guardar la posición cuando la ventana se cierre
    ventana_principal.protocol("WM_DELETE_WINDOW",
                               lambda: (save_window_position(ventana_principal), ventana_principal.destroy()))

    # Ejecutar el loop de la interfaz
    ventana_principal.mainloop()



