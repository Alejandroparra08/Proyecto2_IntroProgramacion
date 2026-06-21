#import zone
import os
import random
CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

import tkinter as tk
import json
from tkinter import messagebox
from clases import VentanaMapa, Torre1, Torre2, Torre3, Zombie, Corredor, Tanque


frame_actual = None
btn_iniciar = None

victorias_defensor = [0]
victorias_atacante = [0]
ventana = tk.Tk()
ventana.title("ATTACK US")
ventana.state("zoomed")



COLOR_FONDO = "#0a0a0a"
COLOR_VERDE = "#39ff14" 
COLOR_ROJO = "#8b0000"
COLOR_TEXTO = "#c8c8c8"
FUENTE_TITULO = ("Courier", 40, "bold")
FUENTE_NORMAL = ("Courier", 12)
FUENTE_BTN   = ("Courier", 14, "bold")
FUENTE_SMALL = ("Courier", 10)


FACCIONES = {
    "Medieval": {
        "torre1": "#A0522D", "torre2": "#6B6B6B", "torre3": "#4A4A4A", 
        "muro": "#8B4513", "base": "#5C4033",
        "zombie": "#34495E", "corredor": "#D35400", "tanque": "#2C3E50"
    },
    "Futurista": {
        "torre1": "#00FFFF", "torre2": "#9400D3", "torre3": "#FF00FF", 
        "muro": "#2F2F2F", "base": "#1A1A2E",
        "zombie": "#00FF00", "corredor": "#FF3333", "tanque": "#3333FF"
    },
    "Naturaleza": {
        "torre1": "#556B2F", "torre2": "#2E8B57", "torre3": "#8FBC8F", 
        "muro": "#654321", "base": "#3B5323",
        "zombie": "#808000", "corredor": "#FF8C00", "tanque": "#8B0000"
    },
}


COLOR_ROJO_VIF = "#FF0000"
RUTA_JSON = os.path.join(CARPETA_PROYECTO, "jugadores.json")


# Clase de soporte local para asegurar que el muro funcione sin depender de archivos externos
class MuroDefensa:
    def __init__(self, fila, col):
        self.fila = fila
        self.col = col
        self.vida = 100
        self.vida_max = 100
        self.daño = 0
        self.texto = "M"
        self.color_1 = "#555555"
    def colocar(self): pass
    def animar(self): pass


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
Fase de Construcción del Defensor
"""
def mostrar_fase_defensor(defensor, atacante, rol_defensor, rol_atacante, faccion_defensor, faccion_atacante, dinero_def=400, dinero_atc=300):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(ventana, bg="#0d0000")
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_actual, text="FASE DE CONSTRUCCIÓN", font=FUENTE_BTN, bg="#0d0000", fg=COLOR_ROJO_VIF).pack(pady=(10,0))
    tk.Label(frame_actual, text=f"{defensor.upper()} — coloca tus defensas", font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_VERDE).pack()

    dinero = [dinero_def]
    lbl_dinero = tk.Label(frame_actual, text=f"💰 Dinero: {dinero[0]}", font=FUENTE_NORMAL, bg="#0d0000", fg="#FFD700")
    lbl_dinero.pack()
    
    frame_central = tk.Frame(frame_actual, bg="#0d0000")
    frame_central.pack(pady=10)

    frame_mapa = tk.Frame(frame_central, bg="#0d0000")
    frame_mapa.pack(side="left", padx=10)
    
    # Aquí es donde inyectamos el color correcto al mapa
    colores_elegidos = FACCIONES.get(faccion_defensor, FACCIONES["Medieval"])
    juego = VentanaMapa(frame_mapa, colores_faccion=colores_elegidos)

    frame_torres = tk.Frame(frame_central, bg="#0d0000", padx=10)
    frame_torres.pack(side="left")

    sel = tk.StringVar(value="Torre1")

    tk.Label(
        frame_torres,
        text="TORRES Y DEFENSAS:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Torre Común ($50)",
        variable=sel,
        value="Torre1",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Disparadora ($80)",
        variable=sel,
        value="Torre3",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_torres,
        text="Cactus ($60)",
        variable=sel,
        value="Torre2",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")

    tk.Radiobutton(
        frame_torres,
        text="Muro ($30)",
        variable=sel,
        value="Muro",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")

    tk.Label(
        frame_torres,
        text="",
        bg="#0d0000"
    ).pack(pady=5)

    tk.Radiobutton(
        frame_torres,
        text="🗑 Borrar",
        variable=sel,
        value="borrar",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")

    costos = {"Torre1": 50, "Torre3": 80, "Torre2": 60, "Muro": 30}

    def colocar_torre(f, c):
        if sel.get() == "borrar":
            if juego.mapa[f][c] == 1:
                juego.mapa[f][c] = 0
                juego.actualizar_celda(f, c)
                if (f, c) in juego.torres:
                    texto = getattr(juego.torres[(f, c)], "texto", "T")
                    if texto == "T": dinero[0] += 50
                    elif texto == "D": dinero[0] += 80
                    elif texto == "C": dinero[0] += 60
                    elif texto == "M": dinero[0] += 30
                    del juego.torres[(f, c)]
                    lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")
            return
    
        if c == 0 or c > 4:
            lbl_dinero.config(text="⚠ Solo puedes colocar torres en columnas 1-4")
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}") if lbl_dinero.winfo_exists() else None)
            return
            
        tipo = sel.get()
        costo = costos[tipo]
        if dinero[0] < costo:
            lbl_dinero.config(text="⚠ No tienes suficiente dinero")
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}") if lbl_dinero.winfo_exists() else None)
            return

        dinero[0] -= costo
        lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")
        

        
        if tipo == "Torre1":
            color_torre = colores_elegidos.get("torre1", "#ff0000")
            color_onda = "#00ff00"  # puedes cambiar esto también por facción después
                
            torre = Torre1(mapa=juego.mapa, ventana=ventana, fila=f, col=c, 
                            actualizar_celda=juego.actualizar_celda,
                            color_torre1=color_torre, 
                            color_onda=color_onda, 
                            vida=130, daño=15, texto="T")
            torre.colocar()
                    
            juego.torres[(f,c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg=color_torre, fg="white", 
                                              text=f"T\nHP:130", font=("Courier", 9, "bold"))

        elif tipo == "Torre2":
            color_torre = colores_elegidos.get("torre2", "#00aa00")
                    
            torre = Torre2(mapa=juego.mapa, ventana=ventana, fila=f, col=c, 
                                actualizar_celda=juego.actualizar_celda,
                                color_1=color_torre, color_2="#00ff00", 
                                vida=170, daño=14, texto="C")
            torre.colocar()
                    
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg=color_torre, fg="white", 
                                              text=f"C\nHP:170", font=("Courier", 9, "bold"))




        elif tipo == "Torre3":
            color_torre = colores_elegidos.get("torre3", "#0000ff")
                    
            torre = Torre3(mapa=juego.mapa, ventana=ventana, fila=f, col=c, 
                                   actualizar_celda=juego.actualizar_celda,
                                   color_1=color_torre, vida=120, daño=16, texto="D")
            torre.colocar()
                    
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
                    
            juego.botones[f][c].config(bg=color_torre, fg="white", 
                                              text="D\nHP:120", font=("Courier", 9, "bold"))

        elif tipo == "Muro":
            color_muro = colores_elegidos.get("muro", "#555555")
            torre = MuroDefensa(f, c)
            torre.color_1 = color_muro   # ← Agregamos esto
                    
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg=color_muro, fg="white", 
                                      text="M\nHP:100", font=("Courier", 9, "bold"))
        

        
    juego.callback_clic = colocar_torre
    juego.torres = {}

    tk.Button(
            frame_actual,
            text="☣  LISTO  ☣",
            command=lambda: mostrar_fase_atacante(
                defensor, 
                atacante, 
                rol_defensor, 
                rol_atacante, 
                juego.mapa, 
                juego.torres, 
                dinero[0], 
                dinero_atc,   
                faccion_defensor, 
                faccion_atacante
            ) if len(juego.torres) > 0 else lbl_dinero.config(text="⚠ Debes colocar al menos una torre"),
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
Fase de Compra del Atacante
"""
def mostrar_fase_atacante(defensor, atacante, rol_defensor, rol_atacante, mapa_defensor, torres_defensor, dinero_defensor, dinero_atacante, faccion_defensor, faccion_atacante):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(ventana, bg="#0d0000")
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_actual, text="FASE DE ATAQUE", font=FUENTE_BTN, bg="#0d0000", fg=COLOR_ROJO_VIF).pack(pady=(10,0))
    tk.Label(frame_actual, text=f"{atacante.upper()} — compra tus unidades", font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_VERDE).pack()



    dinero = [dinero_atacante]
    lbl_dinero = tk.Label(frame_actual, text=f"💰 Dinero: {dinero[0]}", font=FUENTE_NORMAL, bg="#0d0000", fg="#FFD700")
    lbl_dinero.pack()

    # Condición de victoria del defensor: el atacante se queda sin dinero
    costo_minimo = 40
    if dinero[0] < costo_minimo:
        global victorias_defensor
        victorias_defensor[0] += 1

        tk.Label(
            frame_actual,
            text=f"⚠️ {atacante.upper()} se quedó sin dinero — ni siquiera le alcanza para un Zombie",
            font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_ROJO_VIF
        ).pack(pady=10)
        tk.Label(
            frame_actual,
            text=f"🛡️ {defensor.upper()} GANÓ LA RONDA ({victorias_defensor[0]}/3)",
            font=FUENTE_BTN, bg="#0d0000", fg=COLOR_VERDE
        ).pack(pady=10)

        if victorias_defensor[0] >= 3:
            tk.Label(
                frame_actual,
                text=f"🏆 {defensor.upper()} GANÓ LA PARTIDA",
                font=FUENTE_BTN, bg="#0d0000", fg=COLOR_VERDE
            ).pack(pady=10)
            actualizar_victorias(defensor, "defensor")
            tk.Button(
                frame_actual, text="← VOLVER AL MENÚ",
                command=lambda: mostrar_menu_principal(defensor),
                font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF,
                relief="flat", cursor="hand2"
            ).pack(pady=10)
            return

        tk.Button(
            frame_actual,
            text="☣  Iniciar Siguiente Ronda  ☣",
            command=lambda: mostrar_fase_defensor(
                defensor, atacante, rol_defensor, rol_atacante,
                faccion_defensor, faccion_atacante,
                dinero_defensor + 300, dinero[0] + 300
            ),
            font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF,
            relief="flat", cursor="hand2", padx=40, pady=12, width=24
        ).pack(pady=10)
        return

    frame_central = tk.Frame(frame_actual, bg="#0d0000")
    frame_central.pack(pady=10)



    frame_mapa = tk.Frame(frame_central, bg="#0d0000")
    frame_mapa.pack(side="left", padx=10)
    
    # Inyectamos el color para el atacante
    colores_elegidos = FACCIONES.get(faccion_atacante, FACCIONES["Futurista"])
    juego_atk = VentanaMapa(frame_mapa, colores_faccion=colores_elegidos)

    frame_unidades = tk.Frame(frame_central, bg="#0d0000", padx=10)
    frame_unidades.pack(side="left")

    unidad_sel = tk.StringVar(value="Zombie")

    tk.Label(
        frame_unidades,
        text="UNIDADES:",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_unidades,
        text="Zombie ($40)",
        variable=unidad_sel,
        value="Zombie",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    
    tk.Radiobutton(
        frame_unidades,
        text="Corredor ($60)",
        variable=unidad_sel,
        value="Corredor",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")
    
    tk.Radiobutton(
        frame_unidades,
        text="Tanque ($100)",
        variable=unidad_sel,
        value="Tanque",
        bg="#0d0000",
        fg=COLOR_ROJO_VIF,
        selectcolor="#1a0000",
        font=FUENTE_NORMAL
    ).pack(anchor="w")

    costos = {"Zombie": 40, "Corredor": 60, "Tanque": 100}
    unidades_colocadas = []

    def colocar_unidad(f, c):
            if c != 9:
                lbl_dinero.config(text="⚠ Solo puedes colocar en la columna derecha")
                ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}") if lbl_dinero.winfo_exists() else None)
                return
            
            tipo = unidad_sel.get()
            costo = costos[tipo]
            if dinero[0] < costo:
                lbl_dinero.config(text="⚠ No tienes suficiente dinero")
                ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}") if lbl_dinero.winfo_exists() else None)
                return
            
            dinero[0] -= costo
            lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")

            # Colores según facción del atacante
            colores_atk = FACCIONES.get(faccion_atacante, FACCIONES["Futurista"])

            if tipo == "Zombie":
                color_z = colores_atk.get("zombie", "#39ff14")
                unidad = Zombie(juego_atk.mapa, f, 9)
                unidad.color = color_z
            elif tipo == "Corredor":
                color_c = colores_atk.get("corredor", "#ffff00")
                unidad = Corredor(juego_atk.mapa, f, 9)
                unidad.color = color_c
            elif tipo == "Tanque":
                color_t = colores_atk.get("tanque", "#ff6600")
                unidad = Tanque(juego_atk.mapa, f, 9)
                unidad.color = color_t

            juego_atk.mapa[f][9] = 6
            juego_atk.botones[f][9].config(bg=unidad.color, fg="black", text=unidad.texto)
            unidades_colocadas.append(unidad)

    juego_atk.callback_clic = colocar_unidad

    tk.Button(
            frame_actual,
            text="☣  INICIAR COMBATE  ☣",
            command=lambda: mostrar_combate(
                defensor, 
                atacante, 
                rol_defensor, 
                rol_atacante, 
                faccion_defensor,     
                faccion_atacante,      
                mapa_defensor, 
                torres_defensor, 
                unidades_colocadas, 
                dinero_defensor, 
                dinero[0]
            ),
            font=FUENTE_BTN, 
            bg="#1a0000",
            fg=COLOR_ROJO_VIF,
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=12,
            width=20
        ).pack(pady=8)


def actualizar_victorias(usuario, rol):
    with open(RUTA_JSON, "r") as archivo:
        jugadores = json.load(archivo)
    for jugador in jugadores:
        if jugador["usuario"] == usuario:
            if rol == "defensor":
                jugador["victorias_defensor"] += 1
            else:
                jugador["victorias_atacante"] += 1
    with open(RUTA_JSON, "w") as archivo:
        json.dump(jugadores, archivo, indent=4)


        
"""
Modo Combate Balanceado con Sistema de HP en vivo
"""

def mostrar_combate(defensor, atacante, rol_defensor, rol_atacante, faccion_defensor, faccion_atacante, mapa_defensor, torres_defensor, unidades_colocadas, dinero_defensor, dinero_atacante):
    global frame_actual, victorias_defensor, victorias_atacante, btn_iniciar

    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(ventana, bg="#0d0000")
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_actual, text="⚔️ COMBATE BALANCED", font=FUENTE_BTN, bg="#0d0000", fg=COLOR_ROJO_VIF).pack(pady=(10, 0))

    vida_base = [100]
    contador_turnos = [0]
    dinero_def = [dinero_defensor]
    dinero_atc = [dinero_atacante]
    torres_pagadas = set()

    lbl_base = tk.Label(frame_actual, text=f"🏰 Base: {vida_base[0]} HP", font=FUENTE_NORMAL, bg="#0d0000", fg="#FFD700")
    lbl_base.pack()

    frame_dinero = tk.Frame(frame_actual, bg="#0d0000")
    frame_dinero.pack()

    lbl_dinero_def = tk.Label(frame_dinero, text=f"🛡️ {defensor}: 💰 {dinero_def[0]}", font=FUENTE_NORMAL, bg="#0d0000", fg="#FFD700")
    lbl_dinero_def.pack(side="left", padx=10)

    lbl_dinero_atc = tk.Label(frame_dinero, text=f"💀 {atacante}: 💰 {dinero_atc[0]}", font=FUENTE_NORMAL, bg="#0d0000", fg="#FFD700")
    lbl_dinero_atc.pack(side="left", padx=10)

    lbl_estado = tk.Label(frame_actual, text="Haz clic abajo para iniciar la ronda", font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_VERDE)
    lbl_estado.pack()

    mapa = [fila[:] for fila in mapa_defensor]
    unidades = list(unidades_colocadas)

    frame_mapa = tk.Frame(frame_actual, bg="#0d0000")
    frame_mapa.pack(pady=10)

   
    colores_elegidos_defensor = FACCIONES.get(faccion_defensor, FACCIONES["Medieval"])
    juego_combate = VentanaMapa(frame_mapa, colores_faccion=colores_elegidos_defensor)

    def dibujar_torre(f, c, torre):
                texto_id = getattr(torre, "texto", "T")
                vida_t = max(0, getattr(torre, "vida", 150))

                # Colores según facción del defensor (mejorado)
                if texto_id == "T":
                    color_base = colores_elegidos_defensor.get("torre1", "#ff2200")
                elif texto_id == "C":
                    color_base = colores_elegidos_defensor.get("torre2", "#00aa00")
                elif texto_id == "D":
                    color_base = colores_elegidos_defensor.get("torre3", "#0000ff")
                elif texto_id == "M":
                    color_base = colores_elegidos_defensor.get("muro", "#555555")
                else:
                    color_base = colores_elegidos_defensor.get("torre1", "#ff2200")

                # 🟢 LA LÍNEA CLAVE: Le decimos a la matriz lógica que aquí hay una torre (1)
                juego_combate.mapa[f][c] = 1

                juego_combate.botones[f][c].config(
                    bg=color_base,
                    fg="white",
                    text=f"{texto_id}\nHP:{vida_t}",
                    font=("Courier", 9, "bold")
                )
   
    def dibujar_unidad(u):
        if 0 <= u.fila < 10 and 0 <= u.col < 10:
            juego_combate.mapa[u.fila][u.col] = 6
            juego_combate.botones[u.fila][u.col].config(
                bg=u.color,
                fg="black",
                text=f"{u.texto}\n{u.vida}",
                font=("Courier", 9, "bold")
            )

    def limpiar_celda(f, c):
        if 0 <= f < 10 and 0 <= c < 10:
            juego_combate.mapa[f][c] = 0
            juego_combate.actualizar_celda(f, c)

    # Dibujar torres primero
    for f in range(10):
        for c in range(10):
            if mapa[f][c] == 1:
                torre = torres_defensor.get((f, c))
                if torre:
                    dibujar_torre(f, c, torre)

    # Dibujar unidades al iniciar combate
    for u in unidades:
        dibujar_unidad(u)

    def ejecutar_turno():
        contador_turnos[0] += 1

        # Regeneración del Tanque cada 3 turnos
        if contador_turnos[0] % 3 == 0:
            for tanque in unidades:
                if tanque.vida > 0 and tanque.nombre == "Tanque":
                    tanque.regenerar_aliados(unidades)



        
        for (tf, tc), torre in list(torres_defensor.items()):
            if torre is None:
                continue

            texto_torre = getattr(torre, "texto", "T")
            if texto_torre == "M":
                continue

            daño_torre = getattr(torre, "daño", 15)
            rango_torre = getattr(torre, "alcance", 3)

            objetivo = None
            objetivos_t1 = []
            dist_minima = float("inf")

            if texto_torre == "D":
                # Disparador: frente y diagonales derechas hasta 3 casillas,
                # además puede disparar arriba y abajo en su misma columna hasta 3 casillas
                for u in unidades:
                    if u.vida > 0:
                        misma_o_diagonal = abs(u.fila - tf) <= 1
                        hacia_adelante = 0 <= (u.col - tc) <= 3
                        en_cono_frontal = misma_o_diagonal and hacia_adelante

                        misma_columna = u.col == tc
                        arriba_o_abajo = 0 < abs(u.fila - tf) <= 3
                        en_linea_vertical = misma_columna and arriba_o_abajo

                        if en_cono_frontal:
                            dist = u.col - tc
                            if dist < dist_minima:
                                dist_minima = dist
                                objetivo = u
                        elif en_linea_vertical:
                            dist = abs(u.fila - tf)
                            if dist < dist_minima:
                                dist_minima = dist
                                objetivo = u

            elif texto_torre == "T":
                # Torre1: onda 3x3
                for u in unidades:
                    if u.vida > 0:
                        if abs(u.fila - tf) <= 1 and abs(u.col - tc) <= 1 and not (u.fila == tf and u.col == tc):
                            objetivos_t1.append(u)

            else:
                # Torre2 / otras: objetivo más cercano por Manhattan
                for u in unidades:
                    if u.vida > 0:
                        dist = abs(u.fila - tf) + abs(u.col - tc)
                        if dist <= rango_torre and dist < dist_minima:
                            dist_minima = dist
                            objetivo = u

            # Aplicar daño Torre1
            if texto_torre == "T" and objetivos_t1:
                nombres = []
                for e in objetivos_t1:
                    e.vida -= daño_torre
                    e.vida = max(0, e.vida)
                    nombres.append(f"{e.nombre}({e.fila},{e.col})")

                    if e.vida <= 0:
                        limpiar_celda(e.fila, e.col)
                        dinero_def[0] += 35
                        lbl_dinero_def.config(text=f"🛡️ {defensor}: 💰 {dinero_def[0]}")
                    else:
                        dibujar_unidad(e)

                lbl_estado.config(text=f"💥 Torre1 ({tf},{tc}) golpeó: " + ", ".join(nombres))

                if hasattr(torre, "animar"):
                    torre.animar(juego_combate, ventana)

            # Aplicar daño normal
            elif objetivo:
                objetivo.vida -= daño_torre
                objetivo.vida = max(0, objetivo.vida)

                lbl_estado.config(
                    text=f"🏹 Defensa en ({tf},{tc}) dañó a {objetivo.nombre} (HP: {objetivo.vida})"
                )

                if hasattr(torre, "animar"):
                    if texto_torre == "D":
                        torre.animar(juego_combate, ventana, objetivo.fila, objetivo.col)
                    else:
                        torre.animar(juego_combate, ventana)

                if texto_torre == "D" and random.random() < 0.30:
                    objetivo.turnos_paralizado = 2
                    lbl_estado.config(text=f"⚡ ¡{objetivo.nombre} quedó paralizado por 2 turnos!")

                # Habilidad de Torre2 (Cactus): cuando le queda poca vida, ataca más rápido (golpe extra en el mismo turno)
                if texto_torre == "C" and objetivo.vida > 0:
                    vida_max_torre = getattr(torre, "vida_max", 200)
                    if getattr(torre, "vida", 0) < vida_max_torre * 0.30:
                        objetivo.vida -= daño_torre
                        objetivo.vida = max(0, objetivo.vida)
                        lbl_estado.config(text=f"🌵⚡ ¡Cactus con poca vida atacó dos veces! {objetivo.nombre} HP: {objetivo.vida}")
                        if hasattr(torre, "animar"):
                            torre.animar(juego_combate, ventana)

                if objetivo.vida <= 0:
                    limpiar_celda(objetivo.fila, objetivo.col)
                    dinero_def[0] += 35
                    lbl_dinero_def.config(text=f"🛡️ {defensor}: 💰 {dinero_def[0]}")
                else:
                    dibujar_unidad(objetivo)

                # refrescar torre visual
                if getattr(torre, "vida", None) is not None:
                    if texto_torre == "D":
                        color_t = colores_elegidos_defensor.get("torre3", "#0000ff")
                    elif texto_torre == "C":
                        color_t = colores_elegidos_defensor.get("torre2", "#00aa00")
                    elif texto_torre == "M":
                        color_t = colores_elegidos_defensor.get("muro", "#555555")
                    else:
                        color_t = colores_elegidos_defensor.get("torre1", "#ff2200")

                    ventana.after(
                        150,
                        lambda f=tf, c=tc, cl=color_t, tx=texto_torre, hp=getattr(torre, "vida", 150):
                            juego_combate.botones[f][c].config(
                                bg=cl,
                                fg="white",
                                text=f"{tx}\nHP:{hp}"
                            ) if juego_combate.mapa[f][c] == 1 else None
                    )

        for u in unidades:
            if u.vida <= 0:
                continue

            if u.turnos_paralizado > 0:
                u.turnos_paralizado -= 1
                continue

            pasos = u.velocidad

            # Sprint del Corredor: si le quedan turnos de sprint, avanza 2 celdas en vez de 1
            if u.nombre == "Corredor" and u.turnos_sprint > 0:
                pasos = 2
                u.turnos_sprint -= 1

            ataque_realizado = False

            # La unidad da hasta 'pasos' movimientos individuales este turno.
            # Antes de cada movimiento, revisa si ya puede atacar desde donde está.
            for _paso_individual in range(pasos):
                if u.vida <= 0:
                    break

                fila_actual = u.fila
                col_actual = u.col

                # ¿Hay una torre adyacente (1 celda en cualquiera de las 4 direcciones) ahora mismo?
                torre_objetivo_pos = None
                es_ataque_a_distancia = False
                direcciones_adyacentes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for df, dc in direcciones_adyacentes:
                    f_chk, c_chk = fila_actual + df, col_actual + dc
                    if 0 <= f_chk < 10 and 0 <= c_chk < 10:
                        if juego_combate.mapa[f_chk][c_chk] == 1 and (f_chk, c_chk) in torres_defensor:
                            torre_objetivo_pos = (f_chk, c_chk)
                            break

                # El Corredor también puede disparar a 2 celdas en línea recta, sin contraataque
                if torre_objetivo_pos is None and u.nombre == "Corredor":
                    for df, dc in direcciones_adyacentes:
                        f_chk, c_chk = fila_actual + df * 2, col_actual + dc * 2
                        if 0 <= f_chk < 10 and 0 <= c_chk < 10:
                            if juego_combate.mapa[f_chk][c_chk] == 1 and (f_chk, c_chk) in torres_defensor:
                                torre_objetivo_pos = (f_chk, c_chk)
                                es_ataque_a_distancia = True
                                break


                if torre_objetivo_pos:
                    
                    ataque_realizado = True
                    tf_obj, tc_obj = torre_objetivo_pos
                    torre = torres_defensor[(tf_obj, tc_obj)]
                    daño_enemigo = getattr(u, "daño", 15)
                    if not hasattr(torre, "vida"):
                        torre.vida = 150
                    torre.vida -= daño_enemigo

                    if torre_objetivo_pos not in torres_pagadas:
                        torres_pagadas.add(torre_objetivo_pos)
                        dinero_atc[0] += 15
                        lbl_dinero_atc.config(text=f"💀 {atacante}: 💰 {dinero_atc[0]}")



                    if not es_ataque_a_distancia:
                        daño_contraataque = getattr(torre, "daño", 15)
                        u.vida -= daño_contraataque
                        u.vida = max(0, u.vida)
                        if u.vida <= 0:
                            if u.nombre == "Zombie":
                                torre.vida -= 25
                                lbl_estado.config(text=f"💥 ¡El Zombie explotó al morir e hizo 25 de daño extra!")
                            limpiar_celda(fila_actual, col_actual)
                            dinero_def[0] += 35
                            lbl_dinero_def.config(text=f"🛡️ {defensor}: 💰 {dinero_def[0]}")
                    else:
                        lbl_estado.config(text=f"🏃‍♂️🎯 {u.nombre} disparó a distancia a la defensa en ({tf_obj},{tc_obj})! HP: {max(0, torre.vida)}")

                    if torre.vida <= 0:
                        limpiar_celda(tf_obj, tc_obj)
                        del torres_defensor[(tf_obj, tc_obj)]

                        dinero_atc[0] += 50
                        lbl_dinero_atc.config(text=f"💀 {atacante}: 💰 {dinero_atc[0]}")

                        if u.vida > 0:
                            lbl_estado.config(text=f"💥 {u.nombre} destruyó la defensa en ({tf_obj},{tc_obj})!")
                            if u.nombre == "Corredor":
                                u.turnos_sprint = 2
                                lbl_estado.config(text=f"💥⚡ ¡{u.nombre} destruyó la defensa y entró en sprint por 2 turnos!")
                    elif u.vida > 0:
                        dibujar_torre(tf_obj, tc_obj, torre)
                        lbl_estado.config(text=f"🧟 {u.nombre} atacó defensa en ({tf_obj},{tc_obj})! HP: {torre.vida}")

                    # Atacar consume el resto del turno de esta unidad (no sigue dando pasos)
                    break

                objetivo = None
                dist_min = float("inf")

                for (tf, tc) in torres_defensor.keys():
                    casillas_objetivo = [
                        (tf - 1, tc),
                        (tf + 1, tc),
                        (tf, tc - 1),
                        (tf, tc + 1),
                    ]

                    for of, oc in casillas_objetivo:
                        if 0 <= of < 10 and 0 <= oc < 10:
                            if juego_combate.mapa[of][oc] == 0:
                                d = abs(of - fila_actual) + abs(oc - col_actual)
                                if d < dist_min:
                                    dist_min = d
                                    objetivo = (of, oc)

                if objetivo:
                    of, oc = objetivo
                    nueva_f, nueva_c = fila_actual, col_actual

                    if fila_actual < of:
                        nueva_f += 1
                    elif fila_actual > of:
                        nueva_f -= 1

                    if col_actual < oc:
                        nueva_c += 1
                    elif col_actual > oc:
                        nueva_c -= 1
                else:
                    nueva_f, nueva_c = fila_actual, max(0, col_actual - 1)

                # Nunca moverse a una celda con torre (caso límite: ya estaba pegado pero no se detectó arriba)
                if juego_combate.mapa[nueva_f][nueva_c] == 1:
                    break

                # Si la celda de destino tiene otra unidad aliada, intentar rodear (arriba/abajo)
                if juego_combate.mapa[nueva_f][nueva_c] == 6 and (nueva_f, nueva_c) != (fila_actual, col_actual):
                    rodeo_encontrado = False
                    opciones_rodeo = []
                    if fila_actual > 0:
                        opciones_rodeo.append((fila_actual - 1, col_actual))
                    if fila_actual < 9:
                        opciones_rodeo.append((fila_actual + 1, col_actual))
                    for of, oc in opciones_rodeo:
                        if juego_combate.mapa[of][oc] == 0:
                            nueva_f, nueva_c = of, oc
                            rodeo_encontrado = True
                            break
                    if not rodeo_encontrado:
                        break  # no hay forma de avanzar este paso, se queda quieta

                # ¿Llegó a la base?
                if nueva_c <= 1:
                    limpiar_celda(fila_actual, col_actual)
                    vida_base[0] -= 25
                    lbl_base.config(text=f"🏰 Base: {vida_base[0]} HP")
                    u.vida = 0

                    dinero_atc[0] += 30
                    lbl_dinero_atc.config(text=f"💀 {atacante}: 💰 {dinero_atc[0]}")

                    if vida_base[0] <= 0:
                        victorias_atacante[0] += 1
                        lbl_estado.config(
                            text=f"💀 {atacante.upper()} GANÓ LA RONDA ({victorias_atacante[0]}/3)",
                            fg=COLOR_ROJO_VIF
                        )
                        if victorias_atacante[0] >= 3:
                            lbl_estado.config(text=f"🏆 {atacante.upper()} GANÓ LA PARTIDA", fg=COLOR_ROJO_VIF)
                            actualizar_victorias(atacante, "atacante")
                                                
                            tk.Button(frame_actual, text="← VOLVER AL MENÚ", command=lambda: mostrar_menu_principal(defensor), font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF, relief="flat", cursor="hand2").pack(pady=10)
                            return

                        btn_iniciar.config(
                            text="Iniciar Siguiente Ronda",
                            command=lambda: mostrar_fase_defensor(defensor, atacante, rol_defensor, rol_atacante, faccion_defensor, faccion_atacante, dinero_def[0] + 300, dinero_atc[0] + 300)
                        )
                        btn_iniciar.pack(pady=8)
                        return
                    break

                # Movimiento normal a celda vacía
                limpiar_celda(fila_actual, col_actual)
                u.fila = nueva_f
                u.col = nueva_c
                dibujar_unidad(u)

            # (fin del for de pasos individuales de esta unidad)

        # Limpiar muertos de la lista de unidades
        unidades[:] = [u for u in unidades if u.vida > 0]

        # Fin de ronda
        vivas = [u for u in unidades if u.vida > 0]

        if vida_base[0] <= 0:
            return

        if len(vivas) == 0:
            victorias_defensor[0] += 1
            lbl_estado.config(
                text=f"🛡️ {defensor.upper()} GANÓ LA RONDA ({victorias_defensor[0]}/3)",
                fg=COLOR_VERDE
            )

            if victorias_defensor[0] >= 3:
                lbl_estado.config(text=f"🏆 {defensor.upper()} GANÓ LA PARTIDA", fg=COLOR_VERDE)
                actualizar_victorias(defensor, "defensor")
                            
                tk.Button(frame_actual, text="← VOLVER AL MENÚ", command=lambda: mostrar_menu_principal(defensor), font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF, relief="flat", cursor="hand2").pack(pady=10)
                return

            btn_iniciar.config(
                text="Iniciar Siguiente Ronda",
                command=lambda: mostrar_fase_defensor(defensor, atacante, rol_defensor, rol_atacante, faccion_defensor, faccion_atacante, dinero_def[0] + 300, dinero_atc[0] + 300)
            )
            btn_iniciar.pack(pady=8)
            return

        ventana.after(1000, ejecutar_turno)

    btn_iniciar = tk.Button(
        frame_actual,
        text="▶ INICIAR RONDA",
        command=lambda: [btn_iniciar.pack_forget(), ejecutar_turno()],
        font=FUENTE_BTN,
        bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    )
    btn_iniciar.pack(pady=8)



"""
Controlador de Partidas, Menús y Logins Completos
"""
def mostrar_seleccion_faccion(defensor, atacante):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(ventana, bg="#0d0000", padx=40, pady=30)
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_actual, text="─── SELECCIONAR FACCIÓN ───", font=FUENTE_BTN, bg="#0d0000", fg=COLOR_ROJO_VIF).pack(pady=(0, 20))

    nombres_faccion = list(FACCIONES.keys())

    tk.Label(frame_actual, text=f"{defensor.upper()} — elige tu facción (Defensor):", font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_VERDE).pack(anchor="w")
    sel_faccion_defensor = tk.StringVar(value=nombres_faccion[0])
    for fac in nombres_faccion:
        tk.Radiobutton(frame_actual, text=fac, variable=sel_faccion_defensor, value=fac, bg="#0d0000", fg=COLOR_ROJO_VIF, selectcolor="#1a0000", font=FUENTE_NORMAL).pack(anchor="w")

    tk.Label(frame_actual, text="", bg="#0d0000").pack(pady=5)

    tk.Label(frame_actual, text=f"{atacante.upper()} — elige tu facción (Atacante):", font=FUENTE_NORMAL, bg="#0d0000", fg=COLOR_VERDE).pack(anchor="w")
    sel_faccion_atacante = tk.StringVar(value=nombres_faccion[1])
    for fac in nombres_faccion:
        tk.Radiobutton(frame_actual, text=fac, variable=sel_faccion_atacante, value=fac, bg="#0d0000", fg=COLOR_ROJO_VIF, selectcolor="#1a0000", font=FUENTE_NORMAL).pack(anchor="w")

    lbl_error = tk.Label(frame_actual, text="", font=FUENTE_SMALL, bg="#0d0000", fg=COLOR_ROJO_VIF)
    lbl_error.pack(pady=5)

    def confirmar():
        if sel_faccion_defensor.get() == sel_faccion_atacante.get():
            lbl_error.config(text="⚠ Las facciones deben ser diferentes")
            return
        # Enviamos "Defensor" y "Atacante" como roles de relleno para que nada se rompa
        mostrar_fase_defensor(defensor, atacante, "Defensor", "Atacante", sel_faccion_defensor.get(), sel_faccion_atacante.get())

    tk.Button(frame_actual, text="☣  CONFIRMAR  ☣", command=confirmar, font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF, relief="flat", cursor="hand2", padx=40, pady=12, width=20).pack(pady=8)
    tk.Button(frame_actual, text="← VOLVER", command=lambda: mostrar_login_atacante(defensor), font=FUENTE_BTN, bg="#1a0000", fg=COLOR_ROJO_VIF, relief="flat", cursor="hand2", padx=40, pady=12, width=20).pack(pady=4)




def mostrar_login_atacante(defensor):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana, bg = "#0d0000",
        padx=40,
        pady=30
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

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
                    mostrar_seleccion_faccion(defensor, usuario)
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

    def iniciar_nueva_partida():
        global victorias_defensor, victorias_atacante
        victorias_defensor[0] = 0
        victorias_atacante[0] = 0
        mostrar_login_atacante(usuario)

    tk.Button(
        frame_actual,
        text="☣  NUEVA PARTIDA  ☣",
        command=iniciar_nueva_partida,
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
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

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



fondo_inicio_img = tk.PhotoImage(
    file=os.path.join(CARPETA_PROYECTO, "fondo_login.png")
)
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
