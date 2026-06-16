#import zone

import tkinter as tk
import json
from tkinter import messagebox
import os
import sys
os.chdir(r"C:\Users\aleja\OneDrive\Documents\Introduccion a la programacion\Proyecto II Juego - Alejandro & Mathew")

COLOR_FONDO = "#0a0a0a"
COLOR_VERDE = "#39ff14"
COLOR_ROJO = "#8b0000"
COLOR_TEXTO = "#c8c8c8"
FUENTE_TITULO = ("Courier", 40, "bold")
FUENTE_NORMAL = ("Courier", 12)
FUENTE_BTN   = ("Courier", 14, "bold")
FUENTE_SMALL = ("Courier", 10)
COLOR_ROJO_VIF = "#FF0000"
RUTA_JSON = r"C:\Users\aleja\OneDrive\Documents\Introduccion a la programacion\Proyecto II Juego - Alejandro & Mathew\jugadores.json"


"""
Sistema de ranking
"""
def mostrar_ranking():
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000",
        padx=40,
        pady=30
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame_actual,
        text="─── 🏆 RANKING ───",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(0, 20))

    with open(RUTA_JSON, "r") as archivo:
        jugadores = json.load(archivo)

    for i in range(len(jugadores)):
        for j in range(i + 1, len(jugadores)):
            if jugadores[j]["victorias_defensor"] > jugadores[i]["victorias_defensor"]:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]

    tk.Label(
        frame_actual,
        text="TOP 5 DEFENSORES",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack()
    
    posicion = 1
    for jugador in jugadores:
        if posicion > 5:
            break
        
        tk.Label(
            frame_actual,
            text=f"{posicion}. {jugador['usuario']} - {jugador['victorias_defensor']} victorias",
            font=FUENTE_NORMAL,
            bg="#0d0000",
            fg=COLOR_VERDE
        ).pack()
        posicion += 1

    tk.Label(
        frame_actual,
        text="",
        bg="#0d0000"
    ).pack(pady=8)

    for i in range(len(jugadores)):
        for j in range(i + 1, len(jugadores)):
            if jugadores[j]["victorias_atacante"] > jugadores[i]["victorias_atacante"]:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]

    tk.Label(
        frame_actual,
        text="TOP 5 ATACANTES",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack()
    
    posicion = 1
    for jugador in jugadores:
        if posicion > 5:
            break
        tk.Label(
            frame_actual,
            text=f"{posicion}. {jugador['usuario']} - {jugador['victorias_atacante']} victorias",
            font=FUENTE_NORMAL,
            bg="#0d0000",
            fg=COLOR_VERDE
        ).pack()
        posicion += 1

    tk.Label(
        frame_actual,
        text="",
        bg="#0d0000"
    ).pack(pady=8)
    
    tk.Button(
        frame_actual,
        text="← VOLVER",
        command=mostrar_inicio,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)

"""
Muestra del menu inicial
"""
    
def mostrar_menu_principal(usuario):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000",
        padx=40,
        pady=30
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame_actual,
        text=f"BIENVENIDO, {usuario.upper()}",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(0, 30))

    tk.Button(
        frame_actual,
        text="☣  NUEVA PARTIDA  ☣",
        command=lambda: print("Nueva partida"),
        font=FUENTE_BTN, bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)
    
    tk.Button(
        frame_actual,
        text="☣  RANKING  ☣",
        command=mostrar_ranking,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)
    
    tk.Button(
        frame_actual,
        text="☣  SALIR  ☣",
        command=mostrar_inicio,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)

"""
Sistema de logueo
"""

def mostrar_login():
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000",
        padx=40,
        pady=30
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame_actual,
        text="─── INICIAR SESIÓN ───",
        font=FUENTE_BTN, bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(0, 20))

    tk.Label(
        frame_actual,
        text="USUARIO:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    entry_usuario = tk.Entry(
        frame_actual,
        font=FUENTE_NORMAL,
        bg="#1a0000",
        fg=COLOR_VERDE,
        insertbackground=COLOR_VERDE,
        relief="flat",
        highlightbackground=COLOR_ROJO,
        highlightthickness=1
    )
    entry_usuario.pack(fill="x", pady=(2, 10), ipady=6)

    tk.Label(
        frame_actual,
        text="CONTRASEÑA:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    entry_contra = tk.Entry(
        frame_actual,
        font=FUENTE_NORMAL,
        bg="#1a0000",
        fg=COLOR_VERDE,
        insertbackground=COLOR_VERDE,
        relief="flat",
        highlightbackground=COLOR_ROJO,
        highlightthickness=1,
        show="*"
        )
    entry_contra.pack(fill="x", pady=(2, 20), ipady=6)

    lbl_error = tk.Label(
        frame_actual,
        text="",
        font=FUENTE_SMALL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    )
    lbl_error.pack()

    def verificar():
        usuario = entry_usuario.get().strip()
        contra = entry_contra.get().strip()
        if not usuario:
            lbl_error.config(text="⚠ El usuario no puede estar vacío")
            return
        if not contra:
            lbl_error.config(text="⚠ La contraseña no puede estar vacía")
            return
        with open(RUTA_JSON, "r") as archivo:
            jugadores = json.load(archivo)
        for jugador in jugadores:
            if jugador["usuario"] == usuario:
                if jugador["contrasena"] == contra:
                    mostrar_menu_principal(usuario)
                    return
                else:
                    lbl_error.config(text="⚠ Contraseña incorrecta")
                    return
        lbl_error.config(text="⚠ El usuario no existe")

    tk.Button(frame_actual,
              text="☣  ENTRAR  ☣",
              command=verificar,
              font=FUENTE_BTN,
              bg="#1a0000",
              fg=COLOR_ROJO_VIF,
              relief="flat",
              cursor="hand2",
              padx=40,
              pady=12,
              width=20
    ).pack(pady=6)
    
    tk.Button(
        frame_actual,
        text="← VOLVER",
        command=mostrar_inicio,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=4)


def mostrar_registro():
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000",
        padx=40,
        pady=30
    )
    frame_actual.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        frame_actual,
        text="─── REGISTRARSE ───",
        font=FUENTE_BTN, bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(0, 20))

    tk.Label(
        frame_actual,
        text="USUARIO:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    entry_usuario = tk.Entry(
        frame_actual,
        font=FUENTE_NORMAL,
        bg="#1a0000",
        fg=COLOR_VERDE,
        insertbackground=COLOR_VERDE,
        relief="flat",
        highlightbackground=COLOR_ROJO,
        highlightthickness=1
    )
    
    entry_usuario.pack(fill="x", pady=(2, 10), ipady=6)

    tk.Label(
        frame_actual,
        text="CONTRASEÑA:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    entry_contra = tk.Entry(
        frame_actual,
        font=FUENTE_NORMAL,
        bg="#1a0000",
        fg=COLOR_VERDE,
        insertbackground=COLOR_VERDE,
        relief="flat",
        highlightbackground=COLOR_ROJO,
        highlightthickness=1
    )
    entry_contra.pack(fill="x", pady=(2, 20), ipady=6)

    lbl_msg = tk.Label(
        frame_actual,
        text="",
        font=FUENTE_SMALL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    )
    lbl_msg.pack()

    def guardar():
        usuario = entry_usuario.get().strip()
        contra = entry_contra.get().strip()
        if not usuario:
            lbl_msg.config(text="⚠ El usuario no puede estar vacío")
            return
        if not contra:
            lbl_msg.config(text="⚠ La contraseña no puede estar vacía")
            return
        with open(RUTA_JSON, "r") as archivo:
            jugadores = json.load(archivo)
        for jugador in jugadores:
            if jugador["usuario"] == usuario:
                lbl_msg.config(text="⚠ Ese usuario ya existe")
                return
        nuevo = {"usuario": usuario, "contrasena": contra, "victorias_defensor": 0, "victorias_atacante": 0}
        jugadores.append(nuevo)
        with open(RUTA_JSON, "w") as archivo:
            json.dump(jugadores, archivo, indent=4)
        lbl_msg.config(text="✓ Registrado correctamente", fg=COLOR_VERDE)
        ventana.after(1200, mostrar_inicio)

    tk.Button(
        frame_actual,
        text="☣  REGISTRAR  ☣",
        command=guardar,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=6)
    
    tk.Button(
        frame_actual,
        text="← VOLVER",
        command=mostrar_inicio,
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=4)


"""
Ventana de inicio
"""

def mostrar_inicio():
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg = "#0d0000",
        padx = 40,
        pady = 30
    )

    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Button(
        frame_actual,
        text = "☣  INICIAR SESIÓN  ☣",
        command = mostrar_login,
        font = FUENTE_BTN,
        bg = "#1a0000",
        fg = COLOR_ROJO_VIF,
        relief = "flat",
        cursor = "hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)

    tk.Button(
        frame_actual,
        text = "☣  REGISTRARSE  ☣",
        command = mostrar_registro,
        font = FUENTE_BTN,
        bg = "#1a0000",
        fg = COLOR_ROJO_VIF,
        relief = "flat",
        cursor = "hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)

    tk.Button(
        frame_actual,
        text = "☣  RANKING  ☣",
        command = mostrar_ranking,
        font = FUENTE_BTN,
        bg = "#1a0000",
        fg = COLOR_ROJO_VIF,
        relief = "flat",
        cursor = "hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)

    tk.Button(
        frame_actual,
        text = "☣  SALIR  ☣",
        command = ventana.destroy,
        font = FUENTE_BTN,
        bg = "#1a0000",
        fg = COLOR_ROJO_VIF,
        relief = "flat",
        cursor = "hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)






frame_actual = None
ventana = tk.Tk()

ventana.title("ATTACK US")
ventana.state("zoomed")


fondo_inicio_img = tk.PhotoImage(file=r"C:\Users\aleja\OneDrive\Documents\Introduccion a la programacion\Proyecto II Juego - Alejandro & Mathew\fondo_login.png")
fondo_label = tk.Label(
    ventana,
    image = fondo_inicio_img
)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
fondo_label.lower()

tk.Label(
    ventana,
    text = "☣ ATTACK US ☣",
    font = FUENTE_TITULO,
    bg = "#5c1a2e",
    fg = "#FF0000"
).place(relx=0.5, rely=0.1, anchor = "center")

mostrar_inicio()




"""
Fin de ventana de inicio
"""


"""
ranking
"""

"""
Fin de ranking
"""











ventana.mainloop()

    
