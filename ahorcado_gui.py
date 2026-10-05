"""
ahorcado_gui.py
===============
Interfaz gráfica para El Ahorcado Medieval.
Usa tkinter (incluido en Python) sin dependencias externas.

Uso:
    python ahorcado_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.base_datos.inicializar.inicializar_base_datos import inicializar_base_datos
from src.base_datos.consultas.obtener_palabra_aleatoria import obtener_palabra_aleatoria
from src.base_datos.consultas.obtener_todas_las_palabras import obtener_todas_las_palabras
from src.base_datos.consultas.obtener_categorias import obtener_categorias
from src.base_datos.insercion.insertar_palabra import insertar_palabra
from src.juego.estado.clase_estado_partida import EstadoPartida
from src.juego.logica.hay_victoria import hay_victoria
from src.juego.logica.hay_derrota import hay_derrota
from src.juego.logica.letra_en_palabra import letra_en_palabra

MAX_FALLOS = 6

MENSAJES_FALLOS = [
    "La cuerda espera...",
    "Se acerca el peligro...",
    "El destino se acerca...",
    "No te queda mucho tiempo...",
    "Casi es demasiado tarde...",
    "¡Último aviso!",
    "¡GAME OVER!"
]

COLORES = {
    "fondo": "#2b2b2b",
    "panel": "#3c3f41",
    "texto": "#ffffff",
    "acento": "#c7a44a",
    "exito": "#4caf50",
    "error": "#e74c3c",
    "boton": "#4a4a4a",
    "boton_hover": "#5a5a5a",
    "correcta": "#27ae60",
    "fallida": "#c0392b",
    "deshabilitado": "#555555"
}

# Estilo de ttk usado por los títulos de cada pantalla
ESTILO_TITULO = "Titulo.TLabel"

# Eventos del ratón para el efecto hover de los botones
EVENTO_ENTRADA = "<Enter>"
EVENTO_SALIDA = "<Leave>"


class AhorcadoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Ahorcado Medieval")
        self.geometry("800x700")
        self.resizable(False, False)
        self.configure(bg=COLORES["fondo"])

        self.estado = None
        self.botones_letras = {}

        self._configurar_estilos()
        self._mostrar_menu_principal()

    def _configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background=COLORES["fondo"])
        self.style.configure("Panel.TFrame", background=COLORES["panel"])
        self.style.configure(
            ESTILO_TITULO,
            background=COLORES["fondo"],
            foreground=COLORES["acento"],
            font=("Georgia", 28, "bold")
        )
        self.style.configure(
            "Subtitulo.TLabel",
            background=COLORES["fondo"],
            foreground=COLORES["texto"],
            font=("Georgia", 14)
        )
        self.style.configure(
            "Info.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["texto"],
            font=("Consolas", 12)
        )
        self.style.configure(
            "Palabra.TLabel",
            background=COLORES["panel"],
            foreground=COLORES["acento"],
            font=("Consolas", 24, "bold")
        )
        self.style.configure(
            "Menu.TButton",
            font=("Georgia", 14),
            padding=15
        )

    def _limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ==================== MENÚ PRINCIPAL ====================

    def _mostrar_menu_principal(self):
        self._limpiar_ventana()

        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame, text="⚔ El Ahorcado Medieval ⚔", style=ESTILO_TITULO
        ).pack(pady=(0, 40))

        botones = [
            ("🎮  Jugar", self._mostrar_seleccion_dificultad),
            ("➕  Añadir Palabra", self._mostrar_anadir_palabra),
            ("📋  Ver Palabras", self._mostrar_ver_palabras),
            ("🚪  Salir", self._salir),
        ]

        for texto, comando in botones:
            btn = tk.Button(
                frame,
                text=texto,
                command=comando,
                font=("Georgia", 14),
                bg=COLORES["boton"],
                fg=COLORES["texto"],
                activebackground=COLORES["boton_hover"],
                activeforeground=COLORES["texto"],
                relief="flat",
                width=25,
                pady=8,
                cursor="hand2"
            )
            btn.pack(pady=6)
            btn.bind(EVENTO_ENTRADA, lambda e, b=btn: b.configure(bg=COLORES["boton_hover"]))
            btn.bind(EVENTO_SALIDA, lambda e, b=btn: b.configure(bg=COLORES["boton"]))

    # ==================== SELECCIÓN DE DIFICULTAD ====================

    def _mostrar_seleccion_dificultad(self):
        self._limpiar_ventana()

        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame, text="Selecciona Dificultad", style=ESTILO_TITULO
        ).pack(pady=(0, 30))

        dificultades = [
            ("Fácil", "facil", "#27ae60"),
            ("Medio", "medio", "#f39c12"),
            ("Difícil", "dificil", "#e74c3c"),
            ("Legendario", "legendario", "#8e44ad"),
            ("🎲  Aleatorio", None, COLORES["acento"]),
        ]

        for texto, dificultad, color in dificultades:
            btn = tk.Button(
                frame,
                text=texto,
                command=lambda d=dificultad: self._iniciar_juego(dificultad=d),
                font=("Georgia", 13),
                bg=COLORES["boton"],
                fg=color,
                activebackground=COLORES["boton_hover"],
                activeforeground=color,
                relief="flat",
                width=25,
                pady=6,
                cursor="hand2"
            )
            btn.pack(pady=5)
            btn.bind(EVENTO_ENTRADA, lambda e, b=btn: b.configure(bg=COLORES["boton_hover"]))
            btn.bind(EVENTO_SALIDA, lambda e, b=btn: b.configure(bg=COLORES["boton"]))

        self._crear_boton_volver(frame, self._mostrar_menu_principal)

    # ==================== JUEGO ====================

    def _iniciar_juego(self, dificultad=None):
        datos = obtener_palabra_aleatoria(dificultad=dificultad)
        if not datos:
            messagebox.showerror("Error", "No hay palabras disponibles.")
            return

        self.estado = EstadoPartida(
            palabra_secreta=datos["palabra"].lower(),
            categoria=datos["categoria"],
            dificultad=datos["dificultad"]
        )

        self._mostrar_pantalla_juego()

    def _mostrar_pantalla_juego(self):
        self._limpiar_ventana()

        # Marco superior con info
        frame_info = tk.Frame(self, bg=COLORES["panel"], pady=10)
        frame_info.pack(fill="x")

        tk.Label(
            frame_info,
            text=f"Categoría: {self.estado.categoria.upper()}  |  "
                 f"Dificultad: {self.estado.dificultad.upper()}",
            bg=COLORES["panel"],
            fg=COLORES["acento"],
            font=("Georgia", 11)
        ).pack()

        # Canvas para el dibujo
        self.canvas = tk.Canvas(
            self, width=300, height=300,
            bg=COLORES["fondo"], highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self._dibujar_ahorcado()

        # Palabra oculta
        self.label_palabra = tk.Label(
            self,
            text=self._obtener_palabra_oculta(),
            bg=COLORES["fondo"],
            fg=COLORES["acento"],
            font=("Consolas", 28, "bold")
        )
        self.label_palabra.pack(pady=10)

        # Mensaje de estado
        self.label_mensaje = tk.Label(
            self,
            text=MENSAJES_FALLOS[self.estado.numero_fallos],
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Georgia", 11, "italic")
        )
        self.label_mensaje.pack()

        # Contador de fallos
        self.label_fallos = tk.Label(
            self,
            text=f"Fallos: {self.estado.numero_fallos} / {MAX_FALLOS}",
            bg=COLORES["fondo"],
            fg=COLORES["error"],
            font=("Georgia", 10)
        )
        self.label_fallos.pack(pady=(5, 10))

        # Teclado virtual
        self._crear_teclado()

    def _obtener_palabra_oculta(self):
        resultado = []
        for letra in self.estado.palabra_secreta:
            if letra in self.estado.letras_correctas:
                resultado.append(letra.upper())
            else:
                resultado.append("_")
        return " ".join(resultado)

    def _crear_teclado(self):
        frame_teclado = tk.Frame(self, bg=COLORES["fondo"])
        frame_teclado.pack(pady=10)

        filas = [
            "QWERTYUIOP",
            "ASDFGHJKLÑ",
            "ZXCVBNM"
        ]

        self.botones_letras = {}

        for i, fila in enumerate(filas):
            frame_fila = tk.Frame(frame_teclado, bg=COLORES["fondo"])
            frame_fila.pack()

            if i == 2:
                tk.Label(frame_fila, text="  ", bg=COLORES["fondo"]).pack(side="left")

            for letra in fila:
                letra_lower = letra.lower()
                btn = tk.Button(
                    frame_fila,
                    text=letra,
                    width=3,
                    font=("Consolas", 11, "bold"),
                    bg=COLORES["boton"],
                    fg=COLORES["texto"],
                    activebackground=COLORES["boton_hover"],
                    activeforeground=COLORES["texto"],
                    relief="flat",
                    cursor="hand2",
                    command=lambda l=letra_lower: self._intento_letra(l)
                )
                btn.pack(side="left", padx=2, pady=2)
                btn.bind(EVENTO_ENTRADA, lambda e, b=btn: b.configure(bg=COLORES["boton_hover"])
                         if b["state"] == "normal" else None)
                btn.bind(EVENTO_SALIDA, lambda e, b=btn: b.configure(bg=COLORES["boton"])
                         if b["state"] == "normal" else None)
                self.botones_letras[letra_lower] = btn

    def _intento_letra(self, letra):
        if letra in self.estado.letras_correctas or letra in self.estado.letras_fallidas:
            return

        btn = self.botones_letras[letra]

        if letra_en_palabra(letra, self.estado.palabra_secreta):
            self.estado.letras_correctas.add(letra)
            btn.configure(bg=COLORES["correcta"], state="disabled")
        else:
            self.estado.letras_fallidas.add(letra)
            self.estado.numero_fallos += 1
            btn.configure(bg=COLORES["fallida"], state="disabled")

        self.label_palabra.configure(text=self._obtener_palabra_oculta())
        self.label_mensaje.configure(text=MENSAJES_FALLOS[self.estado.numero_fallos])
        self.label_fallos.configure(text=f"Fallos: {self.estado.numero_fallos} / {MAX_FALLOS}")
        self._dibujar_ahorcado()

        if hay_victoria(self.estado):
            self.after(500, self._mostrar_victoria)
        elif hay_derrota(self.estado):
            self.after(500, self._mostrar_derrota)

    def _dibujar_ahorcado(self):
        self.canvas.delete("all")
        c = self.canvas
        nf = self.estado.numero_fallos if self.estado else 0

        # Suelo
        c.create_line(30, 280, 270, 280, fill="#8B7355", width=4)

        # Poste vertical
        c.create_line(80, 280, 80, 40, fill="#8B4513", width=6)

        # Viga horizontal
        c.create_line(80, 40, 200, 40, fill="#8B4513", width=5)

        # Soga
        c.create_line(200, 40, 200, 70, fill="#D2B48C", width=3)

        # Travesaño diagonal
        c.create_line(80, 80, 120, 40, fill="#8B4513", width=3)

        if nf >= 1:  # Cabeza
            c.create_oval(175, 70, 225, 120, outline="#FFFFFF", width=3)
            c.create_line(188, 90, 195, 95, fill="#FFFFFF", width=2)
            c.create_line(205, 90, 212, 95, fill="#FFFFFF", width=2)
            c.create_line(190, 108, 210, 108, fill="#FFFFFF", width=2)

        if nf >= 2:  # Cuerpo
            c.create_line(200, 120, 200, 200, fill="#FFFFFF", width=3)

        if nf >= 3:  # Brazo izquierdo
            c.create_line(200, 140, 160, 170, fill="#FFFFFF", width=3)

        if nf >= 4:  # Brazo derecho
            c.create_line(200, 140, 240, 170, fill="#FFFFFF", width=3)

        if nf >= 5:  # Pierna izquierda
            c.create_line(200, 200, 165, 250, fill="#FFFFFF", width=3)

        if nf >= 6:  # Pierna derecha
            c.create_line(200, 200, 235, 250, fill="#FFFFFF", width=3)
            # Cara triste
            c.create_line(188, 95, 195, 90, fill="#e74c3c", width=2)
            c.create_line(205, 95, 212, 90, fill="#e74c3c", width=2)
            c.delete(c.find_all())

    def _mostrar_victoria(self):
        self._limpiar_ventana()

        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame, text="🏆 ¡VICTORIA! 🏆",
            bg=COLORES["fondo"], fg=COLORES["exito"],
            font=("Georgia", 32, "bold")
        ).pack(pady=20)

        tk.Label(
            frame, text=f'La palabra era: {self.estado.palabra_secreta.upper()}',
            bg=COLORES["fondo"], fg=COLORES["texto"],
            font=("Georgia", 16)
        ).pack(pady=10)

        tk.Label(
            frame, text=f"Fallos: {self.estado.numero_fallos} / {MAX_FALLOS}",
            bg=COLORES["fondo"], fg=COLORES["acento"],
            font=("Georgia", 12)
        ).pack(pady=5)

        self._crear_botones_fin_partida(frame)

    def _mostrar_derrota(self):
        self._limpiar_ventana()

        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame, text="💀 DERROTA 💀",
            bg=COLORES["fondo"], fg=COLORES["error"],
            font=("Georgia", 32, "bold")
        ).pack(pady=20)

        tk.Label(
            frame, text=f'La palabra era: {self.estado.palabra_secreta.upper()}',
            bg=COLORES["fondo"], fg=COLORES["texto"],
            font=("Georgia", 16)
        ).pack(pady=10)

        self._crear_botones_fin_partida(frame)

    def _crear_botones_fin_partida(self, parent):
        frame_btn = tk.Frame(parent, bg=COLORES["fondo"])
        frame_btn.pack(pady=30)

        btn_jugar = tk.Button(
            frame_btn, text="🔄 Jugar de nuevo",
            command=self._mostrar_seleccion_dificultad,
            font=("Georgia", 12), bg=COLORES["boton"], fg=COLORES["texto"],
            activebackground=COLORES["boton_hover"], activeforeground=COLORES["texto"],
            relief="flat", width=18, pady=6, cursor="hand2"
        )
        btn_jugar.pack(side="left", padx=10)

        btn_menu = tk.Button(
            frame_btn, text="🏠 Menú principal",
            command=self._mostrar_menu_principal,
            font=("Georgia", 12), bg=COLORES["boton"], fg=COLORES["texto"],
            activebackground=COLORES["boton_hover"], activeforeground=COLORES["texto"],
            relief="flat", width=18, pady=6, cursor="hand2"
        )
        btn_menu.pack(side="left", padx=10)

    # ==================== AÑADIR PALABRA ====================

    def _mostrar_anadir_palabra(self):
        self._limpiar_ventana()

        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame, text="Añadir Nueva Palabra", style=ESTILO_TITULO
        ).pack(pady=(0, 30))

        # Palabra
        tk.Label(
            frame, text="Palabra:",
            bg=COLORES["fondo"], fg=COLORES["texto"],
            font=("Georgia", 12)
        ).pack(anchor="w")
        entry_palabra = tk.Entry(
            frame, font=("Consolas", 14), width=30,
            bg=COLORES["panel"], fg=COLORES["texto"],
            insertbackground=COLORES["texto"]
        )
        entry_palabra.pack(pady=(0, 15))

        # Categoría
        tk.Label(
            frame, text="Categoría:",
            bg=COLORES["fondo"], fg=COLORES["texto"],
            font=("Georgia", 12)
        ).pack(anchor="w")

        categorias_existentes = [c["categoria"] for c in obtener_categorias()]
        combo_categoria = ttk.Combobox(
            frame, font=("Consolas", 12), width=28,
            values=categorias_existentes, state="normal"
        )
        combo_categoria.pack(pady=(0, 15))

        # Dificultad
        tk.Label(
            frame, text="Dificultad:",
            bg=COLORES["fondo"], fg=COLORES["texto"],
            font=("Georgia", 12)
        ).pack(anchor="w")

        combo_dificultad = ttk.Combobox(
            frame, font=("Consolas", 12), width=28,
            values=["facil", "medio", "dificil", "legendario"], state="readonly"
        )
        combo_dificultad.pack(pady=(0, 25))

        def guardar():
            palabra = entry_palabra.get().strip().lower()
            categoria = combo_categoria.get().strip().lower()
            dificultad = combo_dificultad.get().strip().lower()

            if not palabra:
                messagebox.showwarning("Aviso", "Introduce una palabra.")
                return
            if len(palabra) < 3 or len(palabra) > 30:
                messagebox.showwarning("Aviso", "La palabra debe tener entre 3 y 30 caracteres.")
                return
            if not palabra.isalpha():
                messagebox.showwarning("Aviso", "La palabra solo puede contener letras.")
                return
            if not categoria:
                messagebox.showwarning("Aviso", "Selecciona o escribe una categoría.")
                return
            if not dificultad:
                messagebox.showwarning("Aviso", "Selecciona una dificultad.")
                return

            if insertar_palabra(palabra, categoria, dificultad):
                messagebox.showinfo("Éxito", f'Palabra "{palabra}" añadida correctamente.')
                self._mostrar_menu_principal()
            else:
                messagebox.showwarning("Aviso", "La palabra ya existe en la base de datos.")

        frame_btn = tk.Frame(frame, bg=COLORES["fondo"])
        frame_btn.pack()

        tk.Button(
            frame_btn, text="💾 Guardar", command=guardar,
            font=("Georgia", 12), bg=COLORES["boton"], fg=COLORES["exito"],
            activebackground=COLORES["boton_hover"], activeforeground=COLORES["exito"],
            relief="flat", width=15, pady=6, cursor="hand2"
        ).pack(side="left", padx=10)

        self._crear_boton_volver(frame, self._mostrar_menu_principal, frame_btn)

    # ==================== VER PALABRAS ====================

    def _mostrar_ver_palabras(self):
        self._limpiar_ventana()

        frame_principal = ttk.Frame(self, style="TFrame")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(
            frame_principal, text="Palabras Registradas", style=ESTILO_TITULO
        ).pack(pady=(0, 15))

        # Frame con scroll
        frame_scroll = tk.Frame(frame_principal, bg=COLORES["panel"])
        frame_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_scroll, bg=COLORES["panel"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg=COLORES["panel"])

        frame_contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        palabras = obtener_todas_las_palabras()

        if not palabras:
            tk.Label(
                frame_contenido,
                text="No hay palabras registradas.",
                bg=COLORES["panel"], fg=COLORES["texto"],
                font=("Georgia", 12)
            ).pack(pady=20)
        else:
            categoria_actual = None
            for p in palabras:
                if p["categoria"] != categoria_actual:
                    categoria_actual = p["categoria"]
                    tk.Label(
                        frame_contenido,
                        text=f"\n⚔ {categoria_actual.upper()} ⚔",
                        bg=COLORES["panel"], fg=COLORES["acento"],
                        font=("Georgia", 14, "bold")
                    ).pack(anchor="w", padx=10, pady=(10, 5))

                colores_dif = {
                    "facil": "#27ae60",
                    "medio": "#f39c12",
                    "dificil": "#e74c3c",
                    "legendario": "#8e44ad"
                }
                color = colores_dif.get(p["dificultad"], COLORES["texto"])

                tk.Label(
                    frame_contenido,
                    text=f"  • {p['palabra']}  [{p['dificultad']}]",
                    bg=COLORES["panel"], fg=color,
                    font=("Consolas", 11)
                ).pack(anchor="w", padx=20)

        self._crear_boton_volver(frame_principal, self._mostrar_menu_principal)

    # ==================== UTILIDADES ====================

    def _crear_boton_volver(self, parent, comando, empaquetar_en=None):
        target = empaquetar_en if empaquetar_en else parent
        btn = tk.Button(
            target, text="← Volver", command=comando,
            font=("Georgia", 11), bg=COLORES["boton"], fg=COLORES["texto"],
            activebackground=COLORES["boton_hover"], activeforeground=COLORES["texto"],
            relief="flat", width=15, pady=5, cursor="hand2"
        )
        if empaquetar_en:
            btn.pack(side="left", padx=10)
        else:
            btn.pack(pady=30)

    def _salir(self):
        self.destroy()


if __name__ == "__main__":
    inicializar_base_datos()
    app = AhorcadoGUI()
    app.mainloop()
