"""
test_inicializar_base_datos.py
==============================
Tests para src/base_datos/inicializar/inicializar_base_datos.py
"""

from src.base_datos.inicializar.inicializar_base_datos import inicializar_base_datos


def test_tabla_creada_tras_inicializar(bd_prueba):
    inicializar_base_datos()
    cursor = bd_prueba.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='palabras'"
    )
    assert cursor.fetchone() is not None

def test_palabras_iniciales_insertadas(bd_prueba):
    inicializar_base_datos()
    total = bd_prueba.execute("SELECT COUNT(*) FROM palabras").fetchone()[0]
    assert total >= 20

def test_inicializar_es_idempotente(bd_prueba):
    inicializar_base_datos()
    total_primera = bd_prueba.execute("SELECT COUNT(*) FROM palabras").fetchone()[0]
    inicializar_base_datos()
    total_segunda = bd_prueba.execute("SELECT COUNT(*) FROM palabras").fetchone()[0]
    assert total_primera == total_segunda

def test_palabras_tienen_todos_los_campos(bd_prueba):
    inicializar_base_datos()
    fila = bd_prueba.execute(
        "SELECT palabra, categoria, dificultad FROM palabras LIMIT 1"
    ).fetchone()
    assert fila is not None
    assert fila[0]
    assert fila[1]
    assert fila[2]