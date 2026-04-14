# =============================================================================
# repositories/db/conexion.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Gestiona la conexión a la base de datos SQLite.
# Solo existe UNA conexión durante toda la ejecución del sistema —
# eso se llama patrón Singleton.
#
# ¿POR QUÉ UN SINGLETON?
# Abrir y cerrar conexiones a la BD en cada operación es lento y
# puede causar conflictos si dos partes del código intentan escribir
# al mismo tiempo. Con una sola conexión compartida evitamos eso.
#
# ¿DÓNDE SE CREA EL ARCHIVO .db?
# SQLite guarda todo en un solo archivo en disco. Por defecto lo
# creamos en la raíz del proyecto como "inventario.db". Si el archivo
# no existe, SQLite lo crea automáticamente al conectarse.
# =============================================================================

import sqlite3
import os
from pathlib import Path


# Ruta al archivo de base de datos — en la raíz del proyecto
# Path(__file__) es la ruta de este archivo (conexion.py)
# .parent.parent.parent sube tres niveles: db/ → repositories/ → raíz
_RUTA_BD = Path(__file__).parent.parent.parent / "inventario.db"

# Ruta al archivo schema.sql — en la misma carpeta que este archivo
_RUTA_SCHEMA = Path(__file__).parent / "schema.sql"

# Variable global que guarda la única conexión activa
# Empieza en None y se inicializa la primera vez que se llama a obtener()
_conexion: sqlite3.Connection | None = None


def obtener() -> sqlite3.Connection:
    """
    Retorna la conexión activa a la base de datos.
    Si no existe, la crea e inicializa las tablas.

    Patrón Singleton: siempre retorna la misma instancia de conexión.

    Uso desde cualquier repository:
        from repositories.db.conexion import obtener
        con = obtener()
        con.execute("SELECT * FROM productos")
    """
    global _conexion

    if _conexion is None:
        # Primera llamada — creamos la conexión
        _conexion = sqlite3.connect(str(_RUTA_BD))

        # check_same_thread=False permite usar la misma conexión desde
        # distintas partes del código (necesario en algunos contextos).
        _conexion = sqlite3.connect(
            str(_RUTA_BD),
            check_same_thread=False
        )

        # row_factory: hace que cada fila retornada sea un objeto
        # accesible por nombre de columna, no solo por índice.
        # SIN row_factory: fila[0], fila[1], fila[2]...
        # CON row_factory: fila["nombre"], fila["documento"]...
        # Mucho más legible y menos propenso a errores.
        _conexion.row_factory = sqlite3.Row

        # Activamos las foreign keys — SQLite las tiene desactivadas
        # por defecto por compatibilidad histórica. Con esto activado,
        # si intentas insertar un detalle con un factura_id que no existe,
        # SQLite lanzará un error en vez de aceptarlo silenciosamente.
        _conexion.execute("PRAGMA foreign_keys = ON")

        # Inicializamos las tablas si no existen
        _inicializar_tablas(_conexion)

    return _conexion


def _inicializar_tablas(con: sqlite3.Connection) -> None:
    """
    Lee schema.sql y ejecuta todas las instrucciones CREATE TABLE
    e CREATE INDEX para crear la estructura de la BD.

    Se ejecuta solo una vez — las instrucciones usan IF NOT EXISTS
    así que si las tablas ya existen no hace nada.
    """
    with open(_RUTA_SCHEMA, "r", encoding="utf-8") as f:
        sql = f.read()

    # executescript ejecuta múltiples instrucciones SQL separadas por ;
    # en una sola llamada, lo que es más eficiente que ejecutarlas una a una
    con.executescript(sql)
    con.commit()


def cerrar() -> None:
    """
    Cierra la conexión activa y libera los recursos.
    Se llama desde main.py al terminar el programa.

    Buena práctica: siempre cerrar la conexión al salir para
    garantizar que todos los datos pendientes se escriban en disco.
    """
    global _conexion
    if _conexion is not None:
        _conexion.close()
        _conexion = None