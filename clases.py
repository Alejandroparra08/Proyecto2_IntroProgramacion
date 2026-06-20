import tkinter as tk

class VentanaMapa:
    def __init__(self, frame):
        self.ventana = frame
        self.filas = 10
        self.columnas = 10
        self.color_vacio = "#1d0800"
        self.callback_clic = None
        
        self.mapa = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.torres = {}
        self.botones = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        
        self.crear_mapa()
        self.mapa[4][0] = 4
        self.actualizar_celda(4, 0)

    def clic_celda(self, f, c):
        if self.callback_clic:
            self.callback_clic(f, c)

    def crear_mapa(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                boton = tk.Button(
                    self.ventana, width=4, height=2,
                    font=("Arial", 10, "bold"),
                    command=lambda f=f, c=c: self.clic_celda(f, c)
                )
                boton.grid(row=f, column=c, padx=1, pady=1)
                self.botones[f][c] = boton
        self.actualizar_todo()

    def actualizar_todo(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                self.actualizar_celda(f, c)

    def actualizar_celda(self, f, c):
        if not self.botones[f][c] or not self.botones[f][c].winfo_exists():
            return
        valor = self.mapa[f][c]
        if valor == 0:
            self.botones[f][c].config(bg=self.color_vacio, fg="white", text=" ")
        elif valor == 1:
            defensa = self.torres.get((f, c))
            self.botones[f][c].config(
                bg=getattr(defensa, 'color', "#ff2200"),
                fg="white",
                text=getattr(defensa, 'texto', "T")
            )
        elif valor == 4:
            self.botones[f][c].config(bg="#8b0000", fg="white", text="BASE")
        elif valor == 5:
            self.botones[f][c].config(bg="#39ff14", fg="black", text="E")

# defensores

class Muro:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.vida = 500
        self.texto = "M"
        self.color = "#8B4513"
    
    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

class Torre2: # Cactus
    def __init__(self, mapa, ventana, fila, col, actualizar_celda):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.vida = 200
        self.texto = "C"
        self.color = "#228B22"
        self.daño = 10
    
    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

class Torre1:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda, color_torre1, color_onda, vida, daño, texto="T"):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.color = color_torre1
        self.vida = vida
        self.daño = daño
        self.texto = texto

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

class Torre3:
    def __init__(self, mapa, ventana, fila, col, actualizar_celda, color_1, vida, daño, texto="D"):
        self.mapa = mapa
        self.ventana = ventana
        self.fila = fila
        self.col = col
        self.actualizar_celda = actualizar_celda
        self.color = color_1
        self.vida = vida
        self.daño = daño
        self.texto = texto

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

# atacantes

class Zombie:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Zombie"
        self.vida = 80
        self.daño = 15
        self.velocidad = 1
        self.costo = 40
        self.color = "#39ff14"
        self.texto = "Z"

class Corredor:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Corredor"
        self.vida = 40
        self.daño = 10
        self.velocidad = 2
        self.costo = 60
        self.color = "#ffff00"
        self.texto = "C"

class Tanque:
    def __init__(self, mapa, fila, col):
        self.mapa = mapa
        self.fila = fila
        self.col = col
        self.nombre = "Tanque"
        self.vida = 200
        self.daño = 30
        self.velocidad = 1
        self.costo = 100
        self.color = "#ff6600"
        self.texto = "K"
