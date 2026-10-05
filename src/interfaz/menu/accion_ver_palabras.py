"""
accion_ver_palabras.py
======================
Acción del menú: mostrar todas las palabras almacenadas.
"""

from src.interfaz.pantalla.limpiar_pantalla          import limpiar_pantalla
from src.interfaz.pantalla.mostrar_error             import mostrar_error
from src.interfaz.menu.constantes_menu                import PEDIR_ENTER_VOLVER_MENU
from src.base_datos.consultas.obtener_todas_las_palabras import obtener_todas_las_palabras


def _accion_ver_palabras() -> None:
    """
    Lista todas las palabras agrupadas por categoría
    con su dificultad y el total al final.
    """
    limpiar_pantalla()
    print("\n  ╔══════════════════════════════════════════════╗")
    print("    ║       📜  PALABRAS EN LA BASE DE DATOS       ║")
    print("    ╚══════════════════════════════════════════════╝\n")

    lista_palabras = obtener_todas_las_palabras()

    if not lista_palabras:
        mostrar_error("No hay palabras en la base de datos.")
    else:
        categoria_actual = ""
        for registro in lista_palabras:
            if registro["categoria"] != categoria_actual:
                categoria_actual = registro["categoria"]
                print(f"\n  ── {categoria_actual.upper()} ──")
            print(f"     {registro['palabra']:<20} {registro['dificultad']}")
        print(f"\n  Total: {len(lista_palabras)} palabras\n")

    input(PEDIR_ENTER_VOLVER_MENU)