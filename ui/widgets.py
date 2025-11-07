"""
Widgets reutilizables para la interfaz
"""

import tkinter as tk
from ui.estilos import COLORES, FUENTES


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
        self.widget.bind("<Enter>", self.show_tooltip, add=True)
        self.widget.bind("<Leave>", self.hide_tooltip, add=True)
    
    def show_tooltip(self, event=None):
        """Muestra el tooltip"""
        try:
            if self.tooltip is not None:
                return
            
            # Obtener posición del widget
            x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            
            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                self.tooltip, 
                text=self.text, 
                background=COLORES['info'],
                foreground='white',
                relief="solid", 
                borderwidth=1, 
                font=FUENTES['muy_pequena'],
                padx=8, 
                pady=4,
                wraplength=200
            )
            label.pack()
            
            # Asegurar que el tooltip sea visible
            self.tooltip.lift()
            self.tooltip.attributes('-topmost', True)
            
        except Exception as e:
            pass
    
    def hide_tooltip(self, event=None):
        """Oculta el tooltip"""
        if self.tooltip:
            try:
                self.tooltip.destroy()
            except:
                pass
            self.tooltip = None


class EntradaNumerica(tk.Entry):
    """Widget Entry con validación numérica automática"""
    
    def __init__(self, parent, valor_inicial=0, minimo=None, maximo=None, **kwargs):
        """
        Inicializa entrada numérica
        
        Parámetros:
        - parent: widget padre
        - valor_inicial: valor inicial
        - minimo, maximo: límites (opcionales)
        - kwargs: argumentos adicionales
        """
        super().__init__(parent, **kwargs)
        
        self.minimo = minimo
        self.maximo = maximo
        self.var = tk.StringVar(value=str(valor_inicial))
        self.config(textvariable=self.var)
        
        # Registrar validación
        vcmd = self.register(self._validar)
        self.config(validate='key', validatecommand=(vcmd, '%S'))
    
    def _validar(self, char):
        """Valida que solo se ingresen caracteres numéricos"""
        if not char:
            return True
        if char in '0123456789.-':
            return True
        return False


class BotonesGrupo(tk.Frame):
    """Widget para agrupar botones con estilo uniforme"""
    
    def __init__(self, parent, opciones=None, orientacion=tk.HORIZONTAL, **kwargs):
        """
        Inicializa grupo de botones
        
        Parámetros:
        - parent: widget padre
        - opciones: list de dicts {'texto': str, 'comando': callable}
        - orientacion: HORIZONTAL o VERTICAL
        """
        super().__init__(parent, **kwargs)
        
        self.orientacion = orientacion
        self.var = tk.StringVar()
        self.botones = {}
        
        if opciones:
            for opt in opciones:
                self.agregar_boton(opt.get('texto'), opt.get('comando'))
    
    def agregar_boton(self, texto, comando):
        """Agrega botón al grupo"""
        btn = tk.Button(
            self,
            text=texto,
            command=comando,
            bg=COLORES['primario'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=10,
            pady=8,
            font=FUENTES['normal'],
            activebackground=COLORES['primario_hover']
        )
        
        if self.orientacion == tk.HORIZONTAL:
            btn.pack(side=tk.LEFT, padx=2)
        else:
            btn.pack(side=tk.TOP, pady=2, fill=tk.X)
        
        self.botones[texto] = btn
        return btn


class PanelError(tk.Frame):
    """Widget para mostrar mensajes de error"""
    
    def __init__(self, parent, **kwargs):
        """Inicializa panel de error"""
        super().__init__(parent, bg=COLORES['error'], **kwargs)
        
        self.label = tk.Label(
            self,
            text="",
            bg=COLORES['error'],
            fg='white',
            font=FUENTES['pequena'],
            justify=tk.LEFT,
            wraplength=400,
            padx=10,
            pady=10
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.pack_forget()
    
    def mostrar(self, mensaje):
        """Muestra mensaje de error"""
        self.label.config(text=mensaje)
        self.pack(fill=tk.X, padx=5, pady=5)
    
    def ocultar(self):
        """Oculta el panel"""
        self.pack_forget()


class PanelExito(tk.Frame):
    """Widget para mostrar mensajes de éxito"""
    
    def __init__(self, parent, **kwargs):
        """Inicializa panel de éxito"""
        super().__init__(parent, bg=COLORES['exito'], **kwargs)
        
        self.label = tk.Label(
            self,
            text="",
            bg=COLORES['exito'],
            fg='white',
            font=FUENTES['pequena'],
            justify=tk.LEFT,
            wraplength=400,
            padx=10,
            pady=10
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.pack_forget()
    
    def mostrar(self, mensaje):
        """Muestra mensaje de éxito"""
        self.label.config(text=mensaje)
        self.pack(fill=tk.X, padx=5, pady=5)
    
    def ocultar(self):
        """Oculta el panel"""
        self.pack_forget()

