# =============================================================================
# services/producto_service.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Contiene toda la lógica de negocio del inventario:
#   - Agregar productos nuevos
#   - Cambiar disponibilidad
#   - Editar atributos (nombre, precio, stock, categoría)
#   - Mostrar el inventario formateado
#   - Buscar productos
#
# ANTES: esta lógica estaba repartida entre:
#   - El bloque if opcion_inventario == 1,2,3,4 del controlador
#   - Los métodos de la clase Usuarios (agregar_productos,
#     editar_productos, cambiar_disponibilidad_producto)
#   - La clase Inventario (mostrar_inventario, buscar_producto_id)
#
# AHORA todo en un solo lugar coherente.
#
# PRINCIPIO APLICADO:
#   SRP — este service tiene una sola razón de cambiar: cuando cambian
#   las reglas de negocio del inventario de productos.
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

    def __init__(self, producto_repo: ProductoRepository):
        # Inyección de dependencia: el service recibe el repo,
        # no lo crea. Esto permite cambiar el almacenamiento sin
        # tocar la lógica de negocio.
        self._producto_repo = producto_repo

    # -------------------------------------------------------------------------
    # AGREGAR PRODUCTO
    # -------------------------------------------------------------------------

    def agregar_producto(self, nombre: str, precio: float,
                         categoria: str, stock: int) -> Producto:
        """
        Crea y registra un producto nuevo en el inventario.

        ANTES: esta lógica estaba en if opcion_inventario == 1,
        con validaciones inline y la llamada a trabajador.agregar_productos().

        Parámetros:
            nombre (str): nombre del producto (ya validado por la UI)
            precio (float): precio de venta (ya validado)
            categoria (str): categoría (ya validada)
            stock (int): stock inicial (ya validado)

        Retorna:
            Producto: el objeto creado con su ID asignado

        Lanza:
            ProductoYaExisteError: si ya existe un producto con ese nombre
        """
        # Generamos el ID aquí — el repository es dueño de los IDs
        id_nuevo = self._producto_repo.generar_id()

        nuevo_producto = Producto(id_nuevo, nombre, precio, categoria, stock)

        # guardar() verifica duplicados de nombre y lanza
        # ProductoYaExisteError si encuentra uno
        self._producto_repo.guardar(nuevo_producto)

        return nuevo_producto

    # -------------------------------------------------------------------------
    # CAMBIAR DISPONIBILIDAD
    # -------------------------------------------------------------------------

    def cambiar_disponibilidad(self, codigo: int) -> Producto:
        """
        Alterna la disponibilidad de un producto entre
        'Disponible' y 'No Disponible'.

        ANTES: trabajador.cambiar_disponibilidad_producto(inventario, codigo)
        con un bucle for inline en la clase Usuarios.

        Parámetros:
            codigo (int): ID del producto a modificar

        Retorna:
            Producto: el objeto actualizado (para que la UI muestre
                      el nuevo estado)

        Lanza:
            ProductoNoEncontradoError: si no existe producto con ese ID
        """
        producto = self._obtener_o_lanzar(codigo)
        # cambiar_disponibilidad() está en el modelo — es una operación
        # propia del producto, no lógica de negocio externa
        producto.cambiar_disponibilidad()
        return producto

    # -------------------------------------------------------------------------
    # EDITAR PRODUCTO
    # -------------------------------------------------------------------------

    def editar_nombre(self, codigo: int, nuevo_nombre: str) -> Producto:
        """
        Cambia el nombre de un producto.

        Verifica que el nuevo nombre no esté en uso por otro producto.

        ANTES: trabajador.editar_productos(inventario, id_p, nuevo_nombre=x)
        con la validación de duplicados inline en el controlador.

        Lanza:
            ProductoNoEncontradoError: si no existe el producto
            ProductoYaExisteError: si el nuevo nombre ya está en uso
        """
        producto = self._obtener_o_lanzar(codigo)

        # Verificamos duplicado solo si el nombre realmente cambió
        nombre_normalizado = nuevo_nombre.lower().replace(" ", "")
        nombre_actual = producto.nombre.lower().replace(" ", "")

        if nombre_normalizado != nombre_actual:
            # Buscamos si existe otro producto con ese nombre
            existente = self._producto_repo.buscar_por_nombre(nuevo_nombre)
            if existente is not None and existente.codigo != codigo:
                raise ProductoYaExisteError(
                    f"Ya existe un producto con el nombre '{nuevo_nombre}'"
                )

        producto.nombre = nuevo_nombre
        return producto

    def editar_precio(self, codigo: int, nuevo_precio: float) -> Producto:
        """
        Actualiza el precio de venta de un producto.

        Lanza:
            ProductoNoEncontradoError: si no existe el producto
        """
        producto = self._obtener_o_lanzar(codigo)
        producto.precio = nuevo_precio
        return producto

    def editar_stock(self, codigo: int, nuevo_stock: int) -> Producto:
        """
        Actualiza el stock de un producto directamente.
        (Distinto de aumentar/disminuir — este reemplaza el valor.)

        Lanza:
            ProductoNoEncontradoError: si no existe el producto
        """
        producto = self._obtener_o_lanzar(codigo)
        producto.stock = nuevo_stock

        # Sincronizamos la disponibilidad con el nuevo stock
        if nuevo_stock <= 0:
            producto.disponibilidad = Producto.NO_DISPONIBLE
        else:
            producto.disponibilidad = Producto.DISPONIBLE

        return producto

    def editar_categoria(self, codigo: int,
                         nueva_categoria: str) -> Producto:
        """
        Actualiza la categoría de un producto.

        Lanza:
            ProductoNoEncontradoError: si no existe el producto
        """
        producto = self._obtener_o_lanzar(codigo)
        producto.categoria = nueva_categoria
        return producto

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def buscar_por_id(self, codigo: int) -> Producto:
        """
        Retorna el producto con ese código.

        ANTES: inventario.buscar_producto_id(id_p) retornaba None
        y el controlador verificaba manualmente con if producto is None.

        AHORA: lanza excepción directamente — la UI solo necesita
        hacer try/except, sin verificar None.

        Lanza:
            ProductoNoEncontradoError: si no existe
        """
        return self._obtener_o_lanzar(codigo)

    def buscar_por_nombre(self, nombre: str) -> Producto | None:
        """
        Busca un producto por nombre ignorando mayúsculas y espacios.
        Retorna None si no existe (sin lanzar excepción).
        Útil para las compras donde buscamos si ya existe el producto.
        """
        return self._producto_repo.buscar_por_nombre(nombre)

    def obtener_todos(self) -> list:
        """
        Retorna todos los productos del inventario.
        ANTES: inventario.lista_productos (acceso directo).
        """
        return self._producto_repo.obtener_todos()

    def inventario_vacio(self) -> bool:
        """Retorna True si no hay productos registrados."""
        return self._producto_repo.inventario_vacio()

    def nombre_disponible(self, nombre: str) -> bool:
        """
        Retorna True si el nombre NO está en uso.
        Útil para validar desde la UI antes de pedir más datos.
        """
        return not self._producto_repo.nombre_existe(nombre)

    def formatear_inventario(self) -> str:
        """
        Retorna el inventario completo como string formateado,
        listo para imprimir.

        ANTES: inventario.mostrar_inventario() hacía print() directamente.
        AHORA: el service construye el texto y la UI decide cómo mostrarlo.
        Esto permite reutilizar el formato en otros contextos si se necesita.
        """
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
    # MÉTODO PRIVADO DE APOYO
    # -------------------------------------------------------------------------

    def _obtener_o_lanzar(self, codigo: int) -> Producto:
        """
        Busca un producto por ID. Si no existe, lanza excepción.

        Es un método privado (prefijo _) de uso interno del service.
        Evita repetir el mismo patrón buscar → verificar None → lanzar
        en cada método público.

        Lanza:
            ProductoNoEncontradoError: si no existe producto con ese ID
        """
        producto = self._producto_repo.buscar_por_id(codigo)
        if producto is None:
            raise ProductoNoEncontradoError(
                f"No existe un producto con el código {codigo}"
            )
        return producto