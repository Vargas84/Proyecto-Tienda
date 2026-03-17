#importamos datetime para registrar automaticamente la fecha y hora de la compra
from datetime import datetime
#Importamos la clase DetalleCompra
#Esta clase representa cada producto individual dentro de una compra
from Modelos.productos import Productos
from Modelos.proveedores import Proveedor

class Compra:
    #esta clase representa la factura completa
    #actua como organizador antes de enviar los productos al inventario definitivo
    def __init__(self, id_factura):
        self.id_factura = id_factura#identificador unico de esta factura
        
        # 2. Objeto Proveedor:
        # Se deja en None al inicio y se llena cuando registras el proveedor.
        # Guardar el objeto permite acceder a self.proveedor.nombre, etc.
        self.proveedor = None      # Objeto Proveedor
        
        # Aquí se guardan todos los objetos 'DetalleCompra' que el usuario ingresa.
        # Es una lista de objetos, no de diccionarios.
        self.lista_detalles = []   # Lista de objetos 'DetalleCompra'
        
        #incia en 0 y crece cada vez que agregas un producto nuevo
        self.total_factura = 0

        self.factura_confirmada = False  #  inicia en False y cambia a True al confirmarse la compra


        self.fecha_hora=None #empieza en None y se llena al confirmar la compra



    def agregar_detalle(self, detalle_obj):
        #esta funcion hace dos cosas al mismo tiempo
        #g1 guardar el detalle en la lista de la factura
        self.lista_detalles.append(detalle_obj)
        
        #2 suma el subtotal de cada detalle de compra a la de la factura
        self.total_factura += detalle_obj.subtotal
        
        
    
        
        
        
        
        