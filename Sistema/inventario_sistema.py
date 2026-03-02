from Modelos.inventario import Inventario
from Modelos.usuarios import Usuarios
from Modelos.productos import Productos
from utils import es_letras_y_espacios

#Creamos las instancias UNICAS del sistema
inventario=Inventario() #instancia de la clase Inventario, que contiene la lista de productos y metodos relacionados
"""
    
    print("\n--- REGISTRAR COMPRA ---")
    productos_temporales=[]#Lista temporal para almacenar los productos que se vana  comprar
    total_compra=0 #Variable para almacenar el total de la compra, se va actualizando a medida que se van agregando productos a la compra
    
    
    
    #Entrada de productos
    while True:#bucle que permite varios productos
        
        #Validacion del nombre del producto 
        while True:
            
           nombre_producto=input("Ingrese el nombre del producto a comprar: ").strip()
        
        #validamos que el nombre no este vacio y solo sean letras/espacios
           if nombre_producto and  es_letras_y_espacios(nombre_producto):
            break #si el nombre es valido, salimos del bucle de validación
           else:
            print("Error: El nombre del producto no puede estar vacio o contener caracteres no permitidos")
            continue
        
        
      #2 BUSCAR el producto en el inventario
        producto_contrado=inventario.buscar_producto(nombre_producto)#buscamos el producto en el inventario por su nombre

      #validacion de los datos numricos (Precio y cantidad)
        try:
            cantidad_comprada=int(input(f"Ingrese la cantidad a comprar del producto '{nombre_producto}': "))
            
            #costo lo que le pagamos al proveedor por la compra de ese prodcuto
            costo=float(input(f"Costo unitario del producto '{nombre_producto}': "))
            
            #precio venta es el precio al que vamos a vender ese producto, lo usamos para calcular el total de la compra y mostrarlo al usuario, pero no lo guardamos en el inventario porque el precio del producto en el inventario se actualiza con el precio unitario de la compra
            precio_venta=float(input(f"Precio de venta del producto '{nombre_producto}': "))
            
            
            #validamos que cantidad y precios no sean negativos o cero
            if cantidad_comprada<=0 or costo<=0 or precio_venta<=0:
                print("Error: La cantidad y los precios deben ser mayores a cero")
                continue
            
    #LOGICA de actualizacion o regisro
        #Si el producto ya existe en el inventario 
            if producto_contrado:
            #actualizamos el stock del producto sumando la cantidad comprada al stock 
              print(f"Producto '{nombre_producto}' encontrado en el inventario. Actualizando stock y precio.")
              producto_contrado.stock+=cantidad_comprada
            #guardamos el preico de venta en el objeto para el catalogo
              producto_contrado.precio=precio_venta
              producto_final=producto_contrado
              print(f"Producto actualizado exitosamente")
            
        #Si el producto no existe en el inventario, se crea un nuevo producto y se agrega al inventario
            else:
              print(f"Producto '{nombre_producto}' no encontrado en el inventario.\nRegistrando nuevo producto.")
            
            #Validacion de la categoria del producto nuevo
              while True:
                categoria=input(f"Ingrese la categoría para {nombre_producto}: ").strip()
                if es_letras_y_espacios(categoria) and categoria:
                    break # Si es válida, salimos del bucle
                print("ERROR: Categoría inválida. Solo use letras y espacios.")
            
           #Generamos id automatico y creamos el nuevo objeto
              nuevo_id=inventario.generar_id_productos()
              nuevo_producto=Productos(nuevo_id,nombre_producto,precio_venta,categoria,cantidad_comprada)
        #Lo agregamos a la lista de prodcutos del inventrio 
              inventario.agregar_productos(producto_final)
              print(f"Producto nuevo {producto_final.nombre} registrado exitosamente")

        #Guardamos temporalmente
            productos_temporales.append((producto_final,cantidad_comprada,costo))
        except ValueError:
            print(f"Eror: Ingrese solo numeros validos (Enteros para cantidad, decimales para precios)")
            continue
        #Preguntar para agregar mas productos
        opcion=input("\nDesea agregar mas productosa esta misma factura de compra? (s/n)").lower().strip()
        
        if opcion!='s':#si la opcion es diferente de s el codigo pasa al apartado de factura dando a entender que no desea agregar mas prodcutos
            break
    
    
    #Si no hay productos
    if not productos_temporales:
        print("No se procesaron los productos")
        return
    
    
    #DATOS Del provedor
    documento_proveedor=input("NIT del proveedor: ").strip()
    proveedor_objeto=inventario.buscar_proveedor_documento(documento_proveedor)
    
    if not proveedor_objeto:
        while True:
            nombre_proveedor=input("Nombre de la empresa o proveedor: ").strip()
            if nombre_proveedor and es_letras_y_espacios(nombre_proveedor):
                break
            print("Nombre invalido")
            
        while True:
            telefono = input("Teléfono: ").strip()
            if telefono.isdigit() and len(telefono) >= 7:
                break
            print("Teléfono inválido")

        proveedor_objeto = Proveedor(nombre_proveedor, documento_proveedor, telefono)
        inventario.lista_proveedores.append(proveedor_objeto)
        
        
        
    #Crear obejto compra
    id_compra=inventario.generar_id_compra()
    compra= Compra(id_compra,proveedor_objeto)
    
    #agregar productos a la compra
    for producto,cantidad,costo in productos_temporales:
        compra.agregar_productos(producto,cantidad,costo)
        
    #guardar compra en inventario
    inventario.lista_compras.append(compra)
    
    #Mostrar factura
    compra.mostrar_factura()
    print("Compra registrada exitosamente")
"""
    

#------------- MENU PRINCIPAL ---------------

def inventarioSistema(inventario):#funcion principal que ejecuta el inventario(Menu) y muestra los submenus
#inventario= instacia de la clase Inventario(contiene la lista de productos y metodos relacionados)
    while True:#bucle principal se repite hasta que el usuario elija salir(opcion 4)
        #INICIO DE SESION (Por parte de los trabajadores)
        print("\n======== INICIO DE SESION ========")
        print("1. Crear usuario")
        print("2. Iniciar sesion")
        print("3. Salir del sistema")
            
        try: 
            # Lee la opción del usuario desde entrada estándar y la convierte a entero.
            op_inicio = int(input("Seleccione una opcion: "))#Controla que el usuario ingrese una opcion valida (1,2 o 3)
        except ValueError: 
        # Si la conversión falla (p. ej. el usuario ingresó letras o caracteres especiales), cae aquí.
            print("ERROR: Ingrese un numero valido")
            continue #hace que el bucle while principal vuelva a empezar y muestre nuevamente el menu
        
        if op_inicio<1 or op_inicio>3: # Validación adicional: aunque la entrada sea int, verificamos rango válido (1..4).
            print("Opcion Fuera de rango")
            continue #hace que el bucle while principal vuelva a empezar y muestre nuevamente el menu
              # si es fuera del ramgo, volvemos al menu principal
              
              
        if op_inicio==1:#Si el usuario elige 1 en el menú principal, se llama a la función crear_usuario() para registrar un nuevo usuario
            print("\n======== CREAR USUARIO ========")
            print("Ingrese los datos del nuevo usuario: ")
            
            
            while True: #Bucle para validar que se ingrese un nombre correctament
               nombre= input("Ingrese su nombre:  ")
               #La función 'es_letras_y_espacios' verifica que el nombre contenga solo letras y espacios, y que no esté vacío.
               if not es_letras_y_espacios(nombre) or nombre is None:#verificacion de los datos para nombre de administrador
                   print("Nombre invalido. Use solo letras y espacios")
               else:
                   break
            
            while True: #bucle para validar que se ingrese un documento correctamente
                documento= input(f"Usuario {nombre} ingrese su documento: ")
                if documento.isdigit() and 8<= len(documento) <=11: #verificacion de los datos para el documento 
                    documento=int(documento) #convertimos el documento a entero
                    break
                else:
                   print("Documento inválido. Por favor, ingrese solo números de 8 a 11 dígitos.")
                   continue
               
               
            while True: #bucle para validar que se ingrese un telefono correctamente
                telefono= input(f"Usuario {nombre} ingrese su telefono: ")
                if telefono.isdigit(): #verificacion de los datos para el telefono
                    telefono=int(telefono) #convertimos el telefono a entero
                    break
                else:
                   print("Telefono inválido")
                   continue  
               
               
               
            while True: #bucle parqa validar que se ingrese un correo correctamente
                correo=input(f"Usuario {nombre} ingrese su correo: ")
                #verificacion basica: que contega @ y .com
                if "@" in correo and ".com" in correo:
                    #aqui podrias agregar validaciones mas complejas si lo deseas
                    break
                else: 
                    print("Correo invalido")
                    continue
                
            while True: #bucle para validar que se ingrese una contraseña segura
                contrasena=input(f'Usuario {nombre} ingrese su contraseña: ')
                
                #Definimos los criterios de seguridad
                tiene_largo=len(contrasena)>=8
                tiene_mayus=any(c.isupper() for c in contrasena)#verificacion de mayusculas(al menos una)
                tiene_numero=any(c.isdigit() for c in contrasena)#verificacion de numeros (al menos uno)
                #'c' es cada caracter de la contraseña, 'any' devuelve True si encuentra al menos uno que cumpla la condición (mayuscula o numero)
                
                if tiene_largo and tiene_mayus and tiene_numero:#si esto se cumple entonces la contraeña es segura
                    print("Contraseña segura")#se muestra un mensaje de confirmacion
                    break
                
                else:#en caso de que no se cumpla alguno de los criterios, se muestra un mensaje de error y se vuelve a pedir la contraseña
                    print("Contraseña insegura. \nAsegúrese de que tenga al menos 8 caracteres,\n-Al menos una letra mayuscula\n-Al menos un número.")
                    continue
            
            
            #CREAR USUARIO: creamos un nuevo objeto de tipo Usuarios con los datos ingresados por el usuario
            trabajador=Usuarios(nombre,documento,telefono,correo,contrasena)
            
            #GUARDAR: Accedemos a la lista de usuarios registrados en el menu
            inventario.usuarios_registrados.append(trabajador) #Agregamos el nuevo usuario a la lista de usuarios registrados en el menu
            print(f"Usuario {nombre} creado exitosamente")#mensaje de confirmacion
            print(f"Usuarios registrados: {[usuario.nombre for usuario in inventario.usuarios_registrados]}") #Imprime los nombres de los usuarios registrados para verificar que se guardo correctamente
        
        
        #INICIO DE SESION
        if op_inicio == 2:
            print("\n======== INICIAR SESIÓN ========")
    
            try:
                #Solicitamos el documento. Si el usuario ingresa letras, int() lanzará un error que capturamos en 'except'.
                doc_login = int(input("Ingrese su número de documento: "))
                #La contraseña se recibe como texto (string) para permitir caracteres especiales.
                contrasena_login = input("Ingrese su contraseña: ")

                # 'usuario_autenticado' inicia en None. Actúa como una "bandera" o "recipiente".
                # Si al final sigue siendo None, significa que no hubo coincidencia.
                usuario_autenticado = None

                # Recorremos la lista 'usuarios_registrados' que vive dentro del objeto 'inventario'.
                # 'usu' representa a cada objeto de la clase 'Usuarios' guardado en esa lista.
                for usu in inventario.usuarios_registrados:
            
            # Comparamos si el documento del objeto coincide con el ingresado Y
            # si la contraseña del objeto coincide con la ingresada.
                    if usu.documento == doc_login and usu.contrasena == contrasena_login:
                
                # Si coinciden, guardamos el objeto completo en nuestra variable de control.
                        usuario_autenticado = usu
                
                # Usamos 'break' para dejar de buscar, ya que encontramos al usuario.
                        break
        
                # Una vez fuera del bucle, verificamos si 'usuario_autenticado' contiene a alguien.
                if usuario_autenticado:
                    # Si entramos aquí, el login fue exitoso. Usamos el atributo .nombre del objeto.
                    print(f"\n¡Acceso concedido! Bienvenido/a, {usuario_autenticado.nombre}.")
                    
                    while True:
                        print(f"\n======== MENÚ DE GESTIÓN--Usuario: {usuario_autenticado.nombre}========")
                        print("1. Inventario")
                        print("2. Registrar entrada (Compra)")
                        print("3. Registrar salida (Venta)")
                        print("4. Cerrar sesión")

                        try:
                            opcion_gestion = int(input("Seleccione una opción: "))
                        except ValueError:
                            print("ERROR: Ingrese un número válido.")
                            continue

                        if opcion_gestion < 1 or opcion_gestion > 4:
                            print("Opción fuera de rango.")
                            continue

                        if opcion_gestion == 1:#INVENTARIO 
                        # Aquí llamaríamos a la función que maneja el inventario, pasando 'usuario' e 'inventario'.
                         while True:
                            print("\n--- MENÚ DE INVENTARIO ---")
                            print("1. Agregar producto")#Agregar producto: solicita al usuario los detalles del producto (nombre, precio, categoría, stock), 
                            #valida los datos, crea un nuevo objeto de tipo Productos 
                            #y lo agrega a la lista de productos del inventario.
                            print("2. Eliminar producto")#Eliminar producto: muestra una lista de productos con sus IDs, 
                            #solicita al usuario el ID del producto a eliminar,
                            print("3. Modificar producto")#Modificar producto: muestra una lista de productos con sus IDs, solicita al usuario el ID del producto a modificar,
                            #luego solicita los nuevos detalles del producto, valida los datos y actualiza el producto
                            print("4. Ver inventario")#Ver inventario: muestra una lista completa de los productos en el inventario, incluyendo su ID, nombre, precio, categoría y stock.
                            print("5. Volver al menú anterior")

                            try:
                                opcion_inventario = int(input("Seleccione una opción: "))#variable para validar la opcion del menu
                            except ValueError:#en caso de ingresar caracteres especiales o letras
                                print("ERROR: Ingrese un número válido.")
                                continue

                            if opcion_inventario < 1 or opcion_inventario > 5:
                                print("Opción fuera de rango.")
                                continue

                            if opcion_inventario == 1:#OPCION 1: AGREGAR PRODUCTO al inventario
                                print(f"\n--- AGREGAR PRODUCTO A INVENTARIO ---")
            
                                #Solicitamos detalles del producto al usuario
                                #validacion del nombre del prodcuto
                                while True:
                                    nombre=input("Nombre del producto: ")#nombre del plato a registrar
                                    if not es_letras_y_espacios(nombre) or nombre is None:#verificacion de los datos para nombre del producto
                                       print("Error: Nombre invalido. Use solo letras y espacios")
                                    break#solo llega aqui si el nombre es valido

                                while True:#Validacion del precio del producto
                                    precio=input("Precio a la venta del producto: ").strip()
                                    if not precio:#precio vacio 
                                        print("Precio incorrecto, ingrese un precio para el plato")#mensaje de advertencia
                                        continue
                                    try:#si el precio no es vacio
                                        precio=int(precio)#intentar pasarlo a numero entero
                                        if precio<=0:#si el precio es inferior o igual a 0 
                                            print('Precio incorrecto, ingrese un precio positivo o mayor a 0')
                                            continue
                                        else:
                                            break
                                    except:
                                        print('Precio incorrecto, ingrese un precio valido')#en caso de ingresar caracteres especiales o letras
                                        continue
                                    
                                while True:#Validacion de la categoria del produto
                                    categoria=input(f"Categoria del producto {nombre}: ")
                                #La función 'es_letras_y_espacios' verifica que el nombre contenga solo letras y espacios, y que no esté vacío.
                                    if  not es_letras_y_espacios(categoria) or categoria is None:#verificacion de los datos para categoria del producto
                                      print("Error: Categoria invalida. Use solo letras y espacios")
                                    break#solo llega aqui si la categoria es valida
            
            
                                while True: #validacion del stock del producto
                                    try:
                                        stock=int(input(f"Cantidad de stock del prodcuto {nombre}:"))
                                    except ValueError:
                                        print("Error: Ingrese un numero entero valido")
                                        continue
                                    if stock<=0:
                                        print("Els stock debe ser mayor a cero")
                                        continue
                                    break#Solo llaga aqui si el stock es valido
                
                                id_producto=inventario.generar_id_productos()#generador de Ids para los productos creados
                
                                #CREACION Y GUARDADO 
                                #Una vez que tenemos todos los datos validados, creamos un nuevo objeto de tipo Productos con estos datos
                               #agregamos el producto al inventario del menu
                                trabajador.agregar_productos(inventario,Productos(id_producto,nombre,precio,categoria,stock))
                                print(f'Producto agregado con ID automatico {id_producto}')
            
            
                            #OPCION 2: ELIMINAR PRODUCTO
                            elif opcion_inventario == 2:
                               print(f"\n--- ELIMINAR PRODUCTO DEL INVENTARIO ---")
                               trabajador.ver_inventario(inventario)#muestra el inventario para saber que producto eliminar
                               while True: #bucle para validar que se ingrese un nombre de producto correcto
                                    nombre_producto=input("Ingrese el nombre del producto a eliminar: ").strip()
                                    if not es_letras_y_espacios(nombre_producto) or nombre_producto is None:#verificacion de los datos para nombre del producto a eliminar
                                       print("Error: Nombre invalido. Use solo letras y espacios")
                                       continue #reiniciar el bucle inmediantamente para volver a pedir el nombre del prodcuto
                
                                    if not nombre_producto:#validar que no este vacio
                                       print("Error: El nombre del producto no puede estar vacio")
                                       continue
                                   #se llama al metodo eliminar productos de la clase inventario 
                                    if inventario.eliminar_producto(nombre_producto):#si el metodo retorna True, se elimino el producto  
                                        print(f"Producto {nombre_producto} eliminado exitosamente")
                                        break
                                    else:#si el metodo retorna False, no se encontro el producto con ese nombre
                                         print(f"Error: No se encontró el producto con el nombre '{nombre_producto}' en el inventaio")
    
    
                            #OPCION 3: EDITAR UN PRODUCTO (nombre, precio, categoria o stock)
                            elif opcion_inventario == 3:
                                try:
                                    trabajador.ver_inventario(inventario)#muestra el inventario para saber cual Producto(ID) quiere editar
                                    id_p=int(input('Ingrese el codigo del producto a editar'))#id_p es el ID del producto qe se quiere editar
                                except:
                                    print('Error: Ingrese un numero valdio')#en caso de que se ingrese una opcion incorrecta
                                    continue
                                
                                #suamos inventario.buscar_producto_id() para obtener la referencia el objeto producto
                                producto=inventario.buscar_producto_id(id_p) 
                                
                                if producto is None:
                                    #si no existe un producto con ese OCDIGO, informamos y volvemos al submenu
                                    print('Plato no encontrado')
                                    continue
                                
                                while True:#si el plato existe entramos el menu de opciones a editar
                                    print('1).Nombre\n2).Precio\n3).Categoria\n4).Volver al menu anterior')
                                    
                                    try:#se pide qe opcion se desea editar
                                        op=int(input(f'¿Que desea editar del plato {producto.nombre}?' ))#se pregunta que se desea editar del plato que ingresamos'))
                                    except:
                                        print('Erro. Entrada invalida')#en caso de una entrada no valida vuelve al menu
                                        continue
                                    
                                    
                                    if op<1 or op>4:
                                        print('Error:Opcion fuera de rango')
                                        continue #vuelve al menu
                                    
                                    elif op==1:#editar ell nombre
                                        nuevo_nombre=input('Ingrese el nuevo nombre del producto: ')#se pide un nuevo nombre
                                        if nuevo_nombre=="":#si se deja vacio el sistema dejara el nombre que tiene sin modificar
                                           producto.nombre=producto.nombre#se asigna nuevamente el mismo nombre
                                           print(f'EL nombre del producto {producto.nombre} quedo igual: {producto.nombre}')#se da aviso de que el nombre quedo igual
                                           break# y se rompe el ciclo para el nombre
                                        if not es_letras_y_espacios(nuevo_nombre):#si el nombre no contiene letras se da aviso
                                           print('El nuevo nombre debe contenes solo letras\n')#se repite el ciclo hasta que se ingrese un nombre valido
                                        else:
                                            trabajador.editar_productos(inventario,id_p,nuevo_nombre=nuevo_nombre)#si pasa las validaciones el nombre se agrega correctamente
                                            break #y se rompe el ciclo para nombre
                                        
                                    elif op==2:#editar el precio
                                        nuevo_precio=input('Ingrese el nuevo precio del producto: ')#se pide el nuevo precio del producto
                                        if  nuevo_precio.isdigit():#se verifica que el nuevo precio sea un numero
                                            nuevo_precio=int(nuevo_precio)#si es un sigito lo convierte de str a entero
                                           
                                            if nuevo_precio>0:#si este numero es mayor a 0 
                                               trabajador.editar_productos(inventario,id_p,nuevo_precio=nuevo_precio)#el neuvo precio se agrega correctamente
                                               break# y se rompe el ciclo
                                            
                                            elif nuevo_precio<=0:#en caso de que el entero sea inferior o igual a 0
                                                print('El precio debe ser mayor a 0')
                                                
                                            elif nuevo_precio=="":#si el nuevo precio es vacio se deja como estaba antes
                                                 producto.precio=producto.precio #se hace la asignacion correspondiente
                                                 print(f'El precio del producto {producto.nombre} quedo igual: {producto.precio}\n')#se muestra el mensaje
                                                 break#se rompe el ciclo
                                            else:
                                                print(f'El precio debe ser un numero\n')#en caso de ingresar valores diferentes a numeros
                                                continue
                                    
                                    elif op==3:#editar categoria
                                        nueva_categoria=input('Ingrese la nueva categoria del producto: ')
                                        if nueva_categoria=="":#si la categoria esta vacia se deja como antes
                                            print(f'La categoria del producto {producto.nombre} quedo igual: {producto.categoria}')#se muestra el mensaje
                                            break #se rompe el ciclo
                                        if not es_letras_y_espacios(nueva_categoria):#se hace la validacion de que contenga letras y espacios
                                            print('La categoria debe contener solo letras')
                                        else:#en caso de que la validacion sea correcta
                                            trabajador.editar_productos(inventario,id_p,nueva_categoria=nueva_categoria)#procede a cambiar el estado de la categoria
                                            break
                                    
                                    elif op==4:#volver al menu anterios
                                        break#rompe el codigo
                                                                                  
                            elif  opcion_inventario == 4:  #ver inventario     
                                print('\n------INVENTARIO ACTUAL------')
                                inventario.mostrar_inventario()
                                    
                                    
                                       

                        elif opcion_gestion == 2:
                         # Aquí llamaríamos a la función que maneja las ventas, pasando 'usuario' e 'inventario'.
                           pass  # Reemplaza con la llamada a tu función de gestión de ventas
                        elif opcion_gestion == 3:
                        # Aquí llamaríamos a la función que maneja las compras, pasando 'usuario' e 'inventario'.
                          pass  # Reemplaza con la llamada a tu función de gestión de compras
                        elif opcion_gestion == 4:
                          print(f"¡Hasta luego, {usuario_autenticado.nombre}!")
                        break
                else:
            # Si el bucle terminó y la variable sigue siendo None, los datos estaban mal.
                    print("\nError: El número de documento o la contraseña son incorrectos.")

            except ValueError:
        # Este bloque se activa si el usuario escribe algo que no sea un número en 'doc_login'.
             print("\nError de entrada: El documento debe ser un número entero sin letras ni puntos.")
            
            
            #Cerrar el sistrema
        elif op_inicio==3:#Si el usuario elige 3 en el menú principal, imprimimos un mensaje y salimos
            print("Gracias por usar el sistema")
            break
            
            




            
            