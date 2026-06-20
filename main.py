#import zone
import os

CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

import tkinter as tk
import json
from tkinter import messagebox
from clases import VentanaMapa, Torre1, Torre2, Torre3, Zombie, Corredor, Tanque


COLOR_FONDO = "#0a0a0a"
COLOR_VERDE = "#39ff14" 
COLOR_ROJO = "#8b0000"
COLOR_TEXTO = "#c8c8c8"
FUENTE_TITULO = ("Courier", 40, "bold")
FUENTE_NORMAL = ("Courier", 12)
FUENTE_BTN   = ("Courier", 14, "bold")
FUENTE_SMALL = ("Courier", 10)
COLOR_ROJO_VIF = "#FF0000"
RUTA_JSON = os.path.join(CARPETA_PROYECTO, "jugadores.json")


# Clase de soporte local para asegurar que el muro funcione sin depender de archivos externos
class MuroDefensa:
    def __init__(self, fila, col):
        self.fila = fila
        self.col = col
        self.vida = 100
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
def mostrar_fase_defensor(defensor, atacante, rol_defensor, rol_atacante):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000"
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

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

    dinero = [300]
    lbl_dinero = tk.Label(
        frame_actual, text=f"💰 Dinero: {dinero[0]}",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg="#FFD700"
    )
    lbl_dinero.pack()

    frame_central = tk.Frame(
        frame_actual,
        bg="#0d0000"
    )
    frame_central.pack(pady=10)

    frame_mapa = tk.Frame(
        frame_central,
        bg="#0d0000"
    )
    frame_mapa.pack(side="left", padx=10)
    juego = VentanaMapa(frame_mapa)

    frame_torres = tk.Frame(
        frame_central,
        bg="#0d0000",
        padx=10
    )
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
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}"))
            return
            
        tipo = sel.get()
        costo = costos[tipo]
        if dinero[0] < costo:
            lbl_dinero.config(text="⚠ No tienes suficiente dinero")
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}"))
            return

        dinero[0] -= costo
        lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")

        if tipo == "Torre1":
            try:
                torre = Torre1(mapa=juego.mapa, ventana=ventana, fila=f, col=c, actualizar_celda=juego.actualizar_celda,
                           color_torre1="#ff0000", color_onda="#00ff00", vida=150, daño=15, texto="T")
                torre.colocar()
                torre.animar()
            except:
                class GenericT1:
                    def __init__(self): self.fila, self.col, self.vida, self.daño, self.texto, self.color_1 = f, c, 150, 15, "T", "#ff0000"
                torre = GenericT1()
            juego.torres[(f,c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg="#ff0000", fg="white", text=f"T\nHP:150", font=("Courier", 9, "bold"))
            
        elif tipo == "Torre2":
            try:
                torre = Torre2(mapa=juego.mapa, ventana=ventana, fila=f, col=c, actualizar_celda=juego.actualizar_celda,
                           color_1="#00aa00", color_2="#00ff00", vida=200, daño=20, texto="C")
                torre.colocar()
                torre.animar()
            except:
                class GenericT2:
                    def __init__(self): self.fila, self.col, self.vida, self.daño, self.texto, self.color_1 = f, c, 200, 20, "C", "#00aa00"
                torre = GenericT2()
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg="#00aa00", fg="white", text=f"C\nHP:200", font=("Courier", 9, "bold"))
            
        elif tipo == "Torre3":
            # SOLUCIÓN ABSOLUTA AL DISPARADOR: try-except de control total + Forzado gráfico inmediato
            try:
                torre = Torre3(mapa=juego.mapa, ventana=ventana, fila=f, col=c, actualizar_celda=juego.actualizar_celda,
                           color_1="#0000ff", color_bala="#ffffff", vida=120, daño=35, texto="D")
                torre.colocar()
                if hasattr(torre, "animar"): torre.animar()
            except:
                class GenericT3:
                    def __init__(self): self.fila, self.col, self.vida, self.daño, self.texto, self.color_1 = f, c, 120, 35, "D", "#0000ff"
                torre = GenericT3()
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
            
            def forzar_render():
                if (f, c) in juego.torres:
                    juego.botones[f][c].config(bg="#0000ff", fg="white", text="D\nHP:120", font=("Courier", 9, "bold"))
            forzar_render()
            ventana.after(50, forzar_render)

        elif tipo == "Muro":
            torre = MuroDefensa(f, c)
            juego.torres[(f, c)] = torre
            juego.mapa[f][c] = 1
            juego.botones[f][c].config(bg="#555555", fg="white", text="M\nHP:100", font=("Courier", 9, "bold"))

    juego.callback_clic = colocar_torre
    juego.torres = {}

    tk.Button(
        frame_actual,
        text="☣  LISTO  ☣",
        command=lambda: mostrar_fase_atacante(defensor, atacante, rol_defensor, rol_atacante, juego.mapa, juego.torres) if len(juego.torres) > 0 else lbl_dinero.config(text="⚠ Debes colocar al menos una torre"),
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
def mostrar_fase_atacante(defensor, atacante, rol_defensor, rol_atacante, mapa_defensor, torres_defensor):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000"
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame_actual,
        text="FASE DE ATAQUE",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(10,0))

    tk.Label(
        frame_actual,
        text=f"{atacante.upper()} — compra tus unidades",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_VERDE
    ).pack()

    dinero = [300]
    lbl_dinero = tk.Label(
        frame_actual,
        text=f"💰 Dinero: {dinero[0]}",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg="#FFD700"
    )
    lbl_dinero.pack()

    frame_central = tk.Frame(
        frame_actual,
        bg="#0d0000"
    )
    frame_central.pack(pady=10)

    frame_mapa = tk.Frame(
        frame_central,
        bg="#0d0000"
    )
    frame_mapa.pack(side="left", padx=10)
    juego_atk = VentanaMapa(frame_mapa)

    frame_unidades = tk.Frame(
        frame_central,
        bg="#0d0000",
        padx=10
    )
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
    
    # SOLUCIÓN AL CORREDOR Y AL TANQUE: Ahora todos usan la variable 'unidad_sel' de manera correcta
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
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}"))
            return
        tipo = unidad_sel.get()
        costo = costos[tipo]
        if dinero[0] < costo:
            lbl_dinero.config(text="⚠ No tienes suficiente dinero")
            ventana.after(1500, lambda: lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}"))
            return
        dinero[0] -= costo
        lbl_dinero.config(text=f"💰 Dinero: {dinero[0]}")

        if tipo == "Zombie":
            unidad = Zombie(juego_atk.mapa, f, 9)
        elif tipo == "Corredor":
            unidad = Corredor(juego_atk.mapa, f, 9)
        elif tipo == "Tanque":
            unidad = Tanque(juego_atk.mapa, f, 9)

        juego_atk.mapa[f][9] = 5
        juego_atk.botones[f][9].config(bg=unidad.color, fg="black", text=unidad.texto)
        unidades_colocadas.append(unidad)

    juego_atk.callback_clic = colocar_unidad

    tk.Button(
        frame_actual,
        text="☣  INICIAR COMBATE  ☣",
        command=lambda: mostrar_combate(defensor, atacante, rol_defensor, rol_atacante, mapa_defensor, torres_defensor, unidades_colocadas),
        font=FUENTE_BTN, bg="#1a0000",
        fg=COLOR_ROJO_VIF,
        relief="flat",
        cursor="hand2",
        padx=40,
        pady=12,
        width=20
    ).pack(pady=8)


"""
Modo Combate Balanceado con Sistema de HP en vivo
"""
def mostrar_combate(defensor, atacante, rol_defensor, rol_atacante, mapa_defensor, torres_defensor, unidades_colocadas):
    global frame_actual
    if frame_actual:
        frame_actual.destroy()

    frame_actual = tk.Frame(
        ventana,
        bg="#0d0000"
    )
    frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame_actual,
        text="⚔️ COMBATE BALANCED",
        font=FUENTE_BTN,
        bg="#0d0000",
        fg=COLOR_ROJO_VIF
    ).pack(pady=(10,0))

    vida_base = [100]

    lbl_base = tk.Label(
        frame_actual,
        text=f"🏰 Base: {vida_base[0]} HP",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg="#FFD700"
    )
    lbl_base.pack()

    lbl_estado = tk.Label(
        frame_actual,
        text="Haz clic abajo para iniciar la ronda",
        font=FUENTE_NORMAL,
        bg="#0d0000",
        fg=COLOR_VERDE
    )
    lbl_estado.pack()

    mapa = [fila[:] for fila in mapa_defensor]

    unidades = []
    for u in unidades_colocadas:
        # Valores de vida balanceados 
        if u.nombre == "Tanque": vida_inicial = 250
        elif u.nombre == "Corredor": vida_inicial = 70
        else: vida_inicial = 100
        
        unidades.append({"tipo": u.nombre, "fila": u.fila, "col": 9, "vida": vida_inicial})
        mapa[u.fila][9] = 6

    colores_unidad = {u.nombre: u.color for u in unidades_colocadas}
    textos_unidad = {u.nombre: u.texto for u in unidades_colocadas}

    frame_mapa = tk.Frame(
        frame_actual,
        bg="#0d0000"
    )
    frame_mapa.pack(pady=10)
    juego_combate = VentanaMapa(frame_mapa)

    for f in range(10):
        for c in range(10):
            if mapa[f][c] == 1:
                torre = torres_defensor.get((f, c))
                texto_id = getattr(torre, "texto", "T") if torre else "T"
                vida_t = getattr(torre, "vida", 150)
                
                if texto_id == "D": color = "#0000ff"
                elif texto_id == "C": color = "#00aa00"
                elif texto_id == "M": color = "#555555"
                else: color = "#ff2200"
                
                juego_combate.botones[f][c].config(bg=color, fg="white", text=f"{texto_id}\nHP:{vida_t}", font=("Courier", 9, "bold"))
                juego_combate.mapa[f][c] = 1
            elif mapa[f][c] == 6:
                juego_combate.mapa[f][c] = 6
                for u in unidades:
                    if u["fila"] == f and u["col"] == 9:
                        juego_combate.botones[f][c].config(bg=colores_unidad[u["tipo"]], fg="black", text=textos_unidad[u["tipo"]])

    def ejecutar_turno():
        #sistema de daño y vida
        for (tf, tc), torre in list(torres_defensor.items()):
            daño_torre = getattr(torre, "daño", 15)
            zombie_objetivo = None
            dist_minima_zombie = float('inf')
            
            for u in unidades:
                if u["vida"] > 0:
                    dist_z = abs(u["fila"] - tf) + abs(u["col"] - tc)
                    if dist_z < dist_minima_zombie:
                        dist_minima_zombie = dist_z
                        zombie_objetivo = u
            
            if zombie_objetivo:
                zombie_objetivo["vida"] -= daño_torre
                lbl_estado.config(text=f"🏹 Defensa en ({tf},{tc}) dañó a {zombie_objetivo['tipo']} (HP: {max(0, zombie_objetivo['vida'])})")
                if zombie_objetivo["vida"] <= 0:
                    juego_combate.mapa[zombie_objetivo["fila"]][zombie_objetivo["col"]] = 0
                    juego_combate.actualizar_celda(zombie_objetivo["fila"], zombie_objetivo["col"])

        # 2. IA Y DAÑO CONTINUO DE LOS ZOMBIES
        for u in unidades:
            if u["vida"] <= 0:
                continue
            
            col_actual = u["col"]
            fila_actual = u["fila"]

            juego_combate.mapa[fila_actual][col_actual] = 0
            juego_combate.actualizar_celda(fila_actual, col_actual)

            torre_cercana = None
            dist_minima = float('inf')
            for (tf, tc) in torres_defensor.keys():
                dist = abs(tf - fila_actual) + abs(tc - col_actual)
                if dist < dist_minima:
                    dist_minima = dist
                    torre_cercana = (tf, tc)

            if torre_cercana:
                tf, tc = torre_cercana
                opciones = []
                opciones.append((fila_actual, col_actual - 1, "izq"))
                if fila_actual > 0: opciones.append((fila_actual - 1, col_actual, "arr"))
                if fila_actual < 9: opciones.append((fila_actual + 1, col_actual, "aba"))

                mejor_opcion = opciones[0]
                mejor_dist = float('inf')

                for opf, opc, tipo_mov in opciones:
                    d = abs(opf - tf) + abs(opc - tc)
                    if tipo_mov == "izq": d -= 0.1 
                    if d < mejor_dist:
                        mejor_dist = d
                        mejor_opcion = (opf, opc, tipo_mov)

                sig_f, sig_c, _ = mejor_opcion
            else:
                sig_f = fila_actual
                sig_c = col_actual - 1

            # Lógica de colisión y ataque cuerpo a cuerpo
            if sig_c <= 0:
                vida_base[0] -= 20
                lbl_base.config(text=f"🏰 Base: {vida_base[0]} HP")
                u["vida"] = 0
                if vida_base[0] <= 0:
                    lbl_estado.config(text=f"💀 {atacante.upper()} GANÓ LA RONDA", fg=COLOR_ROJO_VIF)
                    return
            elif juego_combate.mapa[sig_f][sig_c] == 1:
                if (sig_f, sig_c) in torres_defensor:
                    torre = torres_defensor[(sig_f, sig_c)]
                    
                    # Daño balanceado por tipo de enemigo
                    daño_enemigo = 15
                    if u["tipo"] == "Tanque": daño_enemigo = 30
                    elif u["tipo"] == "Corredor": daño_enemigo = 10
                    
                    if not hasattr(torre, "vida"): torre.vida = 150
                    torre.vida -= daño_enemigo
                    texto_id = getattr(torre, "texto", "T")
                    
                    if torre.vida <= 0:
                        juego_combate.mapa[sig_f][sig_c] = 0
                        juego_combate.actualizar_celda(sig_f, sig_c)
                        del torres_defensor[(sig_f, sig_c)]
                        lbl_estado.config(text=f"💥 {u['tipo']} rompió la defensa en ({sig_f},{sig_c})!")
                        u["fila"] = sig_f
                        u["col"] = sig_c
                        juego_combate.mapa[sig_f][sig_c] = 6
                        juego_combate.botones[sig_f][sig_c].config(bg=colores_unidad[u["tipo"]], fg="black", text=textos_unidad[u["tipo"]])
                    else:
                        lbl_estado.config(text=f"🧟 {u['tipo']} atacó defensa en ({sig_f},{sig_c})! HP: {torre.vida}")
                        u["fila"] = fila_actual
                        u["col"] = col_actual
                        juego_combate.mapa[fila_actual][col_actual] = 6
                        juego_combate.botones[fila_actual][col_actual].config(bg=colores_unidad[u["tipo"]], fg="black", text=textos_unidad[u["tipo"]])
                        
                        if texto_id == "D": color_t = "#0000ff"
                        elif texto_id == "C": color_t = "#00aa00"
                        elif texto_id == "M": color_t = "#555555"
                        else: color_t = "#ff2200"
                        juego_combate.botones[sig_f][sig_c].config(bg=color_t, fg="white", text=f"{texto_id}\nHP:{torre.vida}")
            else:
                u["fila"] = sig_f
                u["col"] = sig_c
                juego_combate.mapa[sig_f][sig_c] = 6
                juego_combate.botones[sig_f][sig_c].config(bg=colores_unidad[u["tipo"]], fg="black", text=textos_unidad[u["tipo"]])
                
        vivas = [u for u in unidades if u["vida"] > 0]
        if not vivas and vida_base[0] > 0:
            lbl_estado.config(text=f"🛡️ {defensor.upper()} GANÓ LA RONDA", fg=COLOR_VERDE)
            return

        if vida_base[0] > 0 and vivas:
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


frame_actual = None
ventana = tk.Tk()
ventana.title("ATTACK US")
ventana.state("zoomed")

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
