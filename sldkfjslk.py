import tkinter as tk
import json
import os

class HabitTrackerApp:
    def __init__(self, root):
        self.bg_color2 = "#2f2f2f"  # Color de fondo
        self.text_color = "#ffffff"  # Color del texto
        self.font_body = ("Arial", 12)  # Fuente de texto
        self.habits_file = "Base_de_datos_habitos.json"  # Archivo JSON donde se guardan los hábitos

        # Crear el marco principal
        self.main_frame = tk.Frame(root, bg=self.bg_color2)
        self.main_frame.pack(fill="both", expand=True)

        # Crear el marco para listar los nombres de los hábitos
        self.habits_list_frame = tk.Frame(self.main_frame, bg=self.bg_color2)
        self.habits_list_frame.pack(fill="x", pady=10)

        # Cargar y mostrar los hábitos existentes
        self.habits = self.load_habits()
        self.list_habits()

        # Botón para actualizar la lista de hábitos
        tk.Button(
            self.main_frame,
            text="Actualizar Lista",
            command=self.list_habits,
            bg="#4CAF50",
            fg="white",
            font=self.font_body
        ).pack(pady=10)

    def load_habits(self):
        """Carga los hábitos desde el archivo JSON."""
        if os.path.exists(self.habits_file):
            with open(self.habits_file, "r") as file:
                return json.load(file)
        return []  # Si el archivo no existe, regresa una lista vacía

    def list_habits(self):
        """Lista los nombres de los hábitos en el marco."""
        # Limpiar el marco para evitar duplicados
        for widget in self.habits_list_frame.winfo_children():
            widget.destroy()

        if not self.habits:
            tk.Label(
                self.habits_list_frame,
                text="No hay hábitos registrados.",
                bg=self.bg_color2,
                fg=self.text_color,
                font=self.font_body
            ).pack(pady=5)
        else:
            for habit in self.habits:
                tk.Label(
                    self.habits_list_frame,
                    text=habit["nombre_habito"],
                    bg=self.bg_color2,
                    fg=self.text_color,
                    font=self.font_body
                ).pack(anchor="w", padx=10, pady=2)

# Crear la ventana principal
root = tk.Tk()
root.title("Habit Tracker")
root.geometry("400x300")
app = HabitTrackerApp(root)
root.mainloop()
