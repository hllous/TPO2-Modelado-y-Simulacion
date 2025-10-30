"""
Archivo principal para ejecutar la aplicación de Sistemas Dinámicos
Punto de entrada único de la aplicación
"""

import tkinter as tk
from gui.main_interface import InterfazPrincipal


def main():
    """
    Función principal que inicia la aplicación
    """
    root = tk.Tk()
    app = InterfazPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
