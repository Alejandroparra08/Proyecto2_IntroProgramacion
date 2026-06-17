#import zone
import os
import sys


sys.path.insert(0, r"C:\Users\aleja\OneDrive\Documents\Introduccion a la programacion\Proyecto II Juego - Alejandro & Mathew")
os.chdir(r"C:\Users\aleja\OneDrive\Documents\Introduccion a la programacion\Proyecto II Juego - Alejandro & Mathew")


import tkinter as tk
import json
from tkinter import messagebox
from clases import VentanaMapa, Torre, Sierra



COLOR_FONDO = "#0a0a0a"
COLOR_VERDE = "#39ff14"
COLOR_ROJO = "#8b0000"
COLOR_TEXTO = "#c8c8c8"
FUENTE_TITULO = ("Courier", 40, "bold")
FUENTE_NORMAL = ("Courier", 12)
FUENTE_BTN   = ("Courier", 14, "bold")
FUENTE_SMALL = ("Courier", 10)
COLOR_ROJO_VIF = "#FF0000"
RUTA_JSON = "jugadores.json"


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
Muestra del menu luego de ingresar
"""

def mostrar_fase_defensor(defensor, atacante, rol_defensor, rol_atacante):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000"
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    #Panel superior
    tk.Label(
        frame_actual,
        text="FASE DE CONSTRUCCIÓN",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(10,0))
    
    tk.Label(
        frame_actual,
        text=f"{defensor.upper()} — coloca tus defensas",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_VERDE
    ).pack()

    #Dinero
    dinero = [300]
    lbl_dinero = tk.Label(
        frame_actual, text=f"💰 Dinero: {dinero[0]}",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=GOLD if 'GOLD' in dir() else "#FFD700"
    )
    lbl_dinero.pack()

    # mapa + panel de torres
    frame_central = tk.Frame(
        frame_actual,
        bg="#0d0000"
    )
    frame_central.pack(pady=10)

    # Mapa
    frame_mapa = tk.Frame(
        frame_central,
        bg="#0d0000"
    )
    frame_mapa.pack(side="left", padx=10)
    juego = VentanaMapa(frame_mapa)

    # Panel de torres
    frame_torres = tk.Frame(
        frame_central,
        bg="#0d0000",
        padx=10
    )
    frame_torres.pack(side="left")

    torre_sel = tk.StringVar(value="Torre1")

    tk.Label(
        frame_torres,
        text="TORRES:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Torre ($50)",
        variable=torre_sel,
        value="Torre1",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Disparadora ($80)",
        variable=torre_sel,
        value="Torre2",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Cactus ($60)",
        variable=torre_sel,
        value="Torre3",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")

    costos = {"Torre1": 50, "Torre2": 80, "Torre3": 60}

    def colocar_torre(f, c):
        tipo = torre_sel.get()
        costo = costos[tipo]
        if dinero[0] < costo:
            return
        dinero[0] -= costo
        lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")

        if tipo == "Torre1":
            color_torre = "#ff2200"
            color_onda = "#ff7700"
            texto = "T"
        elif tipo == "Torre2":
            color_torre = "#0000ff"
            color_onda = "#00aaff"
            texto = "D"
        else:
            color_torre = "#00aa00"
            color_onda = "#00ff00"
            texto = "C"

        juego.torre = Torre(
            mapa=juego.mapa,
            ventana=ventana,
            actualizar_celda=juego.actualizar_celda,
            fila=f, col=c,
            color_torre="#ff2200",
            color_onda="#ff7700",
            vecinos=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)],
            velocidad=500,
            vida=120,
            daño=60,
            texto=texto
        )
        juego.mapa[f][c] = 1
        juego.actualizar_celda(f, c)

    juego.callback_clic = colocar_torre

    tk.Button(
        frame_actual,
        text="☣  LISTO  ☣",
        command=lambda: print("fase atacante"),
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)



def mostrar_seleccion_roles(defensor, atacante):
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
        text="─── SELECCIONAR ROL ───",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(0, 20))

    tk.Label(
        frame_actual,
        text=f"{defensor.upper()} — elige tu rol (Defensor):",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_VERDE
    ).pack(anchor="w")
    
    rol_defensor = tk.StringVar(value="Humanos")
    for rol in ["Humanos", "Militares", "Infectados"]:
        tk.Radiobutton(
            frame_actual,
            text=rol,
            variable=rol_defensor,
            value=rol,
            bg="#0d0000",
            fg=COLOR_ROJO_VIF,
            selectcolor="#1a0000",
            font=FUENTE_NORMAL
        ).pack(anchor="w")

    tk.Label(
        frame_actual,
        text="",
        bg="#0d0000"
    ).pack(pady=5)

    tk.Label(
        frame_actual,
        text=f"{atacante.upper()} — elige tu rol (Atacante):",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_VERDE
    ).pack(anchor="w")
    
    rol_atacante = tk.StringVar(value="Infectados")
    for rol in ["Humanos", "Militares", "Infectados"]:
        tk.Radiobutton(
            frame_actual,
            text=rol,
            variable=rol_atacante,
            value=rol,
            bg="#0d0000",
            fg=COLOR_ROJO_VIF,
            selectcolor="#1a0000",
            font=FUENTE_NORMAL
        ).pack(anchor="w")

    lbl_error = tk.Label(
        frame_actual,
        text="",
        font=FUENTE_SMALL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    )
    lbl_error.pack(pady=5)

    def confirmar():
        if rol_defensor.get() == rol_atacante.get():
            lbl_error.config(text="⚠ Los roles deben ser diferentes")
            return
        mostrar_fase_defensor(defensor, atacante, rol_defensor.get(), rol_atacante.get())

    tk.Button(
        frame_actual,
        text="☣  CONFIRMAR  ☣",
        command=confirmar,
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
        text="← VOLVER",
        command=lambda: mostrar_login_atacante(defensor),
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=4)




def mostrar_login_atacante(defensor):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana, bg = "#0d0000",
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
        text = "---JUGADOR 2 INICIAR SESION---",
        font = FUENTE_BTN,
        bg="#0d0000",
        fg= COLOR_ROJO_VIF
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
        if usuario == defensor:
            lbl_error.config(text="⚠ El jugador 2 debe ser diferente al jugador 1")
            return
        with open(RUTA_JSON, "r") as archivo:
            jugadores = json.load(archivo)
        for jugador in jugadores:
            if jugador["usuario"] == usuario:
                if jugador["contrasena"] == contra:
                    mostrar_seleccion_roles(defensor, usuario)
                    return
                else:
                    lbl_error.config(text="⚠ Contraseña incorrecta")
                    return
        lbl_error.config(text="⚠ El usuario no existe")

    tk.Button(
        frame_actual,
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
        command=lambda: mostrar_menu_principal(defensor),
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=4)
        


    
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
        command=lambda: mostrar_login_atacante(usuario),
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
Ventana de inicio, menu incial
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


fondo_inicio_img = tk.PhotoImage(file="fondo_login.png")
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














ventana.mainloop()

    
