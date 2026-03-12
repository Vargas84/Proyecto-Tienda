from Modelos.compras import Compra
from Modelos.productos import Productos
from utils import es_letras_y_espacios

class Inventario:
    def __init__(self):
        self.lista_productos = []#lista donde se almacenan toods los platos,inicialmente vacia
        self.lista_proveedores=[] #lista donde se almacenan todos los proveedores, inicialmente vacia
        self.productos_id=1 #contador de Codigos o IDs para productos, inicia en 1
        #y se incrementa cada vez que se agrega un nuevo producto al inventario
        self.usuarios_registrados=[]#Aqui guardaremos los objetos de tipo Usuarios
        self.compras_id=1
    
    def generar_id_compra(self):
        id_generador_compras=self.compras_id
        self.compras_id+=1
        return id_generador_compras
        
            
    def generar_id_productos(self):#generador de IDs para los platos
       id_generador_productos=self.productos_id#el id generado es igual al valor actual del id
       self.productos_id+=1#el ultimo id se aumenta una vez ya generado
       return id_generador_productos#retorna este valor
  
        
    def mostrar_inventario(self):#se muestran los productos que hay en el inventario y su informacion
        print('\n --- INVENTARIO ---')
        for producto in self.lista_productos:#recorre la lista
            if not self.lista_productos:#si no hay productos cargados en el inventario
                print('\n'+'!'*40)
                print('El inventario se encuentra vacio')
                print('!'*40)
                return 
            print(producto.mostrar_informacion())#se muestra el producto y su informacion con ayuda
            #del metodo mostrar_informacion() de producto con nombre/precio/categoria/disponibilidad y stock
        print(' ')
        
    def agregar_producto(self, producto):
        #recibe un objeto de tipo producto y lo agrega a la lista de productos del inventario
        self.lista_productos.append(producto)
        print(f'El producto {producto.nombre} fue agregado correctamente')
        
        
    def buscar_producto(self,nombre_producto):#buscar por el nombre
        #Buscar un producto por su nombre sin importar mayusculas o minusculas
        # y devolver el objeto si lo encuentra
        
        nombre_producto=nombre_producto.lowe().strip()
        for producto in self.lista_productos:
            if producto.nombre.lower()==nombre_producto:
                return producto #retorna el prodcuto encoontrado
            return None #retorna None si no se encontro el producto con ese nombre
    
    def buscar_producto_id(self,codigo_producto):#buscar producto por su ID 
        for producto in self.lista_productos:#recorre la lista de productos uno por uno
            if producto.codigo==codigo_producto:
                return producto#cuando encuentra un producto cuyo ID(codigo) coincide lo retorna
            return None #Si recorre toda la lista y no encuentra nada, devuelve none
            #para que el que este llamando a la funcion pueda verificae y actuar con un mensaje de alerta

        
        
        
        
    def eliminar_producto(self,nombre_producto):
        #Busca y elimina ignorando mayusculas y minusculas 
        nombre_producto=nombre_producto.lower().strip()
        #recibe un nombre de producto, busca el producto con ese nombre en la lista de productos y lo elimina
        for producto in self.lista_productos:
            if producto.nombre.lower() == nombre_producto:
                self.lista_productos.remove(producto)
                print(f'Producto {producto.nombre} eliminado correctamente')
                producto.eliminado=True#ademas se marca como eliminado el Producto para indicar quee fue eliminado
                #esto nos ayuda en caso de que haya referencias al obejto en pedidos
                break#salimos de la funcion para no buscar mas
        else:            
            return f'Producto no encontrado\n'#retorna False si no se encontro el producto con ese nombre
    
    
    #METODOS PARA PROVEEDRORES
    
    def buscar_proveedor_documento(self,documento):        
        for proveedor in self.lista_proveedores:
            if proveedor.documento==documento:
                return proveedor #retorna el proveedor encoontrado
            return None #retorna None si no se encontro el proveedor con ese documento


    def proveedor_existe(self,documento,telefono):
        #verifica si ya existe un proveedor con ese documento o telefono, para evitar duplicados en el registro de proveedores
        #Retorna True si se encontro el proveedor con ese documento o telefono, False si no se encontro el proveedor con ese documento o telefono     
        for proveedor in self.lista_proveedores:
            if proveedor.documento==documento or proveedor.telefono==telefono:
                return True, f"Proveedor con documento {documento} o teléfono {telefono} ya existe."#retorna True si se encontro el proveedor con ese documento o telefono
            return False #retorna False si no se encontro el proveedor con ese documento o telefono


    def agregar_proveedor(self,nuevo_proveedor):
        #Recibe un objeto proveedor y revisa que no se repita 
        # ni el documento ni el teléfono antes de guardarlo.
        
        #revisar el documento 
        documento_repetido= False #empezamos asumiendo que el documento no esta repetido
        for proveedor in self.lista_proveedores:## Comparamos el documento de cada proveedor guardado con el nuevo
            if proveedor.documento==nuevo_proveedor.documento:
                documento_repetido=True #si encontramos un documento igual, marcamos que el documento esta repetido
                break #salimos del bucle porque ya encontramos un documento repetido, no es necesario seguir buscando
            
            
            
        if documento_repetido==True:
            return False, f"Error: El documento {nuevo_proveedor.documento} ya está registrado para otro proveedor." #retorna False si el documento esta repetido
        
        #revisar el telefono
        telefono_repetido=False #empezamos asumiendo que el telefono no esta repet
        
        
        for proveedor in self.lista_proveedores:## Comparamos el telefono de cada proveedor guardado con el nuevo
            if proveedor.telefono==nuevo_proveedor.telefono:
                telefono_repetido=True #si encontramos un telefono igual, marcamos que el telefono esta repetido
                break #salimos del bucle porque ya encontramos un telefono repetido, no es necesario seguir buscando    
            
            
            
        if telefono_repetido==True:
            return False, f"Error: El teléfono {nuevo_proveedor.telefono} ya está registrado para otro proveedor." #retorna False si el telefono esta repetido
        
        #si el documento y el telefono no estan repetidos, se agrega el nuevo proveedor a la lista de proveedores
        self.lista_proveedores.append(nuevo_proveedor)
        return True, f"Proveedor {nuevo_proveedor.nombre_empresa} agregado exitosamente." #retorna True si el proveedor se agrego exitosamente
    
    
    #METODOS PARA REGISTRAR COMPRAS (entradas al inventario)
    def registrar_compra(self,nombre_producto,cantidad_compradada,precio_unitario):
        #registra la entrada de mercancia al inventario 
        #recibe nombre del prodcuto, cantidad comprada, precio unitario y el proveedor de la compra
        #si el producto ya existe en el inventario, se actualiza su stock y precio
        #si el producto no existe en el inventario, se crea un nuevo producto y se agrega al inventario
        
        #buscar el prodcuto en el inventario
        producto_encontrado=self.buscar_producto(nombre_producto)
        
        if producto_encontrado!=None:#producto ya existe en el inventario
            #Sumamos la nueva cantidad al stock que ya teniamos
            producto_encontrado.stock+=cantidad_compradada
            
            #actualizamos el precio del producnto con el nuevo precio unitarioi
            producto_encontrado.precio=precio_unitario
            
            print(f"Producto '{nombre_producto}' actualizado")
            print(f"Nuevo stock: {producto_encontrado.stock} | Nuevo precio: {producto_encontrado.precio}")
            
            
        else:#producto no existe en el inventario, se crea un nuevo producto y se agrega al inventario
            print(f"Producto '{nombre_producto}' no existe.\nIniciando registro de producto nuevo.")
            
            while True:#validacion de categoria
                categoria = input(f"Ingrese la categoría para {nombre_producto}: ").strip()
                # Usamos tu función de letras y espacios
                if es_letras_y_espacios(categoria) and categoria:
                    break # Si es válida, salimos del bucle
                print("ERROR: Categoría inválida. Solo use letras.")
                
            #CREACION DEL OBJETO    
            # Aquí ya tenemos: nombre (que viene por parámetro), cantidad, precio y categoría validada
            nuevo_producto=Productos(self.generar_id_productos(),nombre_producto,precio_unitario,categoria,cantidad_compradada)
            
            #Guardamos en la lsita de productos
            self.agregar_producto(nuevo_producto)
            print(f"Producto '{nombre_producto}' registrado exitosamente con ID {nuevo_producto.codigo}.")
    
        #IMPLEMENTACION DE PROVEEDOR EN LA COMPRA
        #Mostramos quien nos vendio y cuanto nos costo la compra
        
    
    
    
    
        return True #retorna True si se registro la compra exitosamente, ya sea actualizando un producto existente o creando uno nuevo
    
    
    
    
    
    
    
    
    
    
    
    
    
    