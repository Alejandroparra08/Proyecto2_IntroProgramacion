import tkinter as tk

class VentanaMapa:
    def __init__(self, frame, colores_faccion=None):
        self.ventana = frame
        self.colores = colores_faccion or {
            "torre1": "#A0522D", "torre2": "#2E8B57", "torre3": "#4A4A4A",
            "muro": "#8B4513", "base": "#5C4033",
            "zombie": "#34495E", "corredor": "#D35400", "tanque": "#2C3E50"
        }
        
        self.filas = 10
        self.columnas = 10
        self.mapa = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.botones = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        self.callback_clic = None
        self.torres = {}

        self.crear_mapa()
        # Base central fija
        self.mapa[4][0] = 4
        self.actualizar_celda(4, 0)

    def clic_celda(self, f, c):
        if self.callback_clic:
            self.callback_clic(f, c)

    def crear_mapa(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                boton = tk.Button(
                    self.ventana,
                    width=6,      # ← Más ancho
                    height=3,     # ← Más alto
                    font=("Courier", 10, "bold"),
                    relief="solid",
                    bd=2,
                    command=lambda f=f, c=c: self.clic_celda(f, c)
                )
                boton.grid(row=f, column=c, padx=2, pady=2)
                self.botones[f][c] = boton
        self.actualizar_todo()

    def actualizar_todo(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                self.actualizar_celda(f, c)

    def actualizar_celda(self, f, c):
        valor = self.mapa[f][c]
        boton = self.botones[f][c]

        if valor == 0:
            boton.config(bg="#1d0800", fg="white", text=" ")

        elif valor == 1:  # Torre (se sobrescribirá después)
            torre = self.torres.get((f, c))
            texto_id = getattr(torre, "texto", "T") if torre else "T"
            vida_t = max(0, getattr(torre, "vida", 150)) if torre else 150

            if texto_id == "T":
                color_t = self.colores.get("torre1", "#A0522D")
            elif texto_id == "C":
                color_t = self.colores.get("torre2", "#2E8B57")
            elif texto_id == "D":
                color_t = self.colores.get("torre3", "#4A4A4A")
            elif texto_id == "M":
                color_t = self.colores.get("muro", "#8B4513")
            else:
                color_t = self.colores.get("torre1", "#A0522D")

            boton.config(bg=color_t, fg="white", text=f"{texto_id}\nHP:{vida_t}", font=("Courier", 9, "bold"))

        elif valor == 4:  # Base
            boton.config(bg=self.colores.get("base", "#5C4033"), text="👑", fg="gold")

        elif valor == 6:  # Unidad
            boton.config(bg="#ff0000", text="Z", fg="black")  # temporal
# defensores

class Muro:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.vida = 250
        self.vida_max = 250
        self.texto = "M"
        self.color = "#8B4513"
    
    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

class Torre2:  # Cactus
    def __init__(self, mapa, ventana, fila, col, actualizar_celda, color_1="#228B22", color_2="#00ff00", vida=150, daño=15, texto="C"):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.color = color_1
        self.vida = vida
        self.vida_max = vida
        self.daño = daño 
        self.texto = texto
        self.alcance = 3
        self.turnos_habilidad = 0

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)
        
class Torre1:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda, color_torre1, color_onda, vida=130, daño=15, texto="T"):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.color = color_torre1
        self.color_onda = color_onda
        self.vida = vida
        self.vida_max = vida
        self.daño = daño
        self.texto = texto
        self.vecinos = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.alcance = 1
        self.turnos_habilidad = 0

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

    def animar(self, juego_combate, ventana):
        # Destello propio de la torre
        boton = juego_combate.botones[self.fila][self.col]
        if boton and boton.winfo_exists():
            boton.config(bg=self.color_onda, fg="black")

            def restaurar():
                if boton.winfo_exists() and juego_combate.mapa[self.fila][self.col] == 1:
                    boton.config(bg=self.color, fg="white", text=f"{self.texto}\nHP:{self.vida}")
            ventana.after(150, restaurar)

        # Onda expansiva: prende las 8 celdas vecinas y las apaga
        for df, dc in self.vecinos:
            nf = self.fila + df
            nc = self.col + dc
            if 0 <= nf < 10 and 0 <= nc < 10:
                celda_vecina = juego_combate.mapa[nf][nc]
                if celda_vecina == 0:  # solo enciende celdas vacías
                    boton_vecino = juego_combate.botones[nf][nc]
                    if boton_vecino and boton_vecino.winfo_exists():
                        boton_vecino.config(bg=self.color_onda)
                        ventana.after(150, lambda b=boton_vecino, f=nf, c=nc:
                            b.config(bg="#1d0800") if b.winfo_exists() and juego_combate.mapa[f][c] == 0 else None)

class Torre3:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda, color_1, vida=75, daño=25, texto="D", color_bala="#ffffff"):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.color = color_1
        self.vida = vida
        self.vida_max = vida
        self.daño = daño
        self.texto = texto
        self.color_bala = color_bala
        self.alcance = 3
        self.turnos_habilidad = 0

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

    def animar(self, juego_combate, ventana, fila_objetivo=None, col_objetivo=None):
        # Destello propio de la torre
        boton = juego_combate.botones[self.fila][self.col]
        if boton and boton.winfo_exists():
            boton.config(bg=self.color_bala, fg="black")

            def restaurar():
                if boton.winfo_exists() and juego_combate.mapa[self.fila][self.col] == 1:
                    boton.config(bg=self.color, fg="white", text=f"{self.texto}\nHP:{self.vida}")
            ventana.after(150, restaurar)

        # Si no nos dieron objetivo, no hay bala que animar
        if fila_objetivo is None or col_objetivo is None:
            return

        # Construimos la trayectoria celda por celda desde la torre hasta el objetivo
        df = fila_objetivo - self.fila
        dc = col_objetivo - self.col
        pasos = max(abs(df), abs(dc))
        if pasos == 0:
            return

        trayectoria = []
        for paso in range(1, pasos + 1):
            f = self.fila + round(df * paso / pasos)
            c = self.col + round(dc * paso / pasos)
            trayectoria.append((f, c))

        def mover_bala(indice):
            if indice >= len(trayectoria):
                return
            f, c = trayectoria[indice]
            if not (0 <= f < 10 and 0 <= c < 10):
                return
            boton_celda = juego_combate.botones[f][c]
            if not boton_celda or not boton_celda.winfo_exists():
                return

            # Solo dibujamos la bala si la celda está vacía (no pisamos torres ni unidades)
            celda_vacia = juego_combate.mapa[f][c] == 0
            texto_anterior = boton_celda.cget("text")
            bg_anterior = boton_celda.cget("bg")

            if celda_vacia:
                boton_celda.config(bg=self.color_bala, fg="black", text="•")

            def limpiar():
                if boton_celda.winfo_exists() and juego_combate.mapa[f][c] == 0:
                    boton_celda.config(bg="#1d0800", text=" ")

            if celda_vacia:
                ventana.after(80, limpiar)

            ventana.after(80, lambda: mover_bala(indice + 1))

        mover_bala(0)
        
# atacantes

class Zombie:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Zombie"
        self.vida = 80
        self.vida_max = 80
        self.daño = 15
        self.velocidad = 1
        self.alcance = 1  # cuerpo a cuerpo
        self.costo = 35
        self.color = "#39ff14"
        self.texto = "Z"
        self.turnos_paralizado = 0
        self.turnos_habilidad = 0  # su habilidad (explotar al morir) es pasiva, sin cooldown

class Corredor:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Corredor"
        self.vida = 150
        self.vida_max = 150
        self.daño = 19
        self.velocidad = 1
        self.alcance = 2  # puede atacar torres a 2 celdas de distancia sin recibir contraataque
        self.costo = 60
        self.color = "#ffff00"
        self.texto = "C"
        self.turnos_paralizado = 0
        self.turnos_sprint = 0
        self.habilidad_especial = "Sprint post-destrucción"
        self.turnos_habilidad = 2
        self.alcance = 2

class Tanque:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Tanque"
        self.vida = 220
        self.vida_max = 220
        self.daño = 35
        self.velocidad = 1
        self.alcance = 1  # cuerpo a cuerpo
        self.costo = 100
        self.color = "#ff6600"
        self.texto = "K"
        self.turnos_paralizado = 0
        self.habilidad_especial = "Regeneración aliados"
        self.turnos_habilidad = 3 
        self.alcance = 1

    def regenerar_aliados(self, unidades):
        # Cura 10 de vida a las unidades aliadas en sus 8 celdas vecinas
        for u in unidades:
            if u is self or u.vida <= 0:
                continue
            dist_fila = abs(u.fila - self.fila)
            dist_col = abs(u.col - self.col)
            if dist_fila <= 1 and dist_col <= 1:
                u.vida += 10
