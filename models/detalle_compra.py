# =============================================================================
# models/detalle_compra.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL: la clase importaba Proveedor y Productos aunque
# no los usaba en __init__ — eran imports innecesarios que generan
# acoplamiento sin beneficio.
#
# CORRECCIONES:
#   1. Se eliminaron los imports innecesarios (Proveedor, Productos).
#      DetalleCompra recibe el objeto producto ya construido — no necesita
#      importar la clase para eso.
#   2. Se agrega el atributo 'es_nuevo' directamente en __init__ con valor
#      por defecto False. Antes se añadía "desde afuera" con
#      detalle.es_nuevo = True, lo cual es frágil porque si alguien olvida
#      asignarlo el atributo no existe y lanza AttributeError.
#   3. Se agrega __repr__ para depuración.
#   4. Nombre del archivo en snake_case (detalle_compra.py).
#
# PRINCIPIO APLICADO: SRP — esta clase solo representa UNA línea
# dentro de una factura de compra. No coordina nada.
# =============================================================================


class DetalleCompra:
    """
    Representa una línea (un producto) dentro de una factura de compra.
    
    Atributos:
        id_detalle (int): identificador único del detalle dentro de la factura.
        producto: objeto Producto asociado (real o temporal si es nuevo).
        cantidad_compra (int): unidades compradas de ese producto.
        precio_compra (float): precio unitario al que se compró al proveedor.
        precio_venta_nuevo (float): precio al que se venderá al público.
        subtotal (float): total de este detalle (cantidad * precio_compra).
        es_nuevo (bool): True si el producto no existía en inventario,
                         False si ya estaba registrado.
    """

    def __init__(self, id_detalle: int, producto, cantidad_compra: int,
                 precio_compra: float, precio_venta_nuevo: float,
                 es_nuevo: bool = False):
        self.id_detalle        = id_detalle
        self.producto          = producto
        self.cantidad_compra   = cantidad_compra
        self.precio_compra     = precio_compra
        self.precio_venta_nuevo = precio_venta_nuevo

        # Calculamos el subtotal al crear el objeto.
        # Si se edita la cantidad o el precio después, hay que recalcularlo
        # llamando a recalcular_subtotal().
        self.subtotal = cantidad_compra * precio_compra

        # CAMBIO CLAVE: antes esto se asignaba desde afuera después de crear
        # el objeto (detalle.es_nuevo = True), lo cual es frágil.
        # Ahora es un parámetro del constructor con valor por defecto False.
        self.es_nuevo = es_nuevo

    def recalcular_subtotal(self):
        """
        Recalcula el subtotal cuando se edita la cantidad o el precio de compra.
        Antes este cálculo se repetía inline en el controlador cada vez
        que se editaba un campo. Ahora está centralizado aquí.
        
        Uso:
            detalle.cantidad_compra = nueva_cantidad
            detalle.recalcular_subtotal()
        """
        self.subtotal = self.cantidad_compra * self.precio_compra

    def __repr__(self) -> str:
        return (
            f"DetalleCompra(id={self.id_detalle}, "
            f"producto='{self.producto.nombre}', "
            f"cantidad={self.cantidad_compra}, "
            f"subtotal={self.subtotal})"
        )