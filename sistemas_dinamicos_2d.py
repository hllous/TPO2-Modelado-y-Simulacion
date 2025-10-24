"""
Sistema Dinámico 2D Homogéneo
Análisis de sistemas de ecuaciones diferenciales dx/dt = Ax
donde A es una matriz 2x2
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

class SistemaDinamico2D:
    def __init__(self, matriz):
        """
        Inicializa el sistema dinámico con una matriz 2x2
        
        Parámetros:
        matriz: array 2x2 que representa el sistema dx/dt = Ax
        """
        self.A = np.array(matriz, dtype=float)
        self.autovalores, self.autovectores = np.linalg.eig(self.A)
        self.determinante = np.linalg.det(self.A)
        self.traza = np.trace(self.A)
        
    def clasificar_punto_equilibrio(self):
        """
        Clasifica el tipo de punto de equilibrio según los autovalores
        
        Retorna:
        tipo: string con la clasificación
        estabilidad: string indicando si es estable, inestable o centro
        """
        lambda1, lambda2 = self.autovalores
        
        # Verificar si son complejos
        if np.iscomplex(lambda1) or np.iscomplex(lambda2):
            parte_real = lambda1.real
            if abs(parte_real) < 1e-10:
                return "Centro", "Neutral (órbitas cerradas)"
            elif parte_real < 0:
                return "Espiral (Foco)", "Estable (atractor)"
            else:
                return "Espiral (Foco)", "Inestable (repulsor)"
        
        # Autovalores reales
        else:
            # Verificar si alguno es cero
            if abs(lambda1) < 1e-10 or abs(lambda2) < 1e-10:
                return "Degenerado (autovalor cero)", "Caso especial"
            
            # Ambos autovalores del mismo signo
            if lambda1 * lambda2 > 0:
                if abs(lambda1 - lambda2) < 1e-10:
                    return "Nodo Estrella (autovalores iguales)", "Estable" if lambda1 < 0 else "Inestable"
                else:
                    tipo = "Nodo Propio"
                    estabilidad = "Estable (atractor)" if lambda1 < 0 else "Inestable (repulsor)"
                    return tipo, estabilidad
            
            # Autovalores de signos opuestos
            else:
                return "Punto Silla (Silla de montar)", "Inestable (hiperbólico)"
    
    def sistema_ecuaciones(self, X, t):
        """
        Define el sistema de ecuaciones diferenciales
        dx/dt = Ax
        """
        return np.dot(self.A, X)
    
    def graficar_sistema(self, xlim=(-5, 5), ylim=(-5, 5), n_puntos=20):
        """
        Grafica el campo de direcciones y algunas trayectorias del sistema
        
        Parámetros:
        xlim: límites en x
        ylim: límites en y
        n_puntos: número de puntos para el campo de direcciones
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Crear malla para el campo de direcciones
        x = np.linspace(xlim[0], xlim[1], n_puntos)
        y = np.linspace(ylim[0], ylim[1], n_puntos)
        X, Y = np.meshgrid(x, y)
        
        # Calcular derivadas en cada punto
        U = self.A[0, 0] * X + self.A[0, 1] * Y
        V = self.A[1, 0] * X + self.A[1, 1] * Y
        
        # Normalizar para mejor visualización
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1  # Evitar división por cero
        U_norm = U / M
        V_norm = V / M
        
        # Graficar campo de direcciones
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', alpha=0.6)
        
        # Tiempo para las trayectorias
        t = np.linspace(0, 10, 1000)
        
        # Graficar trayectorias desde diferentes puntos iniciales
        condiciones_iniciales = [
            [4, 0], [-4, 0], [0, 4], [0, -4],
            [3, 3], [-3, 3], [3, -3], [-3, -3],
            [2, 1], [-2, 1], [2, -1], [-2, -1]
        ]
        
        for ic in condiciones_iniciales:
            try:
                solucion = odeint(self.sistema_ecuaciones, ic, t)
                ax.plot(solucion[:, 0], solucion[:, 1], 'b-', linewidth=1.5, alpha=0.7)
                ax.plot(ic[0], ic[1], 'ro', markersize=5)
            except:
                pass
        
        # Graficar autovectores si son reales
        if not np.iscomplex(self.autovalores[0]):
            for i in range(2):
                v = self.autovectores[:, i].real
                if abs(self.autovalores[i]) > 1e-10:
                    scale = 4
                    ax.arrow(0, 0, scale * v[0], scale * v[1], 
                            head_width=0.3, head_length=0.2, 
                            fc='red', ec='red', linewidth=2, alpha=0.8)
                    ax.arrow(0, 0, -scale * v[0], -scale * v[1], 
                            head_width=0.3, head_length=0.2, 
                            fc='red', ec='red', linewidth=2, alpha=0.8)
        
        # Punto de equilibrio en el origen
        ax.plot(0, 0, 'ko', markersize=10, label='Punto de equilibrio')
        
        # Configuración de la gráfica
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel('x₁', fontsize=12)
        ax.set_ylabel('x₂', fontsize=12)
        
        # Título con información del sistema
        tipo, estabilidad = self.clasificar_punto_equilibrio()
        titulo = f'Sistema Dinámico 2D: {tipo}\n{estabilidad}'
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        
        ax.legend()
        plt.tight_layout()
        plt.show()
    
    def mostrar_analisis(self):
        """
        Muestra un análisis completo del sistema
        """
        print("=" * 60)
        print("ANÁLISIS DEL SISTEMA DINÁMICO 2D HOMOGÉNEO")
        print("=" * 60)
        print(f"\nMatriz del sistema A:")
        print(self.A)
        print(f"\n{'─' * 60}")
        
        print(f"\nDeterminante: {self.determinante:.6f}")
        print(f"Traza: {self.traza:.6f}")
        
        print(f"\n{'─' * 60}")
        print("\nAutovalores:")
        for i, autoval in enumerate(self.autovalores, 1):
            if np.iscomplex(autoval):
                print(f"  λ{i} = {autoval.real:.6f} + {autoval.imag:.6f}i")
            else:
                print(f"  λ{i} = {autoval.real:.6f}")
        
        print(f"\n{'─' * 60}")
        print("\nAutovectores:")
        for i in range(2):
            autovec = self.autovectores[:, i]
            if np.iscomplex(autovec[0]):
                print(f"  v{i+1} = [{autovec[0].real:.6f} + {autovec[0].imag:.6f}i, "
                      f"{autovec[1].real:.6f} + {autovec[1].imag:.6f}i]ᵀ")
            else:
                print(f"  v{i+1} = [{autovec[0].real:.6f}, {autovec[1].real:.6f}]ᵀ")
        
        print(f"\n{'─' * 60}")
        tipo, estabilidad = self.clasificar_punto_equilibrio()
        print(f"\nCLASIFICACIÓN DEL PUNTO DE EQUILIBRIO:")
        print(f"  Tipo: {tipo}")
        print(f"  Estabilidad: {estabilidad}")
        
        print("\n" + "=" * 60)


def ingresar_matriz():
    """
    Permite al usuario ingresar una matriz 2x2
    """
    print("\n" + "=" * 60)
    print("INGRESO DE MATRIZ DEL SISTEMA")
    print("=" * 60)
    print("\nIngrese los elementos de la matriz A (2x2):")
    print("El sistema será: dx/dt = Ax")
    print()
    
    while True:
        try:
            print("Fila 1:")
            a11 = float(input("  a₁₁ = "))
            a12 = float(input("  a₁₂ = "))
            print("Fila 2:")
            a21 = float(input("  a₂₁ = "))
            a22 = float(input("  a₂₂ = "))
            
            matriz = [[a11, a12], [a21, a22]]
            return matriz
        except ValueError:
            print("\n❌ Error: Por favor ingrese valores numéricos válidos.\n")


def ejemplos_predefinidos():
    """
    Muestra algunos ejemplos predefinidos de sistemas dinámicos
    """
    ejemplos = {
        '1': {
            'nombre': 'Nodo Estable',
            'matriz': [[-1, 0], [0, -2]]
        },
        '2': {
            'nombre': 'Nodo Inestable',
            'matriz': [[1, 0], [0, 2]]
        },
        '3': {
            'nombre': 'Punto Silla',
            'matriz': [[1, 0], [0, -1]]
        },
        '4': {
            'nombre': 'Espiral Estable',
            'matriz': [[-0.5, 1], [-1, -0.5]]
        },
        '5': {
            'nombre': 'Espiral Inestable',
            'matriz': [[0.5, 1], [-1, 0.5]]
        },
        '6': {
            'nombre': 'Centro',
            'matriz': [[0, 1], [-1, 0]]
        },
        '7': {
            'nombre': 'Nodo Degenerado',
            'matriz': [[-1, 1], [0, -1]]
        }
    }
    
    print("\n" + "=" * 60)
    print("EJEMPLOS PREDEFINIDOS")
    print("=" * 60)
    for key, value in ejemplos.items():
        print(f"{key}. {value['nombre']}")
    print("0. Ingresar matriz personalizada")
    print("=" * 60)
    
    while True:
        opcion = input("\nSeleccione una opción (0-7): ").strip()
        if opcion == '0':
            return ingresar_matriz()
        elif opcion in ejemplos:
            print(f"\n✓ Seleccionado: {ejemplos[opcion]['nombre']}")
            return ejemplos[opcion]['matriz']
        else:
            print("❌ Opción inválida. Intente nuevamente.")


def main():
    """
    Función principal del programa
    """
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "SISTEMAS DINÁMICOS 2D HOMOGÉNEOS" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Obtener la matriz del sistema
    matriz = ejemplos_predefinidos()
    
    # Crear el sistema dinámico
    sistema = SistemaDinamico2D(matriz)
    
    # Mostrar análisis
    sistema.mostrar_analisis()
    
    # Preguntar si desea graficar
    print("\n")
    graficar = input("¿Desea graficar el sistema? (s/n): ").strip().lower()
    
    if graficar == 's' or graficar == 'si' or graficar == 'sí':
        print("\nGenerando gráfica...")
        sistema.graficar_sistema()
    
    # Preguntar si desea analizar otro sistema
    print("\n")
    otro = input("¿Desea analizar otro sistema? (s/n): ").strip().lower()
    
    if otro == 's' or otro == 'si' or otro == 'sí':
        main()
    else:
        print("\n¡Gracias por usar el programa!\n")


if __name__ == "__main__":
    main()
