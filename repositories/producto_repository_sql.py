# =============================================================================
# repositories/producto_repository_sql.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Versión SQLite de ProductoRepository. Gestiona la tabla 'productos'.
#
# DIFERENCIA IMPORTANTE CON LA VERSIÓN EN MEMORIA:
# En la versión en memoria, el ID se generaba con un contador interno
# (self._siguiente_id). En SQLite, el ID lo genera la BD automáticamente
# con AUTOINCREMENT — no necesitamos ni generar ni liberar IDs.
# SQLite garantiza que el ID es único y autoincremental.
#
# Sin embargo, mantenemos generar_id() y liberar_ultimo_id() como métodos
# vacíos para que el service no necesite cambiar su código — sigue llamando
# generar_id() pero con SQLite simplemente no hace falta.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from repositories.db.conexion import obtener
from models.producto import Producto
from exceptions.app_exceptions import (
    ProductoYaExisteError,
    ProductoNoEncontradoError,
)


class ProductoRepositorySQL(BaseRepository):
    """
    Implementación SQLite del repositorio de productos.
    Reemplaza a ProductoRepository (listas en memoria) en producción.
    """

    def __init__(self):
        self._con = obtener()

    # -------------------------------------------------------------------------
    # GESTIÓN DE ID (compatibilidad con el service)
    # -------------------------------------------------------------------------

    def generar_id(self) -> int:
        """
        Con SQLite no necesitamos generar IDs manualmente — AUTOINCREMENT
        lo hace. Retornamos -1 como placeholder; el ID real lo asigna
        SQLite en el INSERT y lo recuperamos con lastrowid.

        El service llama a generar_id() antes de crear el Producto,
        pero con SQLite ese valor no se usa realmente.
        """
        return -1  # SQLite asigna el ID real al insertar

    def liberar_ultimo_id(self) -> None:
        """
        En la versión en memoria, esto devolvía el ID cuando se cancelaba
        una factura. Con SQLite no hace falta — AUTOINCREMENT no se puede
        "devolver", pero tampoco hay problema porque los IDs cancelados
        simplemente se saltan (1, 2, 4 si el 3 se canceló) y eso es normal.
        """
        pass  # No necesario con AUTOINCREMENT

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD
    # -------------------------------------------------------------------------

    def guardar(self, producto: Producto) -> None:
        """
        Inserta un nuevo producto en la tabla 'productos'.
        Después del INSERT recuperamos el ID generado por SQLite
        y lo asignamos al objeto producto.

        Lanza:
            ProductoYaExisteError: si ya existe un producto con ese nombre.
        """
        # Verificamos duplicado de nombre antes del INSERT
        if self.nombre_existe(producto.nombre):
            raise ProductoYaExisteError(
                f"Ya existe un producto con el nombre '{producto.nombre}'"
            )

        cursor = self._con.execute(
            """
            INSERT INTO productos (nombre, precio, categoria, stock, disponibilidad)
            VALUES (?, ?, ?, ?, ?)
            """,
            (producto.nombre, producto.precio, producto.categoria,
             producto.stock, producto.disponibilidad)
        )
        self._con.commit()

        # lastrowid es el ID que SQLite asignó automáticamente al INSERT.
        # Lo guardamos en el objeto para que el service y la UI lo tengan.
        # Antes: id_nuevo = repo.generar_id() → ahora SQLite lo genera.
        producto.codigo = cursor.lastrowid

    def buscar_por_id(self, codigo: int) -> Optional[Producto]:  # type: ignore[override]
        """
        Busca un producto por su código (ID en BD).
        Retorna None si no existe.
        """
        fila = self._con.execute(
            "SELECT * FROM productos WHERE id = ?",
            (codigo,)
        ).fetchone()
        return self._fila_a_producto(fila) if fila else None

    def buscar_por_nombre(self, nombre: str) -> Optional[Producto]:
        """
        Busca un producto por nombre ignorando mayúsculas y espacios.

        LOWER() en SQL hace lo mismo que .lower() en Python.
        REPLACE() elimina los espacios — mismo comportamiento que
        la versión en memoria.

        Usa el índice idx_productos_nombre para búsqueda rápida.
        """
        nombre_normalizado = nombre.lower().replace(" ", "")
        fila = self._con.execute(
            """
            SELECT * FROM productos
            WHERE LOWER(REPLACE(nombre, ' ', '')) = ?
            """,
            (nombre_normalizado,)
        ).fetchone()
        return self._fila_a_producto(fila) if fila else None

    def obtener_todos(self) -> list[Producto]:
        """Retorna todos los productos ordenados por ID."""
        filas = self._con.execute(
            "SELECT * FROM productos ORDER BY id"
        ).fetchall()
        return [self._fila_a_producto(f) for f in filas]

    def obtener_disponibles(self) -> list[Producto]:
        """Retorna solo los productos disponibles."""
        filas = self._con.execute(
            "SELECT * FROM productos WHERE disponibilidad = 'Disponible' ORDER BY id"
        ).fetchall()
        return [self._fila_a_producto(f) for f in filas]

    def eliminar(self, codigo: int) -> bool:
        """Elimina un producto por su código."""
        cursor = self._con.execute(
            "DELETE FROM productos WHERE id = ?",
            (codigo,)
        )
        self._con.commit()
        return cursor.rowcount > 0

    # -------------------------------------------------------------------------
    # ACTUALIZACIÓN
    # -------------------------------------------------------------------------

    def actualizar(self, producto: Producto) -> None:
        """
        Guarda los cambios de un producto existente en la BD.

        En la versión en memoria esto no era necesario — modificar
        el objeto en Python modificaba directamente la lista.
        Con SQLite, modificar el objeto Python NO afecta la BD.
        Hay que hacer un UPDATE explícito.

        El service llama a este método después de editar un producto.
        """
        self._con.execute(
            """
            UPDATE productos
            SET nombre         = ?,
                precio         = ?,
                categoria      = ?,
                stock          = ?,
                disponibilidad = ?
            WHERE id = ?
            """,
            (producto.nombre, producto.precio, producto.categoria,
             producto.stock, producto.disponibilidad, producto.codigo)
        )
        self._con.commit()

    # -------------------------------------------------------------------------
    # VERIFICACIONES DE EXISTENCIA
    # -------------------------------------------------------------------------

    def nombre_existe(self, nombre: str) -> bool:
        """Verifica si ya existe un producto con ese nombre."""
        nombre_normalizado = nombre.lower().replace(" ", "")
        fila = self._con.execute(
            """
            SELECT 1 FROM productos
            WHERE LOWER(REPLACE(nombre, ' ', '')) = ?
            """,
            (nombre_normalizado,)
        ).fetchone()
        return fila is not None

    def total_productos(self) -> int:
        """Retorna la cantidad de productos en el inventario."""
        fila = self._con.execute(
            "SELECT COUNT(*) FROM productos"
        ).fetchone()
        return fila[0]

    def inventario_vacio(self) -> bool:
        """Retorna True si no hay productos registrados."""
        return self.total_productos() == 0

    # -------------------------------------------------------------------------
    # CONVERSIÓN FILA → OBJETO
    # -------------------------------------------------------------------------

    def _fila_a_producto(self, fila) -> Producto:
        """
        Convierte una fila de la tabla 'productos' en un objeto Producto.
        El campo 'id' de la BD se mapea a 'codigo' del modelo.
        """
        p = Producto(
            codigo    = fila["id"],
            nombre    = fila["nombre"],
            precio    = fila["precio"],
            categoria = fila["categoria"],
            stock     = fila["stock"]
        )
        # Asignamos disponibilidad directamente porque el constructor
        # siempre la inicializa como 'Disponible' — necesitamos el valor real
        p.disponibilidad = fila["disponibilidad"]
        return p