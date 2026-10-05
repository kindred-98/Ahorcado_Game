"""
accion_añadir_palabra.py
========================
Acción del menú: añadir una nueva palabra a la base de datos.
"""

from src.interfaz.pantalla.limpiar_pantalla      import limpiar_pantalla
from src.interfaz.pantalla.mostrar_mensaje       import mostrar_mensaje
from src.interfaz.pantalla.mostrar_error         import mostrar_error
from src.interfaz.menu.pedir_campo_validado      import _pedir_campo_validado
from src.interfaz.menu.constantes_menu           import PEDIR_ENTER_VOLVER_MENU
from src.base_datos.insercion.insertar_palabra   import insertar_palabra
from src.base_datos.insercion.palabra_ya_existe  import palabra_ya_existe
from src.validaciones.palabra.validar_palabra    import validar_palabra
from src.validaciones.palabra.validar_categoria  import validar_categoria
from src.validaciones.palabra.validar_dificultad import validar_dificultad
from src.validaciones.palabra.constantes         import CATEGORIAS_VALIDAS, DIFICULTADES_VALIDAS


def _accion_anadir_palabra() -> None:
    """
    Solicita palabra, categoría y dificultad al jugador,
    valida cada campo y confirma si fue insertada correctamente.
    """
    limpiar_pantalla()
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║       📖  AÑADIR NUEVA PALABRA               ║")
    print("  ╚══════════════════════════════════════════════╝\n")

    categorias_texto  = " / ".join(sorted(CATEGORIAS_VALIDAS))
    dificultades_texto = " / ".join(sorted(DIFICULTADES_VALIDAS))

    nueva_palabra = _pedir_campo_validado(
        etiqueta  = "Palabra",
        validador = validar_palabra,
    )
    nueva_categoria = _pedir_campo_validado(
        etiqueta  = f"Categoría ({categorias_texto})",
        validador = validar_categoria,
    )
    nueva_dificultad = _pedir_campo_validado(
        etiqueta  = f"Dificultad ({dificultades_texto})",
        validador = validar_dificultad,
    )

    if palabra_ya_existe(nueva_palabra):
        mostrar_error(f"La palabra '{nueva_palabra}' ya existe en la base de datos.")
    else:
        fue_insertada = insertar_palabra(nueva_palabra, nueva_categoria, nueva_dificultad)
        if fue_insertada:
            mostrar_mensaje(f"✅  Palabra '{nueva_palabra.upper()}' añadida correctamente.")
        else:
            mostrar_error("No se pudo añadir la palabra. Inténtalo de nuevo.")

    input(PEDIR_ENTER_VOLVER_MENU)