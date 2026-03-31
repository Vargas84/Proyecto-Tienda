from Modelos.productos import Productos
from Modelos.cliente import Cliente


class DetalleVenta:
    """Esta clase guarda la información de lo que quieres vender
    sin afectar el objeto Producto original todavía"""
    def __init__(self,id_detalle_ventas,objeto_producto,cantidad_vender):
        #identificador unico de cada detalleVenta
        #cada producto dentro de la venta
        self.id_detalle_ventas=id_detalle_ventas
        
        #referencia al objeto Producto que se esta vendiendo
        #atravez de este objeto se accede al nombre, precio, stock, etc
        self.objeto_producto=objeto_producto
        
        #cantidad de unidades a vender de este producto
        self.cantidad_vender=cantidad_vender
        
        #precio de venta se obtiene directamente del objeto producto
        #es el atributo precio que se encuentra en el inventario
        self.precio_venta=objeto_producto.precio
        
        
        #este es el total de cada producto 
        #cantidad vendida x el precio de venta para el sub total de cada producto
        #dentro de cada factura esto se representa para cada producto
        self.subtotal=cantidad_vender*self.precio_venta