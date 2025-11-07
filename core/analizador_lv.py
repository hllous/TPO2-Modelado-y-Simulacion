"""
Análisis detallado del sistema Lotka-Volterra
Proporciona explicaciones paso a paso
Aplicación de principios KISS y DRY
"""


class AnalizadorLotkaVolterra:
    """Analiza y explica comportamiento del sistema Lotka-Volterra"""
    
    # Títulos y etiquetas reutilizables (DRY)
    TITULOS = {
        'ecuaciones': 'Ecuaciones del Sistema Lotka-Volterra',
        'equilibrios': 'Puntos de Equilibrio',
        'dinamica': 'Dinámica Cíclica del Sistema',
        'ciclo': 'Propiedades del Ciclo Periódico',
        'ecologia': 'Interpretación Ecológica'
    }
    
    def __init__(self, sistema):
        """Inicializa el analizador"""
        self.sistema = sistema
    
    def analizar_completo(self):
        """Realiza análisis completo del sistema"""
        return {
            'ecuaciones': self._explicar_ecuaciones(),
            'equilibrios': self._analizar_equilibrios(),
            'dinamica': self._explicar_dinamica(),
            'oscilaciones': self._analizar_oscilaciones(),
            'interpretacion': self._interpretacion_ecologica()
        }
    
    def _explicar_ecuaciones(self):
        """Explica las ecuaciones del sistema"""
        return {
            'titulo': self.TITULOS['ecuaciones'],
            'ecuaciones': [
                f'dx/dt = {self.sistema.alpha}·x - {self.sistema.beta:.3f}·x·y',
                f'dy/dt = {self.sistema.gamma:.3f}·x·y - {self.sistema.delta}·y'
            ],
            'terminos': {
                'presas_crecimiento': f'α·x = {self.sistema.alpha}·x (crecimiento exponencial)',
                'presas_depredacion': f'β·x·y = {self.sistema.beta:.3f}·x·y (depredación)',
                'depredadores_alimentacion': f'γ·x·y = {self.sistema.gamma:.3f}·x·y (ganancia por alimentación)',
                'depredadores_muerte': f'δ·y = {self.sistema.delta}·y (muerte natural)'
            }
        }
    
    def _analizar_equilibrios(self):
        """Analiza puntos de equilibrio"""
        eq_interior = self.sistema.equilibrio_interior
        
        return {
            'titulo': self.TITULOS['equilibrios'],
            'equilibrio_trivial': {
                'punto': (0, 0),
                'descripcion': 'Extinción total (ambas especies desaparecen)',
                'tipo': 'Nodo silla (inestable)',
                'significado': 'No es realista ecológicamente'
            },
            'equilibrio_interior': {
                'punto': eq_interior,
                'presas': f'{eq_interior[0]:.3f} = δ/γ = {self.sistema.delta}/{self.sistema.gamma}',
                'depredadores': f'{eq_interior[1]:.3f} = α/β = {self.sistema.alpha}/{self.sistema.beta:.3f}',
                'tipo': 'Centro (neutralmente estable)',
                'significado': 'Alrededor de este punto oscilan las poblaciones',
                'caracteristica': 'Órbitas periódicas cerradas'
            }
        }
    
    def _explicar_dinamica(self):
        """Explica la dinámica del sistema paso a paso"""
        return {
            'titulo': self.TITULOS['dinamica'],
            'etapas': [
                {
                    'fase': 1,
                    'nombre': 'Aumento de Presas',
                    'descripcion': 'Cuando hay pocas presas, la depredación es baja',
                    'ecuacion': 'dx/dt ≈ α·x > 0 (crece sin freno)',
                    'duracion': 'Presas crecen exponencialmente',
                    'comportamiento': f'Depredadores: {self.sistema.delta} individuos'
                },
                {
                    'fase': 2,
                    'nombre': 'Saturación de Presas',
                    'descripcion': 'Mayor población de presas = más depredación',
                    'ecuacion': 'dx/dt = α·x - β·x·y se hace negativo',
                    'duracion': 'Depredadores abundan, consumen más',
                    'comportamiento': 'Presas empiezan a disminuir'
                },
                {
                    'fase': 3,
                    'nombre': 'Aumento de Depredadores',
                    'descripcion': 'Muchas presas = bien alimentados los depredadores',
                    'ecuacion': 'dy/dt = γ·x·y - δ·y > 0 (crece)',
                    'duracion': 'Población de depredadores crece',
                    'comportamiento': 'Depredación se intensifica'
                },
                {
                    'fase': 4,
                    'nombre': 'Caída de Presas',
                    'descripcion': 'Depredadores comen demasiadas presas',
                    'ecuacion': 'dx/dt muy negativo',
                    'duracion': 'Presas colapsan',
                    'comportamiento': 'Depredadores sin alimento'
                },
                {
                    'fase': 5,
                    'nombre': 'Muerte de Depredadores',
                    'descripcion': 'Sin comida, los depredadores mueren',
                    'ecuacion': 'dy/dt = -δ·y < 0 (decrece)',
                    'duracion': 'Población de depredadores cae',
                    'comportamiento': 'Presión de depredación disminuye'
                },
                {
                    'fase': 6,
                    'nombre': 'Recuperación de Presas',
                    'descripcion': 'Pocas depredadores = pocas presas consumidas',
                    'ecuacion': 'dx/dt ≈ α·x > 0',
                    'duracion': 'Presas repuntan',
                    'comportamiento': 'Vuelve al inicio del ciclo'
                }
            ]
        }
    
    def _analizar_oscilaciones(self):
        """Analiza propiedades de las oscilaciones"""
        ciclo = self.sistema.calcular_ciclo_periodico()
        
        return {
            'titulo': self.TITULOS['ciclo'],
            'periodo_aproximado': f'{ciclo["periodo_aproximado"]:.2f} unidades de tiempo',
            'formula': f'T ≈ 2π/√(α·δ) = 2π/√({self.sistema.alpha}·{self.sistema.delta})',
            'amplitudes': {
                'presas': f'Oscilan alrededor de {ciclo["presas_equilibrio"]:.3f}',
                'depredadores': f'Oscilan alrededor de {ciclo["depredadores_equilibrio"]:.3f}'
            },
            'observacion': 'Los máximos de depredadores ocurren DESPUÉS de los máximos de presas',
            'desfase': 'Típico de sistemas presa-depredador'
        }
    
    def _interpretacion_ecologica(self):
        """Proporciona interpretación ecológica"""
        ciclo = self.sistema.calcular_ciclo_periodico()
        
        return {
            'titulo': self.TITULOS['ecologia'],
            'conservacion': {
                'propiedad': 'Conservación de cantidad de movimiento en el plano fase',
                'implicacion': 'Las órbitas son exactamente periódicas (no hay decaimiento)',
                'significado': 'Sistema sin fricción - idealización matemática'
            },
            'implicaciones_biologicas': [
                f'1. Las poblaciones NUNCA alcanzan un punto fijo estable',
                f'2. Siempre oscilan en ciclos de duración {ciclo["periodo_aproximado"]:.1f} aprox.',
                f'3. Máximo de depredadores va retrasado respecto máximo de presas',
                f'4. Razón de equilibrio: presas/depredadores ≈ {ciclo["presas_equilibrio"]/ciclo["depredadores_equilibrio"]:.2f}'
            ],
            'perturbaciones': [
                'Si aumenta α: más competencia entre presas, más depredadores en equilibrio',
                'Si aumenta β: más eficiente la depredación, menos presas en equilibrio',
                'Si aumenta γ: depredadores mejor alimentados, más depredadores en equilibrio',
                'Si aumenta δ: depredadores mueren más, menos depredadores en equilibrio'
            ]
        }
