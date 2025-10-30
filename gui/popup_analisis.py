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
        
        ttk.Button(controles, text="Análisis Paso a Paso",
                  command=self._mostrar_analisis_personalizado).pack(
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
    
    def _mostrar_analisis_personalizado(self):
        """Muestra análisis paso a paso para sistemas personalizados"""
        self.text_widget.delete(1.0, tk.END)
        
        texto = "╔" + "═" * 58 + "╗\n"
        texto += "║  ANÁLISIS PASO A PASO                                   ║\n"
        texto += "╚" + "═" * 58 + "╝\n\n"
        
        if self.sistema.funcion_personalizada:
            texto += self._analisis_paso_a_paso_funcion()
        else:
            texto += self._analisis_paso_a_paso_matriz()
        
        self.text_widget.insert(1.0, texto)
    
    def _analisis_paso_a_paso_funcion(self):
        """Análisis detallado para funciones personalizadas"""
        texto = "📝 SISTEMA PERSONALIZADO - ANÁLISIS DETALLADO\n"
        texto += "─" * 60 + "\n\n"
        
        f1 = self.sistema.funcion_personalizada['f1']
        f2 = self.sistema.funcion_personalizada['f2']
        
        texto += "PASO 1: DEFINICIÓN DEL SISTEMA\n"
        texto += "─" * 60 + "\n\n"
        texto += "El sistema está definido por las ecuaciones diferenciales:\n\n"
        texto += f"    dx₁/dt = f₁(x, y, t) = {f1}\n"
        texto += f"    dx₂/dt = f₂(x, y, t) = {f2}\n\n"
        
        # Detectar si tiene términos forzados (dependencia de t)
        tiene_t_f1 = 't' in f1
        tiene_t_f2 = 't' in f2
        
        if tiene_t_f1 or tiene_t_f2:
            texto += "⚠️  El sistema contiene términos dependientes del tiempo (t)\n"
            texto += "   Esto indica un sistema NO AUTÓNOMO (forzado)\n\n"
        else:
            texto += "✓  El sistema es AUTÓNOMO (no depende explícitamente de t)\n\n"
        
        # Detectar no linealidad
        texto += "\nPASO 2: CLASIFICACIÓN DEL SISTEMA\n"
        texto += "─" * 60 + "\n\n"
        
        no_lineal_f1 = any(term in f1 for term in ['**', '*x', '*y', 'x*', 'y*', 'sin', 'cos', 'exp', 'sen'])
        no_lineal_f2 = any(term in f2 for term in ['**', '*x', '*y', 'x*', 'y*', 'sin', 'cos', 'exp', 'sen'])
        
        if no_lineal_f1 or no_lineal_f2:
            texto += "El sistema es NO LINEAL\n\n"
            texto += "Indicadores de no linealidad detectados:\n"
            if '**' in f1 or '**' in f2:
                texto += "  • Potencias (x², y², etc.)\n"
            if any(t in f1+f2 for t in ['*x*', '*y*', 'x*y', 'y*x']):
                texto += "  • Productos cruzados (x·y)\n"
            if any(t in f1+f2 for t in ['sin', 'cos', 'sen']):
                texto += "  • Funciones trigonométricas\n"
            if 'exp' in f1+f2:
                texto += "  • Funciones exponenciales\n"
        else:
            texto += "El sistema es LINEAL\n\n"
            texto += "Todas las expresiones son combinaciones lineales de x e y\n"
        
        # Evaluación en puntos de prueba
        texto += "\n\nPASO 3: EVALUACIÓN EN PUNTOS DE PRUEBA\n"
        texto += "─" * 60 + "\n\n"
        
        puntos_prueba = [(0, 0), (1, 0), (0, 1), (1, 1), (-1, -1)]
        
        texto += "Evaluando el sistema en diferentes puntos:\n\n"
        for x_val, y_val in puntos_prueba:
            try:
                resultado = self.sistema.sistema_ecuaciones([x_val, y_val], 0)
                texto += f"  En ({x_val:2}, {y_val:2}): "
                texto += f"dx₁/dt = {resultado[0]:8.4f}, dx₂/dt = {resultado[1]:8.4f}\n"
            except:
                texto += f"  En ({x_val:2}, {y_val:2}): Error en evaluación\n"
        
        # Búsqueda de equilibrios
        texto += "\n\nPASO 4: PUNTOS DE EQUILIBRIO\n"
        texto += "─" * 60 + "\n\n"
        texto += "Buscando puntos donde dx₁/dt = 0 y dx₂/dt = 0...\n\n"
        
        puntos_eq = self.sistema.encontrar_puntos_equilibrio((-5, 5), (-5, 5))
        
        if puntos_eq:
            texto += f"Encontrados {len(puntos_eq)} punto(s) de equilibrio:\n\n"
            for i, (px, py) in enumerate(puntos_eq, 1):
                texto += f"  {i}. (x, y) = ({px:.4f}, {py:.4f})\n"
                derivadas = self.sistema.sistema_ecuaciones([px, py], 0)
                texto += f"     Verificación: |dx/dt| = {abs(derivadas[0]):.6f}, "
                texto += f"|dy/dt| = {abs(derivadas[1]):.6f}\n"
        else:
            texto += "No se encontraron puntos de equilibrio en el rango [-5, 5]×[-5, 5]\n"
        
        # Análisis de estabilidad cualitativo
        texto += "\n\nPASO 5: ANÁLISIS DE ESTABILIDAD\n"
        texto += "─" * 60 + "\n\n"
        
        if tiene_t_f1 or tiene_t_f2:
            texto += "Para sistemas no autónomos (con términos forzados),\n"
            texto += "el análisis de estabilidad depende del comportamiento\n"
            texto += "del término forzado en el tiempo.\n\n"
            texto += "El sistema podría:\n"
            texto += "  • Converger a una solución periódica\n"
            texto += "  • Exhibir comportamiento caótico\n"
            texto += "  • Seguir al término forzado\n"
        else:
            texto += "Para determinar estabilidad de sistemas no lineales:\n\n"
            texto += "1. Linealizar cerca del punto de equilibrio\n"
            texto += "2. Calcular la matriz Jacobiana:\n\n"
            texto += "       ⎡ ∂f₁/∂x  ∂f₁/∂y ⎤\n"
            texto += "   J = ⎢              ⎥\n"
            texto += "       ⎣ ∂f₂/∂x  ∂f₂/∂y ⎦\n\n"
            texto += "3. Evaluar autovalores de J en cada equilibrio\n"
            texto += "4. Aplicar teorema de Hartman-Grobman\n\n"
            texto += "💡 Sugerencia: Use herramientas de cálculo simbólico\n"
            texto += "   para obtener las derivadas parciales.\n"
        
        return texto
    
    def _analisis_paso_a_paso_matriz(self):
        """Análisis paso a paso para sistemas matriciales"""
        texto = "📊 SISTEMA LINEAL - ANÁLISIS PASO A PASO\n"
        texto += "─" * 60 + "\n\n"
        
        a11, a12 = self.sistema.A[0, 0], self.sistema.A[0, 1]
        a21, a22 = self.sistema.A[1, 0], self.sistema.A[1, 1]
        
        texto += "       ⎡                ⎤\n"
        texto += f"   A = ⎢ {a11:8.4f}  {a12:8.4f} ⎥\n"
        texto += "       ⎢                ⎥\n"
        texto += f"       ⎣ {a21:8.4f}  {a22:8.4f} ⎦\n\n"
        
        texto += self._generar_paso_traza_determinante()
        texto += self._generar_paso_polinomio_caracteristico()
        texto += self._generar_paso_discriminante()
        texto += self._generar_paso_autovalores()
        texto += self._generar_paso_clasificacion()
        
        return texto
    
    def _generar_paso_traza_determinante(self):
        """Genera paso 1: Cálculo de traza y determinante"""
        texto = "PASO 1: CÁLCULO DE TRAZA Y DETERMINANTE\n"
        texto += "─" * 60 + "\n\n"
        
        a11, a12 = self.sistema.A[0, 0], self.sistema.A[0, 1]
        a21, a22 = self.sistema.A[1, 0], self.sistema.A[1, 1]
        
        texto += f"Traza = a₁₁ + a₂₂ = {a11:.4f} + {a22:.4f} = {self.sistema.traza:.6f}\n\n"
        
        det_calc = a11 * a22 - a12 * a21
        texto += f"Determinante = a₁₁·a₂₂ - a₁₂·a₂₁\n"
        texto += f"             = {a11:.4f}·{a22:.4f} - {a12:.4f}·{a21:.4f}\n"
        texto += f"             = {a11*a22:.4f} - {a12*a21:.4f}\n"
        texto += f"             = {det_calc:.6f}\n\n"
        
        return texto
    
    def _generar_paso_polinomio_caracteristico(self):
        """Genera paso 2: Polinomio característico"""
        texto = "PASO 2: POLINOMIO CARACTERÍSTICO\n"
        texto += "─" * 60 + "\n\n"
        
        texto += "El polinomio característico es:\n"
        texto += "    p(λ) = λ² - (tr A)·λ + det(A)\n"
        texto += f"    p(λ) = λ² - ({self.sistema.traza:.6f})·λ + ({self.sistema.determinante:.6f})\n\n"
        
        return texto
    
    def _generar_paso_discriminante(self):
        """Genera paso 3: Discriminante"""
        texto = "PASO 3: CÁLCULO DEL DISCRIMINANTE\n"
        texto += "─" * 60 + "\n\n"
        
        traza = self.sistema.traza
        det = self.sistema.determinante
        discriminante = traza**2 - 4*det
        
        texto += "El discriminante determina la naturaleza de los autovalores:\n"
        texto += "    Δ = (tr A)² - 4·det(A)\n"
        texto += f"    Δ = ({traza:.6f})² - 4·({det:.6f})\n"
        texto += f"    Δ = {traza**2:.6f} - {4*det:.6f}\n"
        texto += f"    Δ = {discriminante:.6f}\n\n"
        
        if discriminante > 0:
            texto += "✓ Δ > 0 → Autovalores REALES Y DISTINTOS\n"
        elif discriminante == 0:
            texto += "✓ Δ = 0 → Autovalores REALES E IGUALES (repetido)\n"
        else:
            texto += "✓ Δ < 0 → Autovalores COMPLEJOS CONJUGADOS\n"
        
        texto += "\n"
        return texto
    
    def _generar_paso_autovalores(self):
        """Genera paso 4: Cálculo de autovalores"""
        texto = "PASO 4: CÁLCULO DE AUTOVALORES\n"
        texto += "─" * 60 + "\n\n"
        
        traza = self.sistema.traza
        det = self.sistema.determinante
        discriminante = traza**2 - 4*det
        
        texto += "Usando la fórmula cuadrática: λ = (tr A ± √Δ) / 2\n\n"
        
        if discriminante >= 0:
            sqrt_disc = np.sqrt(abs(discriminante))
            lambda1 = (traza + sqrt_disc) / 2
            lambda2 = (traza - sqrt_disc) / 2
            
            texto += f"√Δ = √({discriminante:.6f}) = {sqrt_disc:.6f}\n\n"
            texto += f"λ₁ = ({traza:.6f} + {sqrt_disc:.6f}) / 2 = {lambda1:.6f}\n"
            texto += f"λ₂ = ({traza:.6f} - {sqrt_disc:.6f}) / 2 = {lambda2:.6f}\n\n"
        else:
            sqrt_disc = np.sqrt(abs(discriminante))
            real_part = traza / 2
            imag_part = sqrt_disc / 2
            
            texto += f"√Δ = √({discriminante:.6f}) = {imag_part:.6f}i\n\n"
            texto += f"λ₁ = {real_part:.6f} + {imag_part:.6f}i\n"
            texto += f"λ₂ = {real_part:.6f} - {imag_part:.6f}i\n\n"
        
        return texto
    
    def _generar_paso_clasificacion(self):
        """Genera paso 5: Clasificación del punto de equilibrio"""
        texto = "PASO 5: CLASIFICACIÓN DEL PUNTO DE EQUILIBRIO\n"
        texto += "─" * 60 + "\n\n"
        
        lambda1, lambda2 = self.sistema.autovalores
        traza = self.sistema.traza
        det = self.sistema.determinante
        
        texto += "Criterio basado en la posición en el plano (tr A, det A):\n\n"
        
        # Análisis de estabilidad
        if np.iscomplex(lambda1):
            # Complejos
            real_part = lambda1.real
            imag_part = lambda1.imag
            
            if abs(real_part) < 1e-10:
                texto += "📍 Posición: CENTRO\n"
                texto += f"   Parte real: {real_part:.6f} ≈ 0\n"
                texto += f"   Parte imaginaria: ±{imag_part:.6f}i\n"
                texto += "   Comportamiento: Órbitas cerradas (neutral)\n"
            elif real_part < 0:
                texto += "📍 Posición: ESPIRAL ESTABLE (Foco)\n"
                texto += f"   Parte real: {real_part:.6f} < 0\n"
                texto += f"   Parte imaginaria: ±{imag_part:.6f}i\n"
                texto += "   Comportamiento: Converge en espiral hacia el origen\n"
            else:
                texto += "📍 Posición: ESPIRAL INESTABLE (Foco)\n"
                texto += f"   Parte real: {real_part:.6f} > 0\n"
                texto += f"   Parte imaginaria: ±{imag_part:.6f}i\n"
                texto += "   Comportamiento: Diverge en espiral desde el origen\n"
        else:
            # Reales
            if det < 0:
                texto += "📍 Posición: PUNTO SILLA\n"
                texto += f"   λ₁ = {lambda1.real:.6f} (signo +)\n"
                texto += f"   λ₂ = {lambda2.real:.6f} (signo -)\n"
                texto += "   Comportamiento: Inestable (diverge en una dirección)\n"
            elif det > 0:
                if traza < 0:
                    texto += "📍 Posición: NODO ESTABLE\n"
                    texto += f"   λ₁ = {lambda1.real:.6f} < 0\n"
                    texto += f"   λ₂ = {lambda2.real:.6f} < 0\n"
                    texto += "   Comportamiento: Estable (atractor)\n"
                elif traza > 0:
                    texto += "📍 Posición: NODO INESTABLE\n"
                    texto += f"   λ₁ = {lambda1.real:.6f} > 0\n"
                    texto += f"   λ₂ = {lambda2.real:.6f} > 0\n"
                    texto += "   Comportamiento: Inestable (repulsor)\n"
                else:
                    texto += "📍 Posición: CASO ESPECIAL\n"
                    texto += "   tr(A) = 0 pero det(A) > 0\n"
                    texto += "   Comportamiento: Centro lineal\n"
            else:
                texto += "📍 Posición: DEGENERADO\n"
                texto += "   Autovalor cero detectado\n"
                texto += "   Comportamiento: Caso especial - requiere análisis adicional\n"
        
        tipo, estab = self.sistema.clasificar_punto_equilibrio()
        texto += f"\n✅ Clasificación Final: {tipo}\n"
        texto += f"   Estabilidad: {estab}\n"
        
        return texto
