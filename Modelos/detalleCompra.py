from Modelos.productos import Productos
from Modelos.proveedores import Proveedor


class DetalleCompra:
    """
    Esta clase guarda la información de lo que quieres comprar
    sin afectar el objeto Producto original todavía.
    """
    def __init__(self, objeto_producto, cantidad_compra, precio_compra, precio_venta_nuevo):
        self.producto = objeto_producto      # Referencia al objeto Producto (real o nuevo)
        #estos atributos son unicos en esta factura. No se guardan en el producto permamente hasta que
        #el usuario confirme
        self.cantidad_compra = cantidad_compra          # Cantidad a comprar
        self.precio_compra = precio_compra # Costo de esta compra
        
        #este seria el nuevo precio de venta al publico
        self.precio_venta_nuevo = precio_venta_nuevo # Nuevo precio sugerido
        
        #se calcula el subtotal al momento de crear este objeto
        self.subtotal = cantidad_compra * precio_compra #total de ese producto