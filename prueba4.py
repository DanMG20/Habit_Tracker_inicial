import customtkinter as ctk

# Configuración general
ctk.set_appearance_mode("080f0d")  # Tema oscuro
ctk.set_default_color_theme("green")  # Base de colores verde

# Crear la ventana principal
app = ctk.CTk()
app.title("Habit Tracker")
app.geometry("1000x600")
app.configure(bg="#121212")  # Fondo oscuro

# Colores personalizados
PRIMARY_COLOR = "#105f50"
SECONDARY_COLOR = "#292e2d"
TEXT_COLOR = "#d5e3e4"

# --------------------- Encabezado ---------------------
header_frame = ctk.CTkFrame(app, height=80, corner_radius=10, fg_color=SECONDARY_COLOR)
header_frame.pack(fill="x", padx=20, pady=10)

header_label = ctk.CTkLabel(header_frame, text="Habit Tracker", font=("Arial", 28), text_color=PRIMARY_COLOR)
header_label.pack(side="left", padx=20, pady=10)

quote_label = ctk.CTkLabel(header_frame, text="Si lo puedes medir, lo puedes mejorar", font=("Arial", 16),
                           text_color=TEXT_COLOR)
quote_label.pack(side="right", padx=20, pady=10)

# --------------------- Sección de Fecha ---------------------
date_frame = ctk.CTkFrame(app, height=50, corner_radius=10, fg_color=SECONDARY_COLOR)
date_frame.pack(fill="x", padx=20, pady=10)

date_label = ctk.CTkLabel(date_frame, text="Hoy Miércoles 29", font=("Arial", 22), text_color=TEXT_COLOR)
date_label.pack(pady=10)

# --------------------- Selección de Hábitos ---------------------
habits_frame = ctk.CTkFrame(app, height=200, corner_radius=10, fg_color=SECONDARY_COLOR)
habits_frame.pack(fill="x", padx=20, pady=10)

habits_label = ctk.CTkLabel(habits_frame, text="Selecciona el hábito para completarlo:", font=("Arial", 18),
                            text_color=TEXT_COLOR)
habits_label.pack(pady=10)

# Lista de hábitos
habits = ["Meditar", "Leer"]
for habit in habits:
    habit_button = ctk.CTkButton(habits_frame, text=habit, font=("Arial", 16), fg_color=PRIMARY_COLOR,
                                 text_color=TEXT_COLOR, corner_radius=10)
    habit_button.pack(pady=5, padx=20, fill="x")

# --------------------- Tabla de Progreso Semanal ---------------------
progress_frame = ctk.CTkFrame(app, height=200, corner_radius=10, fg_color=SECONDARY_COLOR)
progress_frame.pack(fill="x", padx=20, pady=10)

week_label = ctk.CTkLabel(progress_frame, text="Semana 5", font=("Arial", 20), text_color=TEXT_COLOR)
week_label.pack(pady=10)

# Tabla
table_frame = ctk.CTkFrame(progress_frame, corner_radius=10, fg_color=SECONDARY_COLOR)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Encabezados de los días
days = ["D", "L", "M", "M", "J", "V", "S"]
for col, day in enumerate(days):
    day_label = ctk.CTkLabel(table_frame, text=day, font=("Arial", 14), text_color=TEXT_COLOR)
    day_label.grid(row=0, column=col, padx=5, pady=5)

# Progreso de los hábitos
habits_progress = [
    ["✔", "✔", "✔", "✔", "-", "-", "-"],  # Progreso para el hábito 1
    ["✘", "✔", "✘", "-", "-", "-", "-"],  # Progreso para el hábito 2
]

for row, progress in enumerate(habits_progress, start=1):  # Comienza en la fila 1
    for col, cell in enumerate(progress):
        cell_label = ctk.CTkLabel(table_frame, text=cell, font=("Arial", 14), text_color=TEXT_COLOR)
        cell_label.grid(row=row, column=col, padx=5, pady=5)

# --------------------- Rendimiento ---------------------
performance_frame = ctk.CTkFrame(app, height=100, corner_radius=10, fg_color=SECONDARY_COLOR)
performance_frame.pack(fill="x", padx=20, pady=10)

performance_label = ctk.CTkLabel(performance_frame, text="Rendimiento semanal: 80%", font=("Arial", 18),
                                 text_color=PRIMARY_COLOR)
performance_label.pack(pady=10)

# Ejecutar la aplicación
app.mainloop()


