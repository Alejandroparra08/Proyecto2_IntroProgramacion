# Proyecto II: Juego Attack Us

## Información del curso
- **Profesor:** Diego Mora / Jeff Schmidt
- **Curso:** IC-1802 Introducción a la Programación
- **Periodo:** I Semestre 2026
- **Entrega:** 21 de Junio

## Integrantes
- Alejandro Parra (2026000494)
- Mathew Arguedas (2026093667)

## Descripción
ATTACK US es un juego por turnos para dos jugadores, le implementamos al juego una temática de apocalipsis zombie. 
Un jugador defiende una base colocando torres y muros, mientras el otro la ataca colocando unidades. 

Las torres y los atacantes cuentan con 3 tipos cada una, y cada una cuenta con algun tipo de habilidad que la distingue de las demás.

Cada unidad, ya sea torre o atacante, debe de ser comprada inteligentemente utilizando el dinero que cada jugador tenga.
El primero en ganar 3 rondas gana la partida.

## Requisitos
- Python 3
- Tkinter (incluido en Python)
## Estructura del proyecto
ATTACK_US

├── main.py : Este documento es el principal, contiene la mayor cantidad del codigo para el juego, en este archivo se establecen distintas funciones que permiten la funcionalidad del programa.

├── clases.py : Este py contiene unicamente las clases necesitadas para la creación de torres, atacantes, e incluso la creación del mapa 10x10 donde se juega.

├── jugadores.json : Este archivo almacena en texto cada usuario junto con su contraseña que se registran. Esto ayuda a que con el codigo se tome el texto almacenado, y asi validar que el usuario y contraseña existen, y que si existen sean las correctas.

├── fondo_login.png : Esta es la imagen que se utilizó para poner de fondo a la hora de ingresar al juego y dar una mejor experiencia visual.

## Cómo ejecutar el juego
1. Asegurate de tener todos los archivos en la misma carpeta para que todo funcione.
2. Abrí `main.py` con IDLE de Python.
3. Presioná **F5** para ejecutar.

## Flujo del Juego
1. 1.) Abrir el juego.
2. 2.) Si no tienes un usuario, click al boton de registrarse.
3. 3.) Si ya cuentas con un usuario, click al boton de inciar sesión.
4. 4.) Una vez cuentes con un usuario registrado, inicia sesión con tu usuario y contraseña.
5. 5.) Una vez ingresado el jugador 1, da click en nueva partida.
6. 6.) Al clickear en nueva partida, se solicitara el usuario y la contraseña del usuario que será el jugador 2.
7. 7.) Una vez ambos hayan ingresado, se pedirá que ambos seleccionen una temática, no puede ser la misma para ambos.
8. 8.) Después de escoger temática, empezara la ronda de colocación de muros y torres para el defensor.
9.) Cuando el defensor esté listo, la ronda de colocación para el atacante incia.
10. 10.) Una vez ambos hayan colocado sus unidades, empezara la simulación, basado en las reglas solicitadas. Cuando alguno de los 2 jugadores, ya sea atacante o defensor, gana un total de 3 rondas, es el claro vencedor y acaba el juego.

## Repositorio
[Repositorio en Github](https://github.com/Alejandroparra08/Proyecto2_IntroProgramacion)
