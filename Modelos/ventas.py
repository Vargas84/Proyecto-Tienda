from datetime import datetime 

class Ventas:
    def __init__(self,codigo_venta,usuario):
        self.codigo_venta=codigo_venta #identificador unico de la venta
        self.usuario=usuario #usuario (empleado) que registra la venta se conecta con la clase Usuario
        self.fecha=datetime.now() #fecha automatica en el momento de crear la venta
        self.productos_vendidos=[]# lista de productos vendidos en esta venta
        self.total=0 #total acumulado de la venta
        
        
    
    #Metodo para agregar un producto a la venta
    #Se conecta con la clase Producto(porque recibe un objecto producto para agregarlo a la venta)
    def agregar_producto(self,producto,cantidad,precio_unitario):
        if cantidad <=0:
            print("La cantidad debe ser mayor a cero")
            return
        
        
        if producto.stock < cantidad:
            print("No hay suficiente stock disponible para realizar la venta.")
            return
    
    
    def mostrar_detalles_venta(self):
        print(f'Detalles de la venta {self.codigo_venta}')
        print(f'Fecha: {self.fecha}')
        
        for venta in self.productos_vendidos:
            print(f'Producto: {venta.producto.nombre}, Cantidad: {venta.cantidad}, Precio Unitario: {venta.precio_unitario}, Subtotal: {venta.subtotal}')
            
            
        print(f'Total de la venta: {self.total}')