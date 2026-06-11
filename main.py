#import zone

import tkinter as tk
import json
from tkinter import messagebox





def registrarse():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro")

    etiqueta_usuario= tk.Label(
        ventana_registro,
        text = "Usuario:"
    )

    etiqueta_usuario.pack()

    entrada_usuario = tk.Entry(
        ventana_registro
    )
    entrada_usuario.pack()

    etiqueta_contrasena = tk.Label(
        ventana_registro,
        text = "Contraseña:"
    )
    etiqueta_contrasena.pack()

    entrada_contrasena = tk.Entry(
        ventana_registro
    )
    entrada_contrasena.pack()
    def guardar_usuario():

        usuario = entrada_usuario.get()

        contrasena = entrada_contrasena.get()

        if not usuario:
            messagebox.showerror(
                "Error",
                "El usuario no puede estar vacio"
        )
            return
        if not contrasena:
            messagebox.showerror(
                "Error",
                "La contrasena no puede estar vacia"
        )
            return

        with open("jugadores.json", "r") as archivo:
            jugadores = json.load(archivo)

        for jugador in jugadores:
            if jugador["usuario"] == usuario:
                messagebox.showerror(
                    "Error",
                    "Ese usuario ya existe",
                )

                return
        nuevo_jugador = {
            "usuario": usuario,
            "contrasena": contrasena,
            "victorias_defensor": 0,
            "victorias_atacante": 0
        }

        jugadores.append(nuevo_jugador)
        with open("jugadores.json", "w") as archivo:
            json.dump(jugadores, archivo, indent=4)

        messagebox.showinfo(
            "Exito",
            "Usuario registrado correctamente"
        )

        venatana_registro.destroy()

        print(usuario)

        print(contrasena)

    boton_registrar = tk.Button(
        ventana_registro,
        text = "Registrar",
        command = guardar_usuario
    )

    boton_registrar.pack()

def iniciar_sesion():
    ventana_login = tk.Toplevel()
    ventana_login.title("Iniciar Sesión")

    etiqueta_usuario = tk.Label(ventana_login, text="Usuario:")
    etiqueta_usuario.pack()

    entrada_usuario = tk.Entry(ventana_login)
    entrada_usuario.pack()

    etiqueta_contrasena = tk.Label(ventana_login, text="Contraseña:")
    etiqueta_contrasena.pack()

    entrada_contrasena = tk.Entry(ventana_login, show="*")
    entrada_contrasena.pack()

    def verificar_login():
        usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()

        if not usuario:
            messagebox.showerror("Error", "El usuario no puede estar vacío")
            return
        if not contrasena:
            messagebox.showerror("Error", "La contraseña no puede estar vacía")
            return

        with open("jugadores.json", "r") as archivo:
             jugadores = json.load(archivo)

        for jugador in jugadores:
             if jugador["usuario"] == usuario:
                 if jugador["contrasena"] == contrasena:
                    messagebox.showinfo("Éxito", f"Bienvenido, {usuario}!")
                    ventana_login.destroy()
                    return
                 else:
                        messagebox.showerror(
                            "Error",
                            "Contraseña incorrecta"
                        )
                        return

        messagebox.showerror(
            "Error",
            "El usuario no existe"
        )

    boton_login = tk.Button(ventana_login, text="Iniciar Sesión", command=verificar_login)
    boton_login.pack(pady=10)


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
