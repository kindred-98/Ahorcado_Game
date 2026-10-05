"""
accion_eliminar_palabra.py
==========================
Acción del submenú: eliminar una palabra de la base de datos.
"""

from src.interfaz.pantalla.limpiar_pantalla      import limpiar_pantalla
from src.interfaz.pantalla.mostrar_mensaje       import mostrar_mensaje
from src.interfaz.pantalla.mostrar_error         import mostrar_error
from src.interfaz.menu.constantes_menu            import PEDIR_ENTER
from src.base_datos.insercion.eliminar_palabra   import eliminar_palabra
from src.base_datos.insercion.palabra_ya_existe  import palabra_ya_existe


def _accion_eliminar_palabra() -> None:
    """
    Solicita al jugador la palabra a eliminar, confirma
    que existe y la borra de la base de datos.
    """
    limpiar_pantalla()
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║       🗑️  ELIMINAR PALABRA                   ║")
    print("  ╚══════════════════════════════════════════════╝\n")

    palabra = input("  Palabra a eliminar > ").strip().lower()

    if not palabra:
        mostrar_error("Debes ingresar una palabra.")
        input(PEDIR_ENTER)
        return

    if not palabra_ya_existe(palabra):
        mostrar_error(f"La palabra '{palabra}' no existe en la base de datos.")
        input(PEDIR_ENTER)
        return

    confirmacion = input(
        f"\n  ¿Seguro que quieres eliminar '{palabra.upper()}'? (s/n) > "
    ).strip().lower()

    if confirmacion not in ("s", "si", "sí"):
        mostrar_mensaje("Operación cancelada.")
        input(PEDIR_ENTER)
        return

    if eliminar_palabra(palabra):
        mostrar_mensaje(f"✅  Palabra '{palabra.upper()}' eliminada correctamente.")
    else:
        mostrar_error("No se pudo eliminar la palabra. Inténtalo de nuevo.")

    input(PEDIR_ENTER)