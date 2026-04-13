# =============================================================================
# models/detalle_venta.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL: importaba Cliente y Productos sin usarlos.
#
# CORRECCIONES:
#   1. Se eliminaron los imports innecesarios.
#   2. Se agrega recalcular_subtotal() igual que en DetalleCompra,
#      porque el controlador también recalculaba inline al editar cantidad.
#   3. Se agrega __repr__.
#   4. Nombre del archivo en snake_case (detalle_venta.py).
#
# PRINCIPIO APLICADO: SRP — representa una línea de factura de venta.
# =============================================================================


class DetalleVenta:
    """
    Representa una línea (un producto) dentro de una factura de venta.
    
    Atributos:
        id_detalle_ventas (int): identificador único del detalle.
        objeto_producto: referencia al objeto Producto que se vende.
        cantidad_vender (int): unidades a vender.
        precio_venta (float): precio unitario (tomado del producto).
        subtotal (float): total de este detalle (cantidad * precio_venta).
    """

    def __init__(self, id_detalle_ventas: int, objeto_producto,
                 cantidad_vender: int):
        self.id_detalle_ventas = id_detalle_ventas
        self.objeto_producto   = objeto_producto
        self.cantidad_vender   = cantidad_vender

        # El precio de venta se toma del producto en el momento de crear
        # el detalle. Así queda registrado el precio de ese instante,
        # aunque el precio del producto cambie después.
        self.precio_venta = objeto_producto.precio

        # Subtotal calculado al crear el objeto
        self.subtotal = cantidad_vender * self.precio_venta

    def recalcular_subtotal(self):
        """
        Recalcula el subtotal cuando se edita la cantidad a vender.
        Antes este cálculo aparecía inline en el controlador.
        
        Uso:
            detalle.cantidad_vender = nueva_cantidad
            detalle.recalcular_subtotal()
        """
        self.subtotal = self.cantidad_vender * self.precio_venta

    def __repr__(self) -> str:
        return (
            f"DetalleVenta(id={self.id_detalle_ventas}, "
            f"producto='{self.objeto_producto.nombre}', "
            f"cantidad={self.cantidad_vender}, "
            f"subtotal={self.subtotal})"
        )