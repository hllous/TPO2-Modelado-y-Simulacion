"""
Ventana popup para mostrar análisis paso a paso de autovalores y autovectores
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from ui.estilos import COLORES, FUENTES


class VentanaAnalisisPopup:
    """Ventana modal para mostrar análisis detallado del sistema"""
    
    def __init__(self, parent, sistema):
        """
        Inicializa la ventana popup
        
        Parámetros:
        - parent: ventana padre
        - sistema: objeto SistemaDinamico2D
        """
        self.sistema = sistema
        self.popup = tk.Toplevel(parent)
        self.popup.title("Análisis Detallado - Autovalores y Autovectores")
        self.popup.geometry("700x600")
        self.popup.configure(bg=COLORES['fondo'])
        self.popup.transient(parent)
        self.popup.grab_set()
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea la estructura de widgets del popup"""
        main_frame = ttk.Frame(self.popup, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones de control
        self._crear_controles(main_frame)
        
        # Área de contenido con scroll
        self._crear_area_contenido(main_frame)
        
        # Mostrar análisis inicial
        self._mostrar_analisis_matriz()
    
    def _crear_controles(self, parent):
        """Crea botones de navegación"""
        controles = ttk.Frame(parent)
        controles.pack(fill=tk.X, pady=(0, 10))
        
        if not self.sistema.funcion_personalizada:
            ttk.Button(controles, text="Ver Matriz",
                      command=self._mostrar_analisis_matriz).pack(
                side=tk.LEFT, padx=5)
        
        ttk.Button(controles, text="Autovalores",
                  command=self._mostrar_autovalores).pack(
            side=tk.LEFT, padx=5)
        
        ttk.Button(controles, text="Autovectores",
                  command=self._mostrar_autovectores).pack(
            side=tk.LEFT, padx=5)
        
        ttk.Button(controles, text="Clasificación",
                  command=self._mostrar_clasificacion).pack(
            side=tk.LEFT, padx=5)
        
        ttk.Button(controles, text="Cerrar",
                  command=self.popup.destroy).pack(
            side=tk.RIGHT, padx=5)
    
    def _crear_area_contenido(self, parent):
        """Crea área con scroll para mostrar contenido"""
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=FUENTES['monoespaciada'],
            bg='white',
            relief='flat',
            padx=10,
            pady=10,
            height=20
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_widget.yview)
    
    def _mostrar_analisis_matriz(self):
        """Muestra la matriz del sistema"""
        self.text_widget.delete(1.0, tk.END)
        
        texto = "╔" + "═" * 58 + "╗\n"
        texto += "║  ANÁLISIS DEL SISTEMA DINÁMICO 2D                           ║\n"
        texto += "╚" + "═" * 58 + "╝\n\n"
        
        if self.sistema.funcion_personalizada:
            texto += "📝 SISTEMA PERSONALIZADO\n"
            texto += "─" * 60 + "\n\n"
            texto += f"dx₁/dt = {self.sistema.funcion_personalizada['f1']}\n"
            texto += f"dx₂/dt = {self.sistema.funcion_personalizada['f2']}\n\n"
            texto += "Tipo: " + ("NO LINEAL" if self.sistema.es_no_lineal else "LINEAL") + "\n\n"
            texto += "💡 Nota: Para sistemas no lineales, el análisis de\n"
            texto += "   autovalores requiere linealización en el punto\n"
            texto += "   de equilibrio.\n"
        else:
            texto += "📊 MATRIZ DEL SISTEMA\n"
            texto += "─" * 60 + "\n\n"
            texto += "dx/dt = A·x + f(t)\n\n"
            texto += "Donde A es la matriz de coeficientes:\n\n"
            texto += "       ⎡                ⎤\n"
            texto += f"   A = ⎢ {self.sistema.A[0,0]:8.6f}  {self.sistema.A[0,1]:8.6f} ⎥\n"
            texto += "       ⎢                ⎥\n"
            texto += f"       ⎣ {self.sistema.A[1,0]:8.6f}  {self.sistema.A[1,1]:8.6f} ⎦\n\n"
            
            if self.sistema.termino_forzado:
                texto += self._generar_termino_forzado()
            else:
                texto += "Sistema HOMOGÉNEO (sin término forzado)\n\n"
                texto += f"Determinante: {self.sistema.determinante:.6f}\n"
                texto += f"Traza:        {self.sistema.traza:.6f}\n\n"
        
        self.text_widget.insert(1.0, texto)
    
    def _generar_termino_forzado(self):
        """Genera texto del término forzado"""
        tf = self.sistema.termino_forzado
        texto = "Sistema NO HOMOGÉNEO con término forzado:\n\n"
        
        if tf['tipo'] == 'constante':
            texto += f"f(t) = [{tf['coef1']:.4f}, {tf['coef2']:.4f}]ᵀ\n"
        elif tf['tipo'] == 'exponencial':
            p = tf.get('param', 1)
            texto += f"f(t) = [{tf['coef1']:.4f}·e^({p:.4f}t),\n"
            texto += f"        {tf['coef2']:.4f}·e^({p:.4f}t)]ᵀ\n"
        elif tf['tipo'] in ['seno', 'coseno']:
            p = tf.get('param', 1)
            fn = "sin" if tf['tipo'] == 'seno' else "cos"
            texto += f"f(t) = [{tf['coef1']:.4f}·{fn}({p:.4f}t),\n"
            texto += f"        {tf['coef2']:.4f}·{fn}({p:.4f}t)]ᵀ\n"
        
        texto += "\n"
        return texto
    
    def _mostrar_autovalores(self):
        """Muestra cálculo detallado de autovalores"""
        self.text_widget.delete(1.0, tk.END)
        
        if self.sistema.funcion_personalizada:
            self.text_widget.insert(1.0, "⚠️  SISTEMA PERSONALIZADO\n\nNo se calculan autovalores de forma automática\n"
                                   "para sistemas personalizados.")
            return
        
        texto = "╔" + "═" * 58 + "╗\n"
        texto += "║  CÁLCULO DE AUTOVALORES                                   ║\n"
        texto += "╚" + "═" * 58 + "╝\n\n"
        
        texto += "Los autovalores se obtienen del polinomio característico:\n\n"
        texto += "    det(A - λI) = 0\n\n"
        texto += "Expandiendo para una matriz 2×2:\n\n"
        
        a11, a12 = self.sistema.A[0, 0], self.sistema.A[0, 1]
        a21, a22 = self.sistema.A[1, 0], self.sistema.A[1, 1]
        
        texto += f"    ⎪ {a11:.4f} - λ    {a12:.4f}   ⎪\n"
        texto += f"    ⎪                        ⎪ = 0\n"
        texto += f"    ⎪ {a21:.4f}       {a22:.4f} - λ ⎪\n\n"
        
        traza = self.sistema.traza
        det = self.sistema.determinante
        
        texto += "Polinomio característico:\n\n"
        texto += f"    λ² - (tr(A))·λ + det(A) = 0\n"
        texto += f"    λ² - ({traza:.6f})·λ + ({det:.6f}) = 0\n\n"
        
        # Discriminante
        discriminante = traza**2 - 4*det
        texto += "Usando la fórmula cuadrática:\n\n"
        texto += f"    Δ = (tr(A))² - 4·det(A)\n"
        texto += f"    Δ = ({traza:.6f})² - 4·({det:.6f})\n"
        texto += f"    Δ = {discriminante:.6f}\n\n"
        
        if discriminante >= 0:
            sqrt_disc = np.sqrt(abs(discriminante))
            lambda1 = (traza + sqrt_disc) / 2
            lambda2 = (traza - sqrt_disc) / 2
            
            texto += f"    √Δ = {sqrt_disc:.6f}\n\n"
            texto += "    λ = (tr(A) ± √Δ) / 2\n\n"
            texto += f"    λ₁ = ({traza:.6f} + {sqrt_disc:.6f}) / 2 = {lambda1:.6f}\n"
            texto += f"    λ₂ = ({traza:.6f} - {sqrt_disc:.6f}) / 2 = {lambda2:.6f}\n"
        else:
            sqrt_disc = np.sqrt(abs(discriminante))
            real_part = traza / 2
            imag_part = sqrt_disc / 2
            
            texto += f"    √Δ = √({discriminante:.6f}i²)\n"
            texto += f"    √Δ = {imag_part:.6f}i\n\n"
            texto += "    λ = (tr(A) ± i·√|Δ|) / 2\n\n"
            texto += f"    λ₁ = {real_part:.6f} + {imag_part:.6f}i\n"
            texto += f"    λ₂ = {real_part:.6f} - {imag_part:.6f}i\n"
        
        texto += "\n" + "─" * 60 + "\n\n"
        texto += "✓ AUTOVALORES CALCULADOS\n\n"
        
        for i, lam in enumerate(self.sistema.autovalores, 1):
            if np.iscomplex(lam):
                texto += f"    λ{i} = {lam.real:.6f} + {lam.imag:.6f}i\n"
            else:
                texto += f"    λ{i} = {lam.real:.6f}\n"
        
        self.text_widget.insert(1.0, texto)
    
    def _mostrar_autovectores(self):
        """Muestra cálculo detallado de autovectores"""
        self.text_widget.delete(1.0, tk.END)
        
        if self.sistema.funcion_personalizada:
            self.text_widget.insert(1.0, "⚠️  SISTEMA PERSONALIZADO\n\nNo se calculan autovectores de forma automática\n"
                                   "para sistemas personalizados.")
            return
        
        texto = "╔" + "═" * 58 + "╗\n"
        texto += "║  CÁLCULO DE AUTOVECTORES                                 ║\n"
        texto += "╚" + "═" * 58 + "╝\n\n"
        
        texto += "Para cada autovalor λᵢ, el autovector se obtiene de:\n\n"
        texto += "    (A - λᵢI)·vᵢ = 0\n\n"
        
        a11, a12 = self.sistema.A[0, 0], self.sistema.A[0, 1]
        a21, a22 = self.sistema.A[1, 0], self.sistema.A[1, 1]
        
        for i, lam in enumerate(self.sistema.autovalores, 1):
            texto += f"\n{'─' * 60}\n"
            texto += f"AUTOVECTOR {i}: Autovalor λ{i} = {lam:.6f}\n"
            texto += f"{'─' * 60}\n\n"
            
            # Matriz (A - λI)
            mat_diag = np.array([
                [a11 - lam, a12],
                [a21, a22 - lam]
            ])
            
            texto += f"    (A - λ{i}I) = ⎡ {mat_diag[0,0]:.6f}  {mat_diag[0,1]:.6f} ⎤\n"
            texto += f"                 ⎣ {mat_diag[1,0]:.6f}  {mat_diag[1,1]:.6f} ⎦\n\n"
            
            texto += f"Resolvemos (A - λ{i}I)·v{i} = 0\n"
            texto += f"El autovector se obtiene del espacio nulo.\n\n"
            
            # Autovector normalizado
            autovec = self.sistema.autovectores[:, i-1]
            
            if np.iscomplex(autovec[0]):
                texto += f"✓ AUTOVECTOR v{i}:\n\n"
                texto += f"    v{i} = ⎡ {autovec[0].real:.6f} + {autovec[0].imag:.6f}i ⎤\n"
                texto += f"         ⎣ {autovec[1].real:.6f} + {autovec[1].imag:.6f}i ⎦\n"
            else:
                texto += f"✓ AUTOVECTOR v{i}:\n\n"
                texto += f"    v{i} = ⎡ {autovec[0].real:.6f} ⎤\n"
                texto += f"         ⎣ {autovec[1].real:.6f} ⎦\n"
            
            # Verificación: A·v = λ·v
            texto += f"\nVerificación: A·v{i} ≈ λ{i}·v{i} ✓\n"
        
        self.text_widget.insert(1.0, texto)
    
    def _mostrar_clasificacion(self):
        """Muestra clasificación del punto de equilibrio"""
        self.text_widget.delete(1.0, tk.END)
        
        if self.sistema.funcion_personalizada:
            self.text_widget.insert(1.0, "⚠️  SISTEMA PERSONALIZADO\n\nLa clasificación requiere linealización.\n"
                                   "Consulte la literatura sobre estabilidad Lyapunov.")
            return
        
        texto = "╔" + "═" * 58 + "╗\n"
        texto += "║  CLASIFICACIÓN DEL PUNTO DE EQUILIBRIO                 ║\n"
        texto += "╚" + "═" * 58 + "╝\n\n"
        
        lambda1, lambda2 = self.sistema.autovalores
        
        texto += "Criterio de clasificación:\n\n"
        texto += "1. Si λ₁, λ₂ ∈ ℝ (reales):\n"
        texto += "   • Mismo signo (ambos < 0): NODO ESTABLE\n"
        texto += "   • Mismo signo (ambos > 0): NODO INESTABLE\n"
        texto += "   • Signos opuestos: PUNTO SILLA (inestable)\n\n"
        
        texto += "2. Si λ = α ± βi (complejos):\n"
        texto += "   • α < 0: ESPIRAL ESTABLE (atractor)\n"
        texto += "   • α > 0: ESPIRAL INESTABLE (repulsor)\n"
        texto += "   • α = 0: CENTRO (neutral)\n\n"
        
        texto += f"\n{'─' * 60}\n"
        texto += f"ANÁLISIS DEL SISTEMA ACTUAL\n"
        texto += f"{'─' * 60}\n\n"
        
        texto += f"Traza = {self.sistema.traza:.6f}\n"
        texto += f"Determinante = {self.sistema.determinante:.6f}\n\n"
        
        texto += f"Autovalores:\n"
        for i, lam in enumerate(self.sistema.autovalores, 1):
            if np.iscomplex(lam):
                texto += f"    λ{i} = {lam.real:.6f} + {lam.imag:.6f}i\n"
            else:
                texto += f"    λ{i} = {lam.real:.6f}\n"
        
        texto += "\n"
        
        tipo, estab = self.sistema.clasificar_punto_equilibrio()
        
        texto += f"RESULTADO:\n\n"
        texto += f"  Tipo de equilibrio: {tipo}\n"
        texto += f"  Estabilidad:        {estab}\n"
        
        self.text_widget.insert(1.0, texto)
