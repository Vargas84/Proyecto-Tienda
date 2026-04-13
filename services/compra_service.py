# =============================================================================
# services/compra_service.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Contiene toda la lógica de negocio de las facturas de compra:
#   - Iniciar una factura nueva
#   - Agregar productos a la factura (nuevos o existentes en inventario)
#   - Editar y eliminar productos dentro de la factura
#   - Confirmar la factura (actualizar inventario, guardar)
#   - Cancelar la factura
#   - Consultar facturas guardadas
#
# ANTES: toda esta lógica estaba dentro del bloque elif opcion_gestion == 2
# del controlador, anidada en 10+ niveles de indentación con banderas
# booleanas (factura_confirmada, factura_cancelada) para controlar el flujo.
#
# AHORA: métodos claros y separados. Cada uno hace una sola cosa.
#
# PRINCIPIOS APLICADOS:
#   SRP — este service solo maneja compras
#   DIP — depende de repositorios abstractos, no de listas concretas
# =============================================================================

from datetime import datetime
from models.compra import Compra
from models.detalle_compra import DetalleCompra
from models.proveedor import Proveedor
from models.producto import Producto
from repositories.compra_repository import CompraRepository
from repositories.producto_repository import ProductoRepository
from exceptions.app_exceptions import (
    FacturaVaciaError,
    FacturaYaConfirmadaError,
    ProductoDuplicadoEnFacturaError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)


class CompraService:
    """
    Servicio de gestión de facturas de compra.

    Coordina la creación, edición y confirmación de facturas,
    y actualiza el inventario cuando una compra se confirma.
    """

    def __init__(self, compra_repo: CompraRepository,
                 producto_repo: ProductoRepository):
        # Recibe DOS repositories porque las compras afectan tanto
        # las facturas como el inventario de productos.
        self._compra_repo   = compra_repo
        self._producto_repo = producto_repo

        # Factura actualmente en proceso (antes era la variable local
        # 'factura' dentro del while True del controlador)
        self._factura_actual: Compra | None = None

    # -------------------------------------------------------------------------
    # CICLO DE VIDA DE UNA FACTURA
    # -------------------------------------------------------------------------

    def iniciar_factura(self) -> Compra:
        """
        Crea una nueva factura de compra y la deja como activa.

        ANTES: id_compra = inventario.generar_id_compra()
               factura = Compra(id_compra)
               inventario.detalle_id = 1
        Todo esto estaba inline en el controlador.

        Retorna:
            Compra: la nueva factura vacía con su ID asignado
        """
        self._compra_repo.reiniciar_contador_detalle()
        id_factura = self._compra_repo.generar_id_factura()
        self._factura_actual = Compra(id_factura)
        return self._factura_actual

    def cancelar_factura(self) -> None:
        """
        Cancela la factura actual y libera su ID.

        ANTES: inventario.liberar_id_compra() + print('\nCompra cancelada.')
        El print ahora le corresponde a la UI.

        Lanza:
            ValueError: si no hay factura activa
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        self._compra_repo.liberar_id_factura()
        self._factura_actual = None

    def confirmar_factura(self, proveedor: Proveedor,
                          empleado_nombre: str) -> Compra:
        """
        Confirma la factura actual, actualiza el inventario y la guarda.

        Es el método más importante del service. Antes era el bloque
        elif op_confir_factura == 3, con más de 60 líneas de código
        anidado que hacía todo esto mezclado con print() y input().

        Pasos que ejecuta:
          1. Verifica que la factura tenga productos
          2. Asigna fecha, proveedor y empleado
          3. Recorre los detalles y actualiza el inventario:
             - Producto nuevo → se agrega al inventario con ID real
             - Producto existente → se suma stock y actualiza precio
          4. Marca la factura como confirmada
          5. La guarda en el repository
          6. Limpia la factura activa

        Parámetros:
            proveedor (Proveedor): objeto proveedor ya creado por la UI
            empleado_nombre (str): nombre del empleado que confirma

        Retorna:
            Compra: la factura confirmada y guardada

        Lanza:
            FacturaVaciaError: si no hay productos en la factura
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None

        if len(self._factura_actual.lista_detalles) == 0:
            raise FacturaVaciaError(
                "No puedes confirmar una compra sin productos"
            )

        # Asignamos fecha y hora de confirmación
        self._factura_actual.fecha_hora = datetime.now().strftime(
            '%d/%m/%Y %H:%M:%S'
        )
        self._factura_actual.proveedor = proveedor

        # Actualizamos el inventario según cada detalle
        for detalle in self._factura_actual.lista_detalles:
            if detalle.es_nuevo:
                self._registrar_producto_nuevo(detalle)
            else:
                self._actualizar_producto_existente(detalle)

        # Cerramos la factura
        self._factura_actual.calcular_total()
        self._factura_actual.factura_confirmada = True

        # Guardamos en el repository
        self._compra_repo.guardar(self._factura_actual)
        factura_guardada = self._factura_actual
        self._factura_actual = None

        return factura_guardada

    # -------------------------------------------------------------------------
    # GESTIÓN DE PRODUCTOS EN LA FACTURA ACTIVA
    # -------------------------------------------------------------------------

    def agregar_producto_a_factura(self, nombre_buscado: str,
                                   cantidad: int, precio_compra: float,
                                   precio_venta: float,
                                   categoria: str = "") -> DetalleCompra:
        """
        Agrega un producto a la factura activa.

        Determina automáticamente si el producto es nuevo o existente
        en el inventario y crea el DetalleCompra correspondiente.

        ANTES: este bloque ocupaba ~80 líneas en el controlador con
        dos ramas if/else completamente separadas para nuevo/existente
        y banderas booleanas (es_nuevo, encontrado_en_factura).

        Parámetros:
            nombre_buscado (str): nombre del producto a agregar
            cantidad (int): unidades a comprar
            precio_compra (float): precio al que compramos
            precio_venta (float): precio al que venderemos
            categoria (str): solo requerida si el producto es nuevo

        Retorna:
            DetalleCompra: el detalle creado y agregado a la factura

        Lanza:
            ProductoDuplicadoEnFacturaError: si ya está en la factura
            FacturaYaConfirmadaError: si la factura ya fue confirmada
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        self._verificar_no_confirmada()
        self._verificar_no_duplicado(nombre_buscado)

        # Buscamos si el producto ya existe en el inventario
        producto_existente = self._producto_repo.buscar_por_nombre(
            nombre_buscado
        )

        if producto_existente is not None:
            # Producto existente: usamos el objeto real del inventario
            producto_para_detalle = producto_existente
            es_nuevo = False
        else:
            # Producto nuevo: creamos un objeto temporal.
            # El ID es None hasta que se confirme la factura.
            # ANTES: Productos(None, producto_buscar, 0, categoria, 0)
            producto_para_detalle = Producto(
                None, nombre_buscado, 0, categoria, 0
            )
            es_nuevo = True

        # Generamos el ID del detalle
        id_detalle = self._compra_repo.generar_id_detalle()

        # Creamos el detalle con es_nuevo ya en el constructor
        # (antes se asignaba desde afuera: detalle.es_nuevo = es_nuevo)
        detalle = DetalleCompra(
            id_detalle,
            producto_para_detalle,
            cantidad,
            precio_compra,
            precio_venta,
            es_nuevo=es_nuevo
        )

        self._factura_actual.agregar_detalle(detalle)
        return detalle

    def editar_cantidad_detalle(self, id_detalle: int,
                                nueva_cantidad: int) -> DetalleCompra:
        """
        Actualiza la cantidad de un producto dentro de la factura activa
        y recalcula su subtotal.

        ANTES: esto se hacía inline en el controlador dentro de
        elif op_editar_producto == 2, asignando y recalculando manualmente.

        Lanza:
            ProductoNoEncontradoError: si no existe detalle con ese ID
        """
        detalle = self._buscar_detalle(id_detalle)
        detalle.cantidad_compra = nueva_cantidad
        detalle.recalcular_subtotal()
        assert self._factura_actual is not None
        # Recalculamos el total de la factura porque cambió un subtotal
        self._factura_actual.calcular_total()
        return detalle

    def editar_precio_compra_detalle(self, id_detalle: int,
                                     nuevo_precio: float) -> DetalleCompra:
        """
        Actualiza el precio de compra de un detalle y recalcula subtotal.
        """
        detalle = self._buscar_detalle(id_detalle)
        detalle.precio_compra = nuevo_precio
        detalle.recalcular_subtotal()
        assert self._factura_actual is not None
        self._factura_actual.calcular_total()
        return detalle

    def editar_precio_venta_detalle(self, id_detalle: int,
                                    nuevo_precio: float) -> DetalleCompra:
        """Actualiza el precio de venta sugerido de un detalle."""
        detalle = self._buscar_detalle(id_detalle)
        detalle.precio_venta_nuevo = nuevo_precio
        return detalle

    def editar_nombre_detalle(self, id_detalle: int,
                              nuevo_nombre: str) -> DetalleCompra:
        """
        Cambia el nombre de un producto nuevo dentro de la factura.
        Solo se permite si el producto es nuevo (es_nuevo == True).

        Lanza:
            PermissionError: si el producto ya existe en inventario
        """
        detalle = self._buscar_detalle(id_detalle)
        if not detalle.es_nuevo:
            raise PermissionError(
                "No se puede editar el nombre de un producto "
                "que ya existe en el inventario"
            )
        detalle.producto.nombre = nuevo_nombre
        return detalle

    def eliminar_detalle(self, id_detalle: int) -> tuple[bool, bool]:
        """
        Elimina un producto de la factura activa.

        ANTES: esta lógica estaba en elif op_editar_infor == 2, con
        manejo especial cuando quedaba solo un producto (cancelación
        automática) todo mezclado con print() y banderas booleanas.

        Retorna:
            tuple (eliminado: bool, factura_cancelada: bool)
            - eliminado: True si se encontró y eliminó el detalle
            - factura_cancelada: True si la factura quedó vacía
                                 y se canceló automáticamente

        Lanza:
            ProductoNoEncontradoError: si no existe detalle con ese ID
        """
        detalle = self._buscar_detalle(id_detalle)
        assert self._factura_actual is not None
        self._factura_actual.lista_detalles.remove(detalle)
        self._factura_actual.calcular_total()

        # Si la factura quedó vacía, la cancelamos automáticamente
        if len(self._factura_actual.lista_detalles) == 0:
            self._compra_repo.liberar_id_factura()
            self._factura_actual = None
            return True, True   # eliminado=True, cancelada=True

        return True, False      # eliminado=True, cancelada=False

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def obtener_factura_actual(self) -> Compra | None:
        """Retorna la factura en proceso, o None si no hay ninguna."""
        return self._factura_actual

    def obtener_todas_las_compras(self) -> list:
        """Retorna todas las facturas de compra confirmadas."""
        return self._compra_repo.obtener_todos()

    def buscar_compras_por_mes(self, mes: int, anio: int) -> list:
        """
        Filtra facturas confirmadas por mes y año.
        ANTES: este filtro estaba inline en el controlador dentro de
        elif op_ver_facturas == 1, parseando fechas manualmente.
        """
        return self._compra_repo.buscar_por_mes_anio(mes, anio)

    def hay_compras(self) -> bool:
        """Retorna True si hay al menos una factura guardada."""
        return self._compra_repo.hay_facturas()

    # -------------------------------------------------------------------------
    # MÉTODOS PRIVADOS DE APOYO
    # -------------------------------------------------------------------------

    def _registrar_producto_nuevo(self, detalle: DetalleCompra) -> None:
        """
        Registra en el inventario un producto que no existía antes.

        ANTES: este bloque estaba dentro del for de confirmación
        bajo if detalle.es_nuevo, con comentarios explicando cada paso.
        """
        # Generamos el ID real ahora que la compra está confirmada
        id_real = self._producto_repo.generar_id()
        detalle.producto.codigo = id_real
        detalle.producto.stock  = detalle.cantidad_compra
        detalle.producto.precio = detalle.precio_venta_nuevo

        # Intentamos guardarlo — si por alguna razón el nombre ya existe,
        # lanzará ProductoYaExisteError
        self._producto_repo.guardar(detalle.producto)

    def _actualizar_producto_existente(self, detalle: DetalleCompra) -> None:
        """
        Suma stock y actualiza el precio de venta de un producto existente.

        ANTES: estaba en el else del for de confirmación, con un for
        anidado buscando el producto en inventario.lista_productos.
        AHORA: usamos el método del modelo que ya tiene la lógica.
        """
        # El producto en el detalle es la referencia directa al objeto
        # en el inventario (lo encontramos al buscarlo en el repo).
        # Modificarlo aquí modifica directamente el original.
        detalle.producto.aumentar_stock(detalle.cantidad_compra)
        detalle.producto.precio = detalle.precio_venta_nuevo

    def _buscar_detalle(self, id_detalle: int) -> DetalleCompra:
        """
        Busca un detalle en la factura activa por su ID.
        Lanza excepción si no lo encuentra.
        """
        self._verificar_factura_activa()
        assert self._factura_actual is not None
        for detalle in self._factura_actual.lista_detalles:
            if detalle.id_detalle == id_detalle:
                return detalle
        raise ProductoNoEncontradoError(
            f"No existe un producto con código {id_detalle} en la factura"
        )

    def _verificar_factura_activa(self) -> None:
        """Lanza ValueError si no hay factura en proceso."""
        if self._factura_actual is None:
            raise ValueError("No hay una factura activa en este momento")

    def _verificar_no_confirmada(self) -> None:
        """Lanza FacturaYaConfirmadaError si la factura ya fue cerrada."""
        assert self._factura_actual is not None
        if self._factura_actual.factura_confirmada:
            raise FacturaYaConfirmadaError(
                "Esta factura ya fue confirmada y no puede modificarse"
            )

    def _verificar_no_duplicado(self, nombre: str) -> None:
        """
        Lanza ProductoDuplicadoEnFacturaError si el producto ya está
        en la factura activa.
        ANTES: la bandera encontrado_en_factura + bucle for inline.
        """
        nombre_normalizado = nombre.lower().replace(" ", "")
        assert self._factura_actual is not None
        for detalle in self._factura_actual.lista_detalles:
            if detalle.producto.nombre.lower().replace(
                " ", ""
            ) == nombre_normalizado:
                raise ProductoDuplicadoEnFacturaError(
                    f"'{nombre}' ya está en la factura. "
                    "No se permiten productos duplicados"
                )