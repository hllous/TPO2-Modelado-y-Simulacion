"""
Archivo principal para ejecutar la aplicación de Sistemas Dinámicos 2D
Punto de entrada único de la aplicación
"""

import tkinter as tk
from gui.interfaz import InterfazGrafica


def main():
    """
    Función principal que inicia la aplicación
    """
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()


if __name__ == "__main__":
    main()
