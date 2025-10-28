# Prueba para ENtry

import tkinter as tk

def on_entry_click(event):
    if entry.get() == default_text:
        entry.delete(0, tk.END)  # Borra el texto
        entry.config(fg="black")  # Cambia el color del texto

def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, default_text)  # Restaura el texto predeterminado
        entry.config(fg="gray")  # Cambia el color del texto

root = tk.Tk()
root.title("Entry con texto predeterminado")

default_text = "Escribe aquí..."
entry = tk.Entry(root, fg="gray")
entry.insert(0, default_text)

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)

entry.pack(padx=20, pady=20)

root.mainloop()