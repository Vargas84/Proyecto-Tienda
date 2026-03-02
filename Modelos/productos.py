class Productos:
    def __init__(self,codigo,nombre,precio,categoria,stock):
        self.codigo=codigo #identificador del producto
        self.nombre=nombre #nombre del producto
        self.precio=precio #precio de cada producto
        self.categoria=categoria #categoria a la que pertenece el producto
        self.stock=stock #cantidad disponible de inventario para el producto
        self.eliminado=False 
        
    def mostrar_informacion(self):#se muestra la informacion del producto
            if self.disponible=="Disponible":
                return f"Codigo: {self.codigo}| Nombre: {self.nombre}| Precio: {self.precio}| Categoria: {self.categoria}| Stock: {self.stock}| Disponible: {self.disponible}"
            else:
                return f"Codigo: {self.codigo}| Nombre: {self.nombre}| Precio: {self.precio}| Categoria: {self.categoria}| Stock: {self.stock}| Disponible: {self.disponible}"
            
        
    def aumentar_stock(self, cantidad):#aumentar el stock del producto
        if cantidad > 0:#si la cantidad es positiva se permite aumentar el stock
            self.stock+=cantidad
            print(f"Stock actualizado. Nuevo stock: {self.stock}")#se muestra el nuevo stock despues de aumentar el stock
        else:#en caso contrario se arroja un mensaje de error
            print("La cantidad debe ser mayor a cero.")
            
            
    def disminuir_stock(self, cantidad):#disminuir el stock del producto
        if cantidad <= 0:#si la cantidad es negativa o cero no se permite la venta
            print("La cantidad debe ser mayor que 0.")#se arroja un mensaje de error
        elif cantidad > self.stock:#si la cantidad es mayor al stock disponible no se permite la venta 
            print("No hay suficiente stock disponible.")#se arroja un mensaje de error 
        else:# de lo contrarop se realiza la venta y se disminuye el stock
            self.stock -= cantidad
            print(f"Venta realizada. Stock restante: {self.stock}")#se muestra el stock restante despues de la venta 



    def actualizar_stock(self,cantidad):
        self.stock=cantidad #actualiza el stock del producto con la cantidad dada
        self.disponible="Disponible" if self.stock > 0 else "No disponible "