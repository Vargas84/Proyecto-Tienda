# =============================================================================
# services/venta_service.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Contiene toda la lógica de negocio de las facturas de venta:
#   - Iniciar una factura de venta
#   - Agregar productos disponibles del inventario
#   - Editar cantidad de productos en la factura
#   - Eliminar productos de la factura
#   - Confirmar la venta (descontar stock, guardar factura)
#   - Cancelar la venta
#   - Consultar facturas guardadas
#
# ANTES: esta lógica estaba en elif opcion_gestion == 3, con el mismo
# patrón de banderas booleanas, while True anidados y lógica mezclada
# con print() e input().
#
# PRINCIPIOS APLICADOS:
#   SRP, DIP — mismo patrón que CompraService
# =============================================================================

from datetime import datetime
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.cliente import Cliente
from models.producto import Producto
from repositories.venta_repository import VentaRepository
from repositories.producto_repository import ProductoRepository
from exceptions.app_exceptions import (
    FacturaVaciaError,
    ProductoDuplicadoEnFacturaError,
    ProductoNoEncontradoError,
    ProductoNoDisponibleError,
    StockInsuficienteError,
)


class VentaService:
    """
    Servicio de gestión de facturas de venta.
    Coordina la creación, edición y confirmación de ventas,
    y descuenta el stock del inventario al confirmar.
    """

    def __init__(self, venta_repo,
                 producto_repo):  # acepta en memoria o SQL
        self._venta_repo   = venta_repo
        self._producto_repo = producto_repo
        self._factura_actual: Venta | None = None

    # -------------------------------------------------------------------------
    # CICLO DE VIDA DE UNA FACTURA DE VENTA
    # -------------------------------------------------------------------------

    def iniciar_factura(self) -> Venta:
        """
        Crea una nueva factura de venta y la deja como activa.
        ANTES: id_venta = inventario.generar_id_venta()
               factura_venta = Ventas(id_venta)
               inventario.detalle_venta_id = 1
        """
        self._venta_repo.reiniciar_contador_detalle()
        id_venta = self._venta_repo.generar_id_venta()
        self._factura_actual = Venta(id_venta)
        return self._factura_actual

    def cancelar_factura(self) -> None:
        """
        Cancela la factura activa y libera su ID.
        ANTES: inventario.liberar_id_venta() inline en el controlador.
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        self._venta_repo.liberar_id_venta()
        self._factura_actual = None

    def confirmar_factura(self, cliente: Cliente) -> Venta:
        """
        Confirma la factura de venta, descuenta stock y la guarda.

        ANTES: este bloque era elif op_confir_venta == 2, con un for
        anidado buscando cada producto en inventario.lista_productos
        para descontar stock, todo mezclado con print() e input().

        Pasos:
          1. Verifica que la factura tenga productos
          2. Asigna fecha y cliente
          3. Descuenta el stock de cada producto vendido
          4. Marca como No Disponible si el stock llega a 0
          5. Guarda la factura confirmada

        Parámetros:
            cliente (Cliente): objeto cliente ya creado por la UI

        Retorna:
            Venta: la factura confirmada y guardada

        Lanza:
            FacturaVaciaError: si no hay productos en la factura
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None

        if len(self._factura_actual.productos_vendidos) == 0:
            raise FacturaVaciaError(
                "No puedes confirmar una venta sin productos"
            )

        # Asignamos fecha y cliente
        self._factura_actual.fecha   = datetime.now().strftime(
            '%d/%m/%Y %H:%M:%S'
        )
        self._factura_actual.cliente = cliente

        # Descontamos el stock de cada producto vendido.
        # disminuir_stock() está en el modelo Producto y maneja
        # automáticamente el cambio a No Disponible si stock llega a 0.
        # ANTES: este for estaba en el controlador con un for anidado
        # buscando cada producto en inventario.lista_productos.
        for detalle in self._factura_actual.productos_vendidos:
            detalle.objeto_producto.disminuir_stock(detalle.cantidad_vender)
            # Persistimos el descuento de stock en la BD si el repo lo soporta
            if hasattr(self._producto_repo, 'actualizar'):
                self._producto_repo.actualizar(detalle.objeto_producto)  # type: ignore[union-attr]

        # Cerramos la factura
        self._factura_actual.calcular_total()
        self._factura_actual.venta_confirmada = True

        # Guardamos
        self._venta_repo.guardar(self._factura_actual)
        factura_guardada = self._factura_actual
        self._factura_actual = None

        return factura_guardada

    # -------------------------------------------------------------------------
    # GESTIÓN DE PRODUCTOS EN LA FACTURA ACTIVA
    # -------------------------------------------------------------------------

    def agregar_producto_a_factura(self, nombre_buscado: str,
                                   cantidad: int) -> DetalleVenta:
        """
        Agrega un producto del inventario a la factura de venta activa.

        A diferencia de compras, en ventas solo se pueden agregar
        productos que ya existen en el inventario, están disponibles
        y tienen stock suficiente.

        ANTES: este bloque tenía 4 verificaciones separadas con
        if/continue, luego otro bloque para la cantidad, todo inline.

        Parámetros:
            nombre_buscado (str): nombre del producto a vender
            cantidad (int): unidades a vender

        Retorna:
            DetalleVenta: el detalle creado y agregado

        Lanza:
            ProductoNoEncontradoError: si no existe en inventario
            ProductoDuplicadoEnFacturaError: si ya está en esta factura
            ProductoNoDisponibleError: si está marcado No Disponible
            StockInsuficienteError: si la cantidad supera el stock
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        self._verificar_no_duplicado(nombre_buscado)

        # Verificamos que el producto exista en el inventario
        producto = self._producto_repo.buscar_por_nombre(nombre_buscado)
        if producto is None:
            raise ProductoNoEncontradoError(
                f"'{nombre_buscado}' no existe en el inventario. "
                "Solo se pueden vender productos registrados"
            )

        # Verificamos disponibilidad
        if not producto.esta_disponible():
            raise ProductoNoDisponibleError(
                f"'{producto.nombre}' no está disponible para la venta"
            )

        # Verificamos stock suficiente
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente. Solo hay {producto.stock} "
                f"unidades de '{producto.nombre}'"
            )

        # Creamos el detalle
        id_detalle = self._venta_repo.generar_id_detalle()
        detalle = DetalleVenta(id_detalle, producto, cantidad)

        assert self._factura_actual is not None
        self._factura_actual.agregar_detalle(detalle)
        return detalle

    def editar_cantidad_detalle(self, id_detalle: int,
                                nueva_cantidad: int) -> DetalleVenta:
        """
        Actualiza la cantidad a vender de un producto en la factura.

        Verifica que la nueva cantidad no supere el stock disponible.

        ANTES: elif op_factura_venta == 4, con verificación de stock
        y recálculo de subtotal inline.

        Lanza:
            ProductoNoEncontradoError: si no existe el detalle
            StockInsuficienteError: si la cantidad supera el stock
        """
        detalle = self._buscar_detalle(id_detalle)

        if nueva_cantidad > detalle.objeto_producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente. Solo hay "
                f"{detalle.objeto_producto.stock} unidades de "
                f"'{detalle.objeto_producto.nombre}'"
            )

        detalle.cantidad_vender = nueva_cantidad
        detalle.recalcular_subtotal()
        assert self._factura_actual is not None
        self._factura_actual.calcular_total()
        return detalle

    def eliminar_detalle(self, id_detalle: int) -> tuple[bool, bool]:
        """
        Elimina un producto de la factura de venta activa.

        Igual que en CompraService: si queda vacía, se cancela
        automáticamente.

        Retorna:
            tuple (eliminado: bool, factura_cancelada: bool)

        Lanza:
            ProductoNoEncontradoError: si no existe el detalle
        """
        detalle = self._buscar_detalle(id_detalle)
        assert self._factura_actual is not None
        self._factura_actual.productos_vendidos.remove(detalle)
        self._factura_actual.calcular_total()

        if len(self._factura_actual.productos_vendidos) == 0:
            self._venta_repo.liberar_id_venta()
            self._factura_actual = None
            return True, True

        return True, False

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def obtener_factura_actual(self) -> Venta | None:
        """Retorna la factura de venta en proceso, o None."""
        return self._factura_actual

    def obtener_todas_las_ventas(self) -> list:
        """Retorna todas las facturas de venta confirmadas."""
        return self._venta_repo.obtener_todos()

    def buscar_ventas_por_mes(self, mes: int, anio: int) -> list:
        """
        Filtra ventas confirmadas por mes y año.
        ANTES: el filtro estaba inline en el controlador bajo
        elif op_buscar_ventas == 1.
        """
        return self._venta_repo.buscar_por_mes_anio(mes, anio)

    def hay_ventas(self) -> bool:
        """Retorna True si hay al menos una venta guardada."""
        return self._venta_repo.hay_ventas()

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE APOYO
    # -------------------------------------------------------------------------

    def _buscar_detalle(self, id_detalle: int) -> DetalleVenta:
        """Busca un detalle en la factura activa. Lanza si no existe."""
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        for detalle in self._factura_actual.productos_vendidos:
            if detalle.id_detalle_ventas == id_detalle:
                return detalle
        raise ProductoNoEncontradoError(
            f"No existe un producto con código {id_detalle} en la factura"
        )

    def _verificar_factura_activa(self) -> None:
        """Lanza ValueError si no hay factura en proceso."""
        if self._factura_actual is None:
            raise ValueError("No hay una factura de venta activa")

    def _verificar_no_duplicado(self, nombre: str) -> None:
        """
        Lanza ProductoDuplicadoEnFacturaError si el producto ya está
        en la factura activa.
        """
        assert self._factura_actual is not None
        nombre_normalizado = nombre.lower().replace(" ", "")
        for detalle in self._factura_actual.productos_vendidos:
            if detalle.objeto_producto.nombre.lower().replace(
                " ", ""
            ) == nombre_normalizado:
                raise ProductoDuplicadoEnFacturaError(
                    f"'{nombre}' ya fue agregado a esta factura. "
                    "No pueden existir productos duplicados"
                )