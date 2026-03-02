class Usuarios:
    #Clase que permite la creacion de usuarios correctamente
    
    def __init__(self,nombre,documento,telefono,correo,contrasena):#nos aseguramos de inicializar 
        #correctamente estos atributos
        self.nombre=nombre
        self.documento=documento
        self.telefono=telefono
        self.correo=correo
        self.contrasena=contrasena
    
    def ver_inventario(self,inventario):
        inventario.mostrar_inventario()#se llama la funcion mostrar inventario de la clase INVENTARIO 
        
        
        
    def agregar_productos(self,inventario,producto):
        #funcion que permite al usuario(trabajador) agregar ub objeto Producto al inventario
         inventario.agregar_producto()
         
         
    def eliminar_productos(self,inventario,nombre_producto):
        #funcion que permite al trabajador eliminar un producto del inventario por su nombre
        #internamente llama al metodo eliminar_producto() de Invetario, ya 
        #Qeu recorre la lista y elimina el producto
        inventario.eliminar_producto(nombre_producto)#se llama la funcion eliminar producto de la clase inventario
    
    def editar_productos(self,inventario,id_producto,nuevo_nombre=None,nuevo_precio=None,nueva_categoria=None):#funcion que ayuda al menuSistema a hacer validaciones
    #el atrabajador puede editar el precio de los platos
        producto=inventario.buscar_producto_id(id_producto) #busca el objeto producto con el ID
        if producto is None:#si el producto no existe
          print("Error el producto no existe")
        if nuevo_nombre is not None:#editar nombre si el producto
            try:
              producto.nombre=nuevo_nombre#entra a asignar el nuevo nombre
              print(f"Nombre del producto actualizado a: {nuevo_nombre}")#envia un mensaje de actualizacion
            except:
              print("Error: ingrese datos correctos para nombre dese la funcion")#en caso de ingresar numeros
        if nuevo_nombre=="":#si se deja un vacio el sistema dejara el nombre que tiene sin modificarlo
            producto.nombre=producto.nombre#se asigna nuevamente el mismo nombre
            print(f"El nombre del plato {producto.nombre} quedo igual: {producto.nombre}")#se da aviso de esta asignacion

        if nuevo_precio is not None:#editar precio si no es nulo el valor
            producto.precio=nuevo_precio#se asigna el nuevo precio
            print(f"Precio actualizado a: {nuevo_precio}")#se da aviso de esta actualizacion 
        if nuevo_precio=="":#si el nuevo precio es vacio el sistema dejara el mismo precio que tenia
           producto.precio=producto.precio#se asigna el mismo precio
           print(f"El precio del plato {producto.nombre} quedo igual: {producto.precio}")#se da aviso de esta asignacion



        if nueva_categoria is not None:#editar categoria si no es nulo el valor
            try:
               producto.categoria=nueva_categoria#se le asigna la nueva categoria
               print(f'Categoria actualizada a: {nueva_categoria}')#se da aviso de la asignacion    
            except:
               print("Error: ingrese datos correctos para la categoria")
        if nueva_categoria=="":#en caso de quedar en vacio el espacio el sistema dejara la misma categoria
            producto.categoria=producto.categoria#asignacion a la categoria que estaba
            print(f"La categoria del plato quedo igual {producto.categoria}")#aviso de esa asignacion
       
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        