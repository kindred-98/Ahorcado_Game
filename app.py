"""
app.py
======
Servidor Flask para El Ahorcado Medieval.

Uso:
    python app.py

Variables de entorno opcionales:
    AHORCADO_SECRET_KEY  Clave para firmar las cookies de sesión.
                         Si no se define, se usa (o se genera) el
                         archivo local ".secret_key" (no versionado).
    FLASK_DEBUG          Poner "1" para activar el modo depuración.
    FLASK_PORT           Puerto del servidor (por defecto 5000).

Seguridad:
    La app usa CSRFProtect de Flask-WTF: todas las rutas que cambian
    estado exigen el token "X-CSRFToken" que el front-end lee de la
    etiqueta <meta name="csrf-token"> de index.html.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_wtf.csrf import CSRFProtect
import secrets
import sys
import os

RUTA_CLAVE_SECRETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".secret_key")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.base_datos.inicializar.inicializar_base_datos import inicializar_base_datos
from src.base_datos.consultas.obtener_palabra_aleatoria import obtener_palabra_aleatoria
from src.base_datos.consultas.obtener_todas_las_palabras import obtener_todas_las_palabras
from src.base_datos.consultas.obtener_categorias import obtener_categorias
from src.base_datos.insercion.insertar_palabra import insertar_palabra


def _obtener_clave_secreta() -> str:
    """
    Resuelve la clave de firma de sesión sin dejarla en el código.

    Prioridad: variable de entorno AHORCADO_SECRET_KEY, archivo local
    ".secret_key" (ignorado por Git) y, como último recurso, una clave
    aleatoria válida solo para la sesión actual.

    Returns:
        str: Clave secreta para firmar las cookies de sesión.
    """
    clave_del_entorno = os.environ.get("AHORCADO_SECRET_KEY", "").strip()
    if clave_del_entorno:
        return clave_del_entorno

    if os.path.exists(RUTA_CLAVE_SECRETA):
        try:
            with open(RUTA_CLAVE_SECRETA, encoding="utf-8") as archivo:
                clave_guardada = archivo.read().strip()
            if clave_guardada:
                return clave_guardada
        except OSError:
            pass

    clave_generada = secrets.token_hex(32)
    try:
        with open(RUTA_CLAVE_SECRETA, "w", encoding="utf-8") as archivo:
            archivo.write(clave_generada)
    except OSError:
        pass

    return clave_generada


app = Flask(__name__)
app.secret_key = _obtener_clave_secreta()

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

csrf = CSRFProtect(app)

inicializar_base_datos()

MAX_FALLOS = 6


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/jugar", methods=["POST"])
def jugar():
    data = request.get_json() or {}
    dificultad = data.get("dificultad") or None

    datos = obtener_palabra_aleatoria(dificultad=dificultad)
    if not datos:
        return jsonify({"error": "No hay palabras disponibles"}), 400

    session["palabra"] = datos["palabra"].lower()
    session["categoria"] = datos["categoria"]
    session["dificultad"] = datos["dificultad"]
    session["correctas"] = []
    session["fallidas"] = []
    session["fallos"] = 0

    return jsonify({
        "categoria": datos["categoria"],
        "dificultad": datos["dificultad"],
        "longitud": len(datos["palabra"]),
        "palabra_oculta": "_ " * len(datos["palabra"]),
        "fallos": 0,
        "max_fallos": MAX_FALLOS,
        "terminado": False,
        "resultado": None
    })


@app.route("/api/intentar", methods=["POST"])
def intentar():
    if "palabra" not in session:
        return jsonify({"error": "No hay partida activa"}), 400

    data = request.get_json() or {}
    letra = data.get("letra", "").lower()

    if not letra or len(letra) != 1:
        return jsonify({"error": "Envía una sola letra"}), 400

    correctas = session["correctas"]
    fallidas = session["fallidas"]

    if letra in correctas or letra in fallidas:
        return jsonify({"error": "Ya usaste esa letra"}), 400

    palabra = session["palabra"]

    if letra in palabra:
        correctas.append(letra)
        session["correctas"] = correctas
    else:
        fallidas.append(letra)
        session["fallidas"] = fallidas
        session["fallos"] = session.get("fallos", 0) + 1

    fallos = session["fallos"]

    # Construir palabra oculta
    palabra_oculta = ""
    for c in palabra:
        if c in correctas:
            palabra_oculta += c.upper() + " "
        else:
            palabra_oculta += "_ "

    # Verificar victoria/derrota
    terminado = False
    resultado = None

    if set(palabra).issubset(set(correctas)):
        terminado = True
        resultado = "victoria"
    elif fallos >= MAX_FALLOS:
        terminado = True
        resultado = "derrota"

    response = {
        "palabra_oculta": palabra_oculta.strip(),
        "correctas": correctas,
        "fallidas": fallidas,
        "fallos": fallos,
        "max_fallos": MAX_FALLOS,
        "terminado": terminado,
        "resultado": resultado
    }

    if terminado:
        response["palabra_completa"] = palabra.upper()
        session.pop("palabra", None)

    return jsonify(response)


@app.route("/api/categorias", methods=["GET"])
def categorias():
    cats = obtener_categorias()
    return jsonify(cats)


@app.route("/api/palabras", methods=["GET"])
def palabras():
    p = obtener_todas_las_palabras()
    return jsonify(p)


@app.route("/api/anadir", methods=["POST"])
def anadir():
    data = request.get_json() or {}
    palabra = data.get("palabra", "").strip().lower()
    categoria = data.get("categoria", "").strip().lower()
    dificultad = data.get("dificultad", "").strip().lower()

    if not palabra or len(palabra) < 3 or len(palabra) > 30:
        return jsonify({"error": "La palabra debe tener entre 3 y 30 caracteres"}), 400
    if not palabra.isalpha():
        return jsonify({"error": "Solo se permiten letras"}), 400
    if not categoria:
        return jsonify({"error": "Introduce una categoría"}), 400
    if dificultad not in ("facil", "medio", "dificil", "legendario"):
        return jsonify({"error": "Dificultad no válida"}), 400

    if insertar_palabra(palabra, categoria, dificultad):
        return jsonify({"ok": True, "mensaje": f'Palabra "{palabra}" añadida'})
    else:
        return jsonify({"error": "La palabra ya existe"}), 400


if __name__ == "__main__":
    puerto = int(os.environ.get("FLASK_PORT", "5000"))
    depurar = os.environ.get("FLASK_DEBUG", "").strip().lower() in ("1", "true", "yes", "on")
    app.run(host="127.0.0.1", port=puerto, debug=depurar)
