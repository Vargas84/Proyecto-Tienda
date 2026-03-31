from datetime import datetime 
from Modelos.cliente import Cliente


class Ventas:
    def __init__(self,codigo_venta):
        self.codigo_venta=codigo_venta #identificador unico de la venta
        self.cliente=None #usuario (empleado) que registra la venta se conecta con la clase Usuario
        self.fecha=None #fecha automatica, se agrega al momento de confirmar la venta
        self.productos_vendidos=[]# lista de productos vendidos en esta venta(detalleVentas)
        self.total_venta=0 #total acumulado de la venta(suma de los subtotales de los detallesVenta)
        self.venta_confirmada=False #se cambia el estado de la venta cuando se confirma la factura(True)
        
    
    def agregar_detalle(self, detalle):
        #agrega un objeto detalleVenta a la lista de detalles
        #es como escribir una fila nueva en la factura
        self.productos_vendidos.append(detalle)