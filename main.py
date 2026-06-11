import tkinter as tk

ventana = tk.Tk()
ventana.title("Defensa y Asalto de Base")
ventana.geometry("800x600")

etiqueta = tk.Label(
    ventana,
    text="Proyecto Defensa y Asalto de Base"
)

etiqueta.pack(pady=20)

ventana.mainloop()

