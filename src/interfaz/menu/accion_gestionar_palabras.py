"""
accion_gestionar_palabras.py
============================
Submenú de gestión de palabras: ver, añadir, modificar y eliminar.
"""

from src.interfaz.pantalla.limpiar_pantalla          import limpiar_pantalla
from src.interfaz.pantalla.mostrar_error             import mostrar_error
from src.interfaz.menu.constantes_menu                import PEDIR_ENTER
from src.base_datos.consultas.obtener_todas_las_palabras import obtener_todas_las_palabras
from src.interfaz.menu.accion_añadir_palabra         import _accion_anadir_palabra
from src.interfaz.menu.accion_modificar_palabra      import _accion_modificar_palabra
from src.interfaz.menu.accion_eliminar_palabra       import _accion_eliminar_palabra


# ── Constantes del submenú ────────────────────────────────────

_OPCION_VER:       str = "1"
_OPCION_AÑADIR:    str = "2"
_OPCION_MODIFICAR: str = "3"
_OPCION_ELIMINAR:  str = "4"
_OPCION_SALIR:     str = "5"

_OPCIONES_VALIDAS: tuple[str, ...] = (
    _OPCION_VER,
    _OPCION_AÑADIR,
    _OPCION_MODIFICAR,
    _OPCION_ELIMINAR,
    _OPCION_SALIR,
)


def _accion_gestionar_palabras() -> None:
    """
    Bucle del submenú de gestión de palabras.
    Permite ver, añadir, modificar y eliminar palabras.
    """
    while True:
        limpiar_pantalla()
        _mostrar_submenu()
        opcion = _pedir_opcion_submenu()

        if opcion == _OPCION_VER:
            _ver_palabras()

        elif opcion == _OPCION_AÑADIR:
            _accion_anadir_palabra()

        elif opcion == _OPCION_MODIFICAR:
            _accion_modificar_palabra()

        elif opcion == _OPCION_ELIMINAR:
            _accion_eliminar_palabra()

        elif opcion == _OPCION_SALIR:
            break


# ── Funciones privadas ────────────────────────────────────────

def _mostrar_submenu() -> None:
    """
    Muestra las opciones del submenú de gestión de palabras.
    """
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║       📚  GESTIÓN DE PALABRAS                ║")
    print("  ╠══════════════════════════════════════════════╣")
    print("  ║                                              ║")
    print("  ║   1)  📜  Ver palabras                      ║")
    print("  ║   2)  📖  Añadir palabra                    ║")
    print("  ║   3)  ✏️  Modificar palabra                  ║")
    print("  ║   4)  🗑️  Eliminar palabra                   ║")
    print("  ║   5)  🔙  Volver al menú principal          ║")
    print("  ║                                              ║")
    print("  ╚══════════════════════════════════════════════╝\n")


def _pedir_opcion_submenu() -> str:
    """
    Solicita una opción del submenú en bucle hasta recibir
    una entrada válida.

    Returns:
        str: Opción elegida entre "1" y "5".
    """
    while True:
        opcion = input("  Tu elección > ").strip()
        if opcion in _OPCIONES_VALIDAS:
            return opcion
        mostrar_error("Opción no válida. Elige entre 1 y 5.")


def _ver_palabras() -> None:
    """
    Muestra todas las palabras agrupadas por categoría.
    """
    limpiar_pantalla()
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║       📜  PALABRAS EN LA BASE DE DATOS       ║")
    print("  ╚══════════════════════════════════════════════╝\n")

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

    input(PEDIR_ENTER)