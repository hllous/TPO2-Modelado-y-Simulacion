"""
Widgets reutilizables para la interfaz
"""

import tkinter as tk


class ToolTip:
    """Muestra un tooltip (pequeña ventana de ayuda) al pasar el mouse"""
    
    def __init__(self, widget, text):
        """
        Parámetros:
        - widget: widget de tkinter al que adjuntar el tooltip
        - text: texto del tooltip
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Muestra el tooltip"""
        try:
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
            
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=self.text, 
                            background="#ffffe0", relief="solid", 
                            borderwidth=1, font=("Arial", 9),
                            padx=5, pady=3)
            label.pack()
        except:
            pass  # Ignorar errores de bbox en widgets que no lo soportan
    
    def hide_tooltip(self, event=None):
        """Oculta el tooltip"""
        if self.tooltip:
            try:
                self.tooltip.destroy()
            except:
                pass  # Tooltip ya destruido
            self.tooltip = None
