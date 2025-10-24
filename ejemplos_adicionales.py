"""
Ejemplos Adicionales de Sistemas Dinámicos 2D
Colección de matrices interesantes para explorar
"""

EJEMPLOS_ADICIONALES = {
    "Sistemas de Población": {
        "Competencia entre especies": {
            "matriz": [[-1, -0.5], [-0.5, -1]],
            "descripcion": "Dos especies compitiendo por recursos. Ambas decrecen."
        },
        "Depredador-Presa": {
            "matriz": [[0.5, -0.5], [0.5, -0.5]],
            "descripcion": "Modelo simplificado depredador-presa. Punto silla."
        },
        "Simbiosis": {
            "matriz": [[0.5, 0.3], [0.3, 0.5]],
            "descripcion": "Dos especies que se benefician mutuamente."
        }
    },
    
    "Sistemas Mecánicos": {
        "Oscilador armónico sin fricción": {
            "matriz": [[0, 1], [-1, 0]],
            "descripcion": "Movimiento oscilatorio puro. Centro con órbitas circulares."
        },
        "Oscilador amortiguado subcrítico": {
            "matriz": [[0, 1], [-4, -2]],
            "descripcion": "Oscilaciones con amortiguamiento. Espiral estable."
        },
        "Oscilador amortiguado sobrecrítico": {
            "matriz": [[0, 1], [-1, -4]],
            "descripcion": "Retorno sin oscilación. Nodo estable."
        },
        "Péndulo linealizado inestable": {
            "matriz": [[0, 1], [1, 0]],
            "descripcion": "Péndulo invertido. Punto silla."
        }
    },
    
    "Sistemas Eléctricos": {
        "Circuito RLC subamortiguado": {
            "matriz": [[0, 1], [-5, -0.5]],
            "descripcion": "Circuito RLC con poca resistencia. Espiral estable."
        },
        "Circuito RLC crítico": {
            "matriz": [[0, 1], [-1, -2]],
            "descripcion": "Amortiguamiento crítico. Retorno rápido sin oscilación."
        }
    },
    
    "Casos Especiales": {
        "Expansión uniforme": {
            "matriz": [[2, 0], [0, 2]],
            "descripcion": "Todas las direcciones se expanden igual. Nodo estrella inestable."
        },
        "Contracción uniforme": {
            "matriz": [[-1, 0], [0, -1]],
            "descripcion": "Todas las direcciones se contraen igual. Nodo estrella estable."
        },
        "Rotación pura": {
            "matriz": [[0, 2], [-2, 0]],
            "descripcion": "Rotación sin cambio de magnitud. Centro."
        },
        "Shear transformation": {
            "matriz": [[1, 1], [0, 1]],
            "descripcion": "Transformación de cizalladura. Nodo degenerado inestable."
        },
        "Espiral dorada": {
            "matriz": [[0.1, -1], [1, 0.1]],
            "descripcion": "Espiral lenta hacia afuera. Espiral inestable."
        }
    },
    
    "Transiciones Interesantes": {
        "Casi un centro (muy leve espiral estable)": {
            "matriz": [[-0.01, 1], [-1, -0.01]],
            "descripcion": "Espiral muy lenta hacia el origen."
        },
        "Casi punto silla": {
            "matriz": [[0.9, 0], [0, -1]],
            "descripcion": "Silla con autovalor positivo pequeño."
        },
        "Nodo con ratio extremo": {
            "matriz": [[-10, 0], [0, -0.1]],
            "descripcion": "Velocidades muy diferentes en cada dirección."
        }
    }
}


def imprimir_ejemplos():
    """Imprime todos los ejemplos disponibles"""
    print("=" * 80)
    print("EJEMPLOS ADICIONALES DE SISTEMAS DINÁMICOS 2D")
    print("=" * 80)
    
    for categoria, ejemplos in EJEMPLOS_ADICIONALES.items():
        print(f"\n{'─' * 80}")
        print(f"📁 {categoria.upper()}")
        print('─' * 80)
        
        for nombre, datos in ejemplos.items():
            matriz = datos['matriz']
            desc = datos['descripcion']
            
            print(f"\n  🔹 {nombre}")
            print(f"     Matriz: {matriz}")
            print(f"     {desc}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    imprimir_ejemplos()
