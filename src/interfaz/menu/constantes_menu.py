"""
constantes_menu.py
==================
Constantes de opciones y mensajes del menú principal.
"""

OPCION_JUGAR:             str = "1"
OPCION_GESTIONAR_PALABRAS: str = "2"
OPCION_SALIR:             str = "3"

OPCIONES_VALIDAS: tuple[str, ...] = (
    OPCION_JUGAR,
    OPCION_GESTIONAR_PALABRAS,
    OPCION_SALIR,
)

PEDIR_ENTER:             str = "\n  Presiona ENTER para continuar..."
PEDIR_ENTER_VOLVER_MENU: str = "\n  Presiona ENTER para volver al menú..."