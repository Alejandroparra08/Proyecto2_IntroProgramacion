#import zone

import tkinter as tk
import json
from tkinter import messagebox


COLOR_FONDO = "#0a0a0a"
COLOR_VERDE = "#39ff14"
COLOR_ROJO = "#8b0000"
COLOR_TEXTO = "#c8c8c8"
FUENTE_TITULO = ("Courier", 28, "bold")
FUENTE_NORMAL = ("Courier", 12)

"""
Sistema de Logueo
"""

def registrarse():
    global ventana_registro
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro")
    ventana_registro.configure(bg = COLOR_FONDO)

    etiqueta_usuario= tk.Label(
        ventana_registro,
        text = "Usuario:",
        bg = COLOR_FONDO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL
    )

    etiqueta_usuario.pack()

    entrada_usuario = tk.Entry(
        ventana_registro,
        bg = "#1a1a1a",
        fg = COLOR_VERDE,
        insertbackground = COLOR_VERDE,
        font = FUENTE_NORMAL
    )
    entrada_usuario.pack()

    etiqueta_contrasena = tk.Label(
        ventana_registro,
        text = "Contraseña:",
        bg = COLOR_FONDO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL,
    )
    etiqueta_contrasena.pack()

    entrada_contrasena = tk.Entry(
        ventana_registro,
        bg = "#1a1a1a",
        fg = COLOR_VERDE,
        insertbackground = COLOR_VERDE,
        font = FUENTE_NORMAL
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

        ventana_registro.destroy()
        messagebox.showinfo(
            "Exito",
            "Usuario registrado correctamente"
        )

        ventana_registro.destroy()

        print(usuario)

        print(contrasena)

    boton_registrar = tk.Button(
        ventana_registro,
        text = "Registrar",
        command = guardar_usuario,
        bg = COLOR_ROJO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL,
        relief = "flat",
        cursor = "hand2"
    )

    boton_registrar.pack()



def abrir_menu_principal(usuario):
    ventana_menu = tk.Toplevel()
    ventana_menu.title("Menú Principal")
    ventana_menu.geometry("800x600")

    tk.Label(
        ventana_menu,
        text=f"Bienvenido, {usuario}!",
        font=("Arial", 20)
    ).pack(pady=30)

    tk.Button(
        ventana_menu,
        text="Nueva Partida",
        width=20,
        command=lambda: print("Nueva partida")
    ).pack(pady=10)

    tk.Button(
        ventana_menu,
        text="Ver Ranking",
        width=20,
        command=ranking
    ).pack(pady=10)

    tk.Button(
        ventana_menu,
        text="Salir",
        width=20,
        command=ventana_menu.destroy
    ).pack(pady=10)



def iniciar_sesion():
    global ventana_login
    ventana_login = tk.Toplevel()
    ventana_login.title("Iniciar Sesión")
    ventana_login.configure(bg = COLOR_FONDO)
    

    etiqueta_usuario = tk.Label(
        ventana_login,
        text="Usuario:",
        bg = COLOR_FONDO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL
    )
    etiqueta_usuario.pack()

    entrada_usuario = tk.Entry(
        ventana_login,
        bg = "#1a1a1a",
        fg = COLOR_VERDE,
        insertbackground = COLOR_VERDE,
        font = FUENTE_NORMAL
    )
    entrada_usuario.pack()

    etiqueta_contrasena = tk.Label(
        ventana_login,
        text="Contraseña:",
        bg = COLOR_FONDO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL
    )
    etiqueta_contrasena.pack()

    entrada_contrasena = tk.Entry(
        ventana_login,
        show="*",
        bg = "#1a1a1a",
        fg = COLOR_VERDE,
        insertbackground = COLOR_VERDE,
        font = FUENTE_NORMAL
    )
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
                    abrir_menu_principal(usuario)
                    ventana.withdraw()
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

    boton_login = tk.Button(
        ventana_login,
        text="Iniciar Sesión",
        command=verificar_login,
        bg = COLOR_ROJO,
        fg = COLOR_VERDE,
        font = FUENTE_NORMAL,
        relief = "flat",
        cursor = "hand2"
    )
    boton_login.pack(pady=10)
"""
Fin del sistema de logueo
"""


"""
Ventana de inicio
"""

ventana = tk.Tk()

ventana.title("Defensa y Asalto de Base")
ventana.geometry("800x600")
ventana.configure(bg = COLOR_FONDO)

titulo = tk.Label(
    ventana,
    text="☣ DEFENSA Y ASALTO DE BASE ☣",
    font= FUENTE_TITULO,
    bg = COLOR_FONDO,
    fg = COLOR_VERDE
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



"""
Fin de ventana de inicio
"""


"""
ranking
"""

def ranking():
    ventana_ranking = tk.Toplevel()
    ventana_ranking.title("Ranking")
    ventana_ranking.geometry("400x500")

    tk.Label(
        ventana_ranking,
        text="🏆 ranking",
        font= ("Arial", 18)
    ).pack(pady=20)

    with open("jugadores.json", "r") as archivo:
        jugadores = json.load(archivo)

    #Algoritmo de ordenamiento para saber quien tiene mas
    for i in range(len(jugadores)):
        for j in range(i + 1, len(jugadores)):
            if jugadores[j]["victorias_defensor"] > jugadores[i]["victorias_defensor"]:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]
                
    

    #Crear el top 5 de defensores

    tk.Label(
        ventana_ranking,
        text = "Top 5 defensores",
        font = ("Arial", 13, "bold")
    ).pack(pady=(10, 5))

    posicion = 1
    for jugador in jugadores:
        if posicion > 5:
            break
        tk.Label(
            ventana_ranking,
            text = f"{posicion}. {jugador['usuario']} - {jugador['victorias_defensor']} victorias"
        ).pack()
        posicion += 1


    #Reordenar para atacante

    for i in range(len(jugadores)):
        for j in range(i + 1, len(jugadores)):
            if jugadores[j]["victorias_atacante"] > jugadores[i]["victorias_atacante"]:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]
                

    tk.Label(
        ventana_ranking,
        text = "Top 5 Atacantes",
        font = ("Arial", 13, "bold")
    ).pack(pady=(20,5))


    posicion = 1
    for jugador in jugadores:
        if posicion > 5:
            break
        tk.Label(
            ventana_ranking,
            text = f"{posicion}. {jugador['usuario']} - {jugador['victorias_atacante']} victorias"
        ).pack()
        posicion += 1

    tk.Button(
        ventana_ranking,
        text = "Cerrar",
        command = ventana_ranking.destroy
    ).pack(pady = 20)
    
"""
Fin de ranking
"""












ventana.mainloop()

    
