#importamos datetime para registrar automaticamente la fecha y hora de la compra
from datetime import datetime
#Importamos la clase DetalleCompra
#Esta clase representa cada producto individual dentro de una compra
from Modelos.productos import Productos

#La clase compra representa una transaccion de entrada de productos
#Es decir, cuando llegan productos de proveedores
class Compra:
    #Constructor:Se ejecuta cuando se crea una nueva compra
    def __init__(self,codigo_compra,proveedor):
        self.codigo_compra=codigo_compra #identificador unico de la compra
        self.fecha=datetime.now()#fecha automatica en el momento de crear la compra
        self.total=0#total acumulado de la compra
        self.proveedor=proveedor #objeto proveedor
        self.productos_comprados=[]#lista vacia al iinicio
        
    def agregar_productos(self,producto,cantidad,costo_unitario):
        subtotal=cantidad*costo_unitario
        detalle={
            "Producto":producto, #objeto producto
            "Cantidad": cantidad,
            "Costo Unitario": costo_unitario,
            "Subtotal":subtotal
        }
        
        self.productos_comprados.append(detalle)
        self.total+=subtotal
        
    def mostrar_factura(self):
        print("Factura de compra".center(60))
        print("*" * 60)
        print(f"Codigo de compra: {self.codigo_compra}")
        print(f"Proveedor: {self.proveedor.nombre_empresa}")
        print(f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')}")
        print("-" * 60)
        print(f"{'PRODUCTO':<20} {'CANT':<6} {'COSTO':<10} {'SUBTOTAL':<10}")
        
        for producto in self.productos_comprados:
            print(
                f"{producto['producto'].nombre:<20} "
                f"{producto['cantidad']:<6} "
                f"${producto['costo_unitario']:<9} "
                f"${producto['subtotal']:<10}"
            )
            
        print("-" * 60)
        print(f"TOTAL PAGADO: ${self.total}")
        print("*" * 60)
            
        
        
        
        
        
        
        
        
        
        
        
        
        