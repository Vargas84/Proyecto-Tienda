# =============================================================================
# services/producto_service.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA VERSIÓN ANTERIOR?
#
# Con la versión en memoria, modificar un atributo del objeto Producto
# era suficiente porque el objeto vivía en la lista del repository.
#
# Con SQLite, modificar el objeto Python NO afecta la base de datos.
# Hay que hacer un UPDATE explícito llamando a repo.actualizar(producto).
#
# SOLUCIÓN: cada método de edición ahora llama a _persistir(producto)
# al final, que invoca actualizar() si el repository lo soporta.
# Si el repository no tiene actualizar() (versión en memoria), simplemente
# no hace nada — así el mismo service funciona con ambos storages.
# =============================================================================

from models.producto import Producto
from repositories.producto_repository import ProductoRepository
from exceptions.app_exceptions import (
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)


class ProductoService:
    """
    Servicio de gestión del inventario de productos.
    Coordina las operaciones sobre productos aplicando
    las reglas de negocio del sistema.
    """

    def __init__(self, producto_repo):  # acepta en memoria o SQL
        self._producto_repo = producto_repo

    # -------------------------------------------------------------------------
    # AGREGAR PRODUCTO
    # -------------------------------------------------------------------------

    def agregar_producto(self, nombre: str, precio: float,
                         categoria: str, stock: int) -> Producto:
        """
        Crea y registra un producto nuevo en el inventario.
        Con SQLite, guardar() hace el INSERT y asigna el ID real.
        """
        id_nuevo = self._producto_repo.generar_id()
        nuevo_producto = Producto(id_nuevo, nombre, precio, categoria, stock)
        self._producto_repo.guardar(nuevo_producto)
        return nuevo_producto

    # -------------------------------------------------------------------------
    # CAMBIAR DISPONIBILIDAD
    # -------------------------------------------------------------------------

    def cambiar_disponibilidad(self, codigo: int) -> Producto:
        """
        Alterna la disponibilidad entre 'Disponible' y 'No Disponible'.
        Persiste el cambio en la BD con _persistir().
        """
        producto = self._obtener_o_lanzar(codigo)
        producto.cambiar_disponibilidad()
        # Con SQLite necesitamos persistir el cambio explícitamente.
        # Con la versión en memoria _persistir() no hace nada.
        self._persistir(producto)
        return producto

    # -------------------------------------------------------------------------
    # EDITAR PRODUCTO
    # -------------------------------------------------------------------------

    def editar_nombre(self, codigo: int, nuevo_nombre: str) -> Producto:
        """Cambia el nombre verificando que no esté duplicado. Persiste."""
        producto = self._obtener_o_lanzar(codigo)

        nombre_normalizado = nuevo_nombre.lower().replace(" ", "")
        nombre_actual = producto.nombre.lower().replace(" ", "")

        if nombre_normalizado != nombre_actual:
            existente = self._producto_repo.buscar_por_nombre(nuevo_nombre)
            if existente is not None and existente.codigo != codigo:
                raise ProductoYaExisteError(
                    f"Ya existe un producto con el nombre '{nuevo_nombre}'"
                )

        producto.nombre = nuevo_nombre
        self._persistir(producto)
        return producto

    def editar_precio(self, codigo: int, nuevo_precio: float) -> Producto:
        """Actualiza el precio de venta. Persiste en BD."""
        producto = self._obtener_o_lanzar(codigo)
        producto.precio = nuevo_precio
        self._persistir(producto)
        return producto

    def editar_stock(self, codigo: int, nuevo_stock: int) -> Producto:
        """Reemplaza el stock y sincroniza disponibilidad. Persiste en BD."""
        producto = self._obtener_o_lanzar(codigo)
        producto.stock = nuevo_stock

        if nuevo_stock <= 0:
            producto.disponibilidad = Producto.NO_DISPONIBLE
        else:
            producto.disponibilidad = Producto.DISPONIBLE

        self._persistir(producto)
        return producto

    def editar_categoria(self, codigo: int,
                         nueva_categoria: str) -> Producto:
        """Actualiza la categoría. Persiste en BD."""
        producto = self._obtener_o_lanzar(codigo)
        producto.categoria = nueva_categoria
        self._persistir(producto)
        return producto

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def buscar_por_id(self, codigo: int) -> Producto:
        """Retorna el producto o lanza ProductoNoEncontradoError."""
        return self._obtener_o_lanzar(codigo)

    def buscar_por_nombre(self, nombre: str) -> Producto | None:
        """Busca por nombre ignorando mayúsculas y espacios."""
        return self._producto_repo.buscar_por_nombre(nombre)

    def obtener_todos(self) -> list:
        """Retorna todos los productos del inventario."""
        return self._producto_repo.obtener_todos()

    def inventario_vacio(self) -> bool:
        """Retorna True si no hay productos registrados."""
        return self._producto_repo.inventario_vacio()

    def nombre_disponible(self, nombre: str) -> bool:
        """Retorna True si el nombre NO está en uso."""
        return not self._producto_repo.nombre_existe(nombre)

    def formatear_inventario(self) -> str:
        """Retorna el inventario formateado listo para imprimir."""
        productos = self._producto_repo.obtener_todos()

        if not productos:
            return (
                "\n" + "!" * 40 + "\n"
                "El inventario se encuentra vacío\n"
                + "!" * 40
            )

        encabezado = (
            f"\n --- INVENTARIO ---\n"
            f"{'Codigo':<10} | {'Nombre':<20} | {'Precio':<10} | "
            f"{'Stock':<10} | {'Categoría':<15} | {'Disponibilidad':<20}\n"
            + "-" * 100
        )
        filas = "\n".join(p.mostrar_informacion() for p in productos)
        return encabezado + "\n" + filas

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS
    # -------------------------------------------------------------------------

    def _obtener_o_lanzar(self, codigo: int) -> Producto:
        """Busca por ID. Si no existe, lanza ProductoNoEncontradoError."""
        producto = self._producto_repo.buscar_por_id(codigo)
        if producto is None:
            raise ProductoNoEncontradoError(
                f"No existe un producto con el código {codigo}"
            )
        return producto

    def _persistir(self, producto: Producto) -> None:
        """
        Llama a actualizar() si el repository lo implementa.

        Con SQLite: ProductoRepositorySQL.actualizar() hace el UPDATE.
        Con memoria: ProductoRepository no tiene actualizar(),
                     así que hasattr retorna False y no hace nada.

        Este patrón se llama "duck typing" — no nos importa el tipo
        concreto del repository, solo si tiene el método que necesitamos.
        """
        if hasattr(self._producto_repo, 'actualizar'):
            self._producto_repo.actualizar(producto)  # type: ignore[union-attr]