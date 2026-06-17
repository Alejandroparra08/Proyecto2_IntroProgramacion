import tkinter as tk

class VentanaMapa:
    def __init__(self, frame):
        self.ventana = frame
        self.filas = 10
        self.columnas = 10
        self.color_vacio = "#1d0800"
        self.callback_clic = None

        self.mapa = [
            [0 for _ in range(self.columnas)]
            for _ in range(self.filas)
        ]

        self.botones = [
            [None for _ in range(self.columnas)]
            for _ in range(self.filas)
        ]
        self.torre = None
        self.sierra = None
        self.crear_mapa()

    def clic_celda(self, f, c):
        if self.mapa[f][c] == 0 and self.callback_clic:
            self.callback_clic(f, c)

    def crear_mapa(self):
        frame = self.ventana
        for f in range(self.filas):
            for c in range(self.columnas):
                boton = tk.Button(
                    frame,
                    width=6,
                    height=3,
                    font=("Arial", 12, "bold"),
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
        valor = self.mapa[f][c]
        if valor == 0:
            self.botones[f][c].config(
                bg=self.color_vacio,
                fg="white",
                text=" "
            )
        elif valor == 1:
            self.botones[f][c].config(
                bg=self.torre.color_torre,
                fg="white",
                text=self.torre.texto if hasattr(self.torre, 'texto') else 'T'
            )
        elif valor == 2:
            self.botones[f][c].config(
                bg=self.torre.color_onda,
                fg="white",
                text="1"
            )
        elif valor == 3:
            self.botones[f][c].config(
                bg=self.sierra.color_actual,
                fg="black",
                text="*"
            )

class Torre:
    def __init__(self, mapa, ventana, actualizar_celda, fila, col, color_torre, color_onda, vecinos, velocidad, vida, daño, texto = "T"):
        self.mapa = mapa
        self.ventana = ventana
        self.actualizar_celda = actualizar_celda
        self.fila = fila
        self.col = col
        self.color_torre = color_torre
        self.color_onda = color_onda
        self.vecinos = vecinos
        self.velocidad = velocidad
        self.vida = vida
        self.daño = daño
        self.onda_encendida = False
        self.texto = texto

    def colocar(self):
        self.mapa[self.fila][self.col] = 1
        self.actualizar_celda(self.fila, self.col)

    def cambiar_vecinos(self, encender):
        valor_nuevo = 2 if encender else 0
        for df, dc in self.vecinos:
            nf = self.fila + df
            nc = self.col + dc
            if 0 <= nf < len(self.mapa) and 0 <= nc < len(self.mapa[0]):
                if self.mapa[nf][nc] != 1 and self.mapa[nf][nc] != 3:
                    self.mapa[nf][nc] = valor_nuevo
                    self.actualizar_celda(nf, nc)

    def animar(self):
        self.onda_encendida = not self.onda_encendida
        self.cambiar_vecinos(self.onda_encendida)
        self.ventana.after(self.velocidad, self.animar)

class Sierra:
    def __init__(self, mapa, ventana, actualizar_celda, fila, col, color_1, color_2, velocidad, vida, daño):
        self.mapa = mapa
        self.ventana = ventana
        self.actualizar_celda = actualizar_celda
        self.fila = fila
        self.col = col
        self.color_1 = color_1
        self.color_2 = color_2
        self.velocidad = velocidad
        self.color_actual = self.color_1
        self.vida = vida
        self.daño = daño

    def colocar(self):
        self.mapa[self.fila][self.col] = 3
        self.actualizar_celda(self.fila, self.col)

    def animar(self):
        if self.color_actual == self.color_1:
            self.color_actual = self.color_2
        else:
            self.color_actual = self.color_1
        self.actualizar_celda(self.fila, self.col)
        self.ventana.after(self.velocidad, self.animar)

class Disparador:
    def __init__(self, mapa, ventana, actualizar_celda, fila, col, color_disparador, color_disparo, direccion, velocidad, vida, daño):
        self.mapa = mapa
        self.ventana = ventana
        self.actualizar_celda = actualizar_celda
        self.fila = fila
        self.col = col
        self.color_disparador = color_disparador 
        self.color_disparo = color_disparo        
        self.direccion = direccion               
        self.velocidad = velocidad
        self.vida = vida
        self.daño = daño

if __name__ == "__main__":
    ventana = tk.Tk()
    juego = VentanaMapa(ventana)

    juego.torre = Torre(
        mapa=juego.mapa,
        ventana=ventana,
        actualizar_celda=juego.actualizar_celda,
        fila=3,
        col=3,
        color_torre="#ff2200",
        color_onda="#ff7700",
        vecinos=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)],
        velocidad=500,
        vida=120,
        daño=60
    )

    juego.sierra = Sierra(
        mapa=juego.mapa,
        ventana=ventana,
        actualizar_celda=juego.actualizar_celda,
        fila=5,
        col=5,
        color_1="#ffcc00",
        color_2="#ff9900",
        velocidad=200,
        vida=300,
        daño=10
    )

    juego.torre.colocar()
    juego.sierra.colocar()
    juego.torre.animar()
    juego.sierra.animar()

    ventana.mainloop()
