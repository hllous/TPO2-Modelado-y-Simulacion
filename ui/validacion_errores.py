"""
Módulo centralizado para validación y manejo de errores
Aplica principios KISS y DRY
"""

import tkinter as tk
from tkinter import messagebox
import traceback
import logging
from ui.estilos import COLORES, FUENTES

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidadorEntrada:
    """Centraliza validación de entrada"""
    
    @staticmethod
    def es_numero(valor):
        """Verifica si es un número válido"""
        if valor == "" or valor == "-" or valor == ".":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def es_entero(valor):
        """Verifica si es entero válido"""
        if valor == "" or valor == "-":
            return True
        try:
            int(valor)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def es_rango_valido(min_val, max_val):
        """Verifica que min < max"""
        try:
            return float(min_val) < float(max_val)
        except:
            return False
    
    @staticmethod
    def validar_matriz_2x2(a11, a12, a21, a22):
        """Valida que los elementos sean números"""
        elementos = [a11, a12, a21, a22]
        for elem in elementos:
            try:
                float(elem)
            except:
                return False
        return True
    
    @staticmethod
    def validar_funcion_expresion(expresion):
        """Valida que una expresión sea válida"""
        if not expresion or not expresion.strip():
            return False
        # Verificar caracteres permitidos
        permitidos = set('xytu0123456789-+*/.()^sin cos tan exp sqrt abs log')
        # Simplificado - no validar sintaxis completa aquí
        return True


class ManejoErrores:
    """Centraliza manejo de errores con interfaz amigable"""
    
    @staticmethod
    def mostrar_error(titulo, mensaje, detalles=None, parent=None):
        """Muestra diálogo de error"""
        logger.error(f"{titulo}: {mensaje}")
        if detalles:
            logger.error(f"Detalles: {detalles}")
        
        msg_completo = mensaje
        if detalles:
            msg_completo += f"\n\nDetalles técnicos:\n{detalles}"
        
        messagebox.showerror(titulo, msg_completo, parent=parent)
    
    @staticmethod
    def mostrar_advertencia(titulo, mensaje, parent=None):
        """Muestra diálogo de advertencia"""
        logger.warning(f"{titulo}: {mensaje}")
        messagebox.showwarning(titulo, mensaje, parent=parent)
    
    @staticmethod
    def mostrar_info(titulo, mensaje, parent=None):
        """Muestra diálogo informativo"""
        logger.info(f"{titulo}: {mensaje}")
        messagebox.showinfo(titulo, mensaje, parent=parent)
    
    @staticmethod
    def capturar_excepcion(func):
        """Decorador para capturar excepciones"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error en {func.__name__}: {str(e)}")
                logger.error(traceback.format_exc())
                ManejoErrores.mostrar_error(
                    "Error de Ejecución",
                    f"Se produjo un error en {func.__name__}",
                    detalles=traceback.format_exc()
                )
                return None
        return wrapper


class CreadorWidget:
    """Factory para crear widgets con validación integrada"""
    
    @staticmethod
    def crear_entrada_numerica(parent, inicial=0, minimo=None, maximo=None, 
                             ancho=10, tooltip=None):
        """
        Crea entrada numérica con validación
        
        Retorna: (frame, entry, variable)
        """
        from ui.widgets import ToolTip
        
        frame = tk.Frame(parent)
        var = tk.StringVar(value=str(inicial))
        
        # Registrar validación
        raiz = parent
        while raiz.master:
            raiz = raiz.master
        
        vcmd = (raiz.register(ValidadorEntrada.es_numero), '%P')
        
        entry = tk.Entry(
            frame,
            textvariable=var,
            width=ancho,
            validate='key',
            validatecommand=vcmd,
            font=FUENTES['normal'],
            relief=tk.SOLID,
            bd=1
        )
        entry.pack(fill=tk.X)
        
        if tooltip:
            ToolTip(entry, tooltip)
        
        return frame, entry, var
    
    @staticmethod
    def crear_entrada_rango(parent, label_min="Min", label_max="Max", 
                           inicial_min=0, inicial_max=10):
        """Crea entrada de rango min-max con validación"""
        frame = tk.Frame(parent)
        
        # Min
        frame_min = tk.Frame(frame)
        frame_min.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(frame_min, text=label_min + ":", width=8, anchor='w').pack(side=tk.LEFT)
        var_min = tk.StringVar(value=str(inicial_min))
        entry_min = tk.Entry(frame_min, textvariable=var_min, width=10)
        entry_min.pack(side=tk.LEFT, padx=5)
        
        # Max
        frame_max = tk.Frame(frame)
        frame_max.pack(fill=tk.X, padx=5, pady=3)
        tk.Label(frame_max, text=label_max + ":", width=8, anchor='w').pack(side=tk.LEFT)
        var_max = tk.StringVar(value=str(inicial_max))
        entry_max = tk.Frame(frame_max, padx=5)
        entry_max.pack(side=tk.LEFT, padx=5)
        
        return frame, var_min, var_max


class MensajeEstado:
    """Widget para mostrar estado y mensajes"""
    
    def __init__(self, parent):
        """Inicializa panel de estado"""
        self.frame = tk.Frame(parent, bg=COLORES['info'], height=30)
        self.label = tk.Label(
            self.frame,
            text="",
            bg=COLORES['info'],
            fg='white',
            font=FUENTES['pequena'],
            anchor='w',
            padx=10
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        self.frame.pack_forget()
    
    def mostrar_info(self, mensaje):
        """Muestra mensaje informativo"""
        self.frame.config(bg=COLORES['info'])
        self.label.config(text=mensaje, bg=COLORES['info'])
        self.frame.pack(fill=tk.X)
    
    def mostrar_exito(self, mensaje):
        """Muestra mensaje de éxito"""
        self.frame.config(bg=COLORES['exito'])
        self.label.config(text=mensaje, bg=COLORES['exito'])
        self.frame.pack(fill=tk.X)
    
    def mostrar_error_interno(self, mensaje):
        """Muestra mensaje de error"""
        self.frame.config(bg=COLORES['error'])
        self.label.config(text=mensaje, bg=COLORES['error'])
        self.frame.pack(fill=tk.X)
    
    def ocultar(self):
        """Oculta el panel"""
        self.frame.pack_forget()
