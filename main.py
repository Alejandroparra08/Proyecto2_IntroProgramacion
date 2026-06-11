import tkinter as tk

def registrarse():
    print("Ventana de registro")

def iniciar_sesion():
    print("Ventana de inicio de sesión")

ventana = tk.Tk()

ventana.title("Defensa y Asalto de Base")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Defensa y Asalto de Base",
    font=("Arial", 20)
)
titulo.pack(pady=30)

boton_registro = tk.Button(
    ventana,
    text="Registrarse",
    width=20,
    command=registrarse
)
boton_registro.pack(pady=10)

boton_login = tk.Button(
    ventana,
    text="Iniciar Sesión",
    width=20,
    command=iniciar_sesion
)
boton_login.pack(pady=10)

ventana.mainloop()
