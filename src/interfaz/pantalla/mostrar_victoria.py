"""
mostrar_victoria.py
===================
Función para mostrar la animación de victoria al jugador.
"""

import time
import os


# ── Frames de la animación ────────────────────────────────────

_FRAMES: list[str] = [

r"""
  .      ✦       .        ✦      .       ✦       .       ✦      .
     ✦       .        ✦      .       ✦       .       ✦      .


         ⚔                                            ⚔
        /|\                                          /|\
       / | \          ¡¡ V I C T O R I A !!         / | \
      /  |  \                  BABY                /  |  \


  .      ✦       .        ✦      .       ✦       .       ✦      .
""",

r"""
  .      ✦       .        ✦      .       ✦       .       ✦      .
     ✦       .        ✦      .       ✦       .       ✦      .


        \⚔/                                        \⚔/
         |             ¡¡ V I C T O R I A !!        |
        / \                 ESTAMOS READY🎯        / \
       /   \                                       /   \


  .      ✦       .        ✦      .       ✦       .       ✦      .
""",

r"""
  .      ✦       .        ✦      .       ✦       .       ✦      .
     ✦       .        ✦      .       ✦       .       ✦      .

     ✦
         ⚔                                            ⚔
        /|\          * ¡¡ V I C T O R I A !! *       /|\
       / | \        *  ¡El reino está a salvo!  *    / | \
      /  |  \        *          GG 🕹️ WP        *   /  |  \
                      **************************
  .      ✦       .        ✦      .       ✦       .       ✦      .
""",

r"""
  .      ✦       .        ✦      .       ✦       .       ✦      .
     ✦       .        ✦      .       ✦       .       ✦      .

              ✦           ✦            ✦           ✦
   ⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔
   ║                                                     ║
   ║   ✦ ¡FELICIDADES! HAS ADIVINADO LA PALABRA 🏆 ✦    ║
   ║                                                     ║
   ⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔⚔ 
              ✦           ✦            ✦           ✦

  .      ✦       .        ✦      .       ✦       .       ✦      .
""",
]

_DURACION_FRAME: float = 0.4  # segundos entre frames
_REPETICIONES:   int   = 3    # veces que se repite la animación

# ── Marco de la pantalla final ────────────────────────────────

_FILA_VACIA: str = "  ║                                                          ║"


# ── Función pública ───────────────────────────────────────────

def mostrar_victoria(palabra_secreta: str) -> None:
    """
    Muestra una animación ASCII de victoria en la terminal.

    Args:
        palabra_secreta (str): Palabra que el jugador adivinó,
                               mostrada al final de la animación.
    """
    for _ in range(_REPETICIONES):
        for frame in _FRAMES:
            os.system("cls" if os.name == "nt" else "clear")
            print(frame)
            time.sleep(_DURACION_FRAME)

    os.system("cls" if os.name == "nt" else "clear")
    _mostrar_pantalla_final(palabra_secreta)


# ── Función privada ───────────────────────────────────────────

def _mostrar_pantalla_final(palabra_secreta: str) -> None:
    """
    Muestra la pantalla final estática después de la animación.

    Args:
        palabra_secreta (str): Palabra adivinada por el jugador.
    """
    print("\n")
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║                       ¡¡ VICTORIA !!                     ║")
    print(_FILA_VACIA)
    print("  ║   ⚔   🪢❌ La cuerda se queda guardada… ¡ganaste!   ⚔    ║")
    print(_FILA_VACIA)
    print(f"  ║   La palabra era: {palabra_secreta.upper():<38} ║")
    print(_FILA_VACIA)
    print("  ║   ✦  El reino está a salvo gracias a ti 💪 ✦             ║")
    print(_FILA_VACIA)
    print("  ╚══════════════════════════════════════════════════════════╝")
    print("\n")

     