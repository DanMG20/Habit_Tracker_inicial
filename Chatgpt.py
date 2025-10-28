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
    if os.path.exists("window_position.json"):
        with open("window_position.json", "r") as f:
            position = json.load(f)
            # Colocar la ventana en la posición guardada
            window.geometry(f"+{position['x']}+{position['y']}")


# Crear la ventana principal
root = tk.Tk()

# Cargar la posición de la ventana al iniciar
load_window_position(root)

# Hacer que la ventana se ejecute maximizada
root.state('zoomed')

# Establecer el tamaño de la ventana y el título
root.geometry("800x600")  # Ajusta el tamaño si lo necesitas
root.title("Mi Aplicación")

# Guardar la posición cuando la ventana se cierre
root.protocol("WM_DELETE_WINDOW", lambda: (save_window_position(root), root.destroy()))

# Resto de tu código para la interfaz

# Ejecutar el loop de la interfaz
root.mainloop()
