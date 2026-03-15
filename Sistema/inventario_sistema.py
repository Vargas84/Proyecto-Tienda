from Modelos.inventario import Inventario
from Modelos.usuarios import Usuarios
from Modelos.productos import Productos
from Modelos.compras import Compra
from Modelos.detalleCompra import DetalleCompra
from utils import es_letras_y_espacios

#Creamos las instancias UNICAS del sistema
inventario=Inventario() #instancia de la clase Inventario, que contiene la lista de productos y metodos relacionados


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
                if not documento: #documento vacio
                    print('Debes ingresar un documento. Este campo es obligatorio para el registro')
                    continue#reiniciar al while
                elif not documento.isdigit():
                    print('Ingrese unicamente numeros')
                    continue#reiniciar el while
                
                elif len(documento)>=8 and len(documento)<=10:#si el documento contiene de 8 a 10 numeros
                    try:
                        documento=int(documento)#convertimos a entero cuando sean validos
                    
                        #validar si existe ya en la base de datos
                        existe=False#variable para verificar si existe o no
                        for usuario in inventario.usuarios_registrados:
                            if usuario.documento ==documento:
                                existe=True
                                break#dejarlo de buscar si lo encuentra
                        if existe:
                            print(f'El documento {documento} ya esta en uso. Intente nuevamente')
                            #no hay break aqui asi que el while True se repite
                        else:
                            #paso todas las pruebas
                            #documento=documento #guardamos el valor validado
                            break   #rompe el while y pasa al siguiente requisito    
                
                    except:
                        print('Ingrese su numero de documento sin espacios ni puntos')
                        continue
                else:
                    print('Ingrese un documento con minimo 8 numeros y maximo 10 numeros')
               
               
            while True: #bucle para validar que se ingrese un telefono correctamente
                telefono= input(f"Usuario {nombre} ingrese su telefono: ")
                if not telefono:#telefono vacio
                    print('Debes ingresar un telefono. Este campo es obligatorio para el registro')
                    continue# reiniciar el while
                elif not telefono.isdigit():
                    print('Ingrese unicamente numeros')
                    continue#reinicie el while
                elif len(telefono)==10:#si la longitud del telefono es 10
                    try:
                        telefono=int(telefono)#convertios a entero el numero de telefoono
                        #validar si existe ya en la base de datos
                        existe=False#variable para verificar si existe o no
                        for usuario in inventario.usuarios_registrados:
                            if usuario.telefono==telefono:
                                existe=True
                                break#dejarlo de buscar si lo encuentra
                        if existe:
                            print(f'El telefono {telefono} ya esta en uso. Intente nuevamente')
                            #el while se repite
                    
                        else:
                            #si llegamos aqui pasamos todas las pruebas
                            break# rompe el codigo y guarda el telefono
                    except:
                        print('Ingrese su telefono sin espacios ni puntos')
                        continue
                else:
                    print('Ingrese un telefono con maximo 10 numeros')
                
            while True: #bucle parqa validar que se ingrese un correo correctamente
                correo=input(f"Usuario {nombre} ingrese su correo: ")
                if not correo:#correo vacio
                    print('Debes ingresar un correo. Este campo es obligatorio para el registro')
                    continue#reinicia el bucle

                    #verificacion basica: que contega @ y .com
                if "@" in correo and ".com" in correo:#si es correcto que contenga esto
                    existe=False
                    for usuario in inventario.usuarios_registrados:#buscar que el correo no este repetido
                        if usuario.correo==correo:
                            existe=True
                            break#dejarlo de buscar si lo encuentra
                    if existe:
                        print(f'El correo {correo} ya esta en uso. Intente nuevamnete')
                        #el while se repite
                    else:#si llegamos aqui pasamos todas las pruebas
                        break
                else:
                    print('Ingrese un correo valido. Debe contener "@" y ".com"')
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
        
        #INICIO DE SESION
        if op_inicio == 2:
            print("\n======== INICIAR SESIÓN ========")
            
            try:
                #Solicitamos el documento. Si el usuario ingresa letras, int() lanzará un error que capturamos en 'except'.
                doc_login = int(input("Ingrese su número de documento: "))
            except ValueError:
                # Este bloque se activa si el usuario escribe algo que no sea un número en 'doc_login'.
                print("\nError de entrada: El documento debe ser un número entero sin letras ni puntos.")
            else:
                #buscamos el documento previamente registrado
                usuario_autenticado = None
                
                for usuario in inventario.usuarios_registrados:#bucamos que el docuemento este previamente registrado
                    if usuario.documento ==doc_login:
                        usuario_autenticado=usuario#guardamos el objeto si existe
                        break
                #verificamos si lo encontramos
                if usuario_autenticado is None:
                    print('Error: Este documento no existe en la base de datos')
                    print('Debe registrarse primero o verificar el numero')
                    continue
                    #aca el programa vuelve a reinicar nuevamente
                else:
                    #solo si el documento existe, pedimos la contraseña
                    #La contraseña se recibe como texto (string) para permitir caracteres especiales.
                    contrasena_login = input("Ingrese su contraseña: ")
                    
                    if usuario_autenticado.contrasena==contrasena_login:
                # Una vez fuera del bucle, verificamos si 'usuario_autenticado' contiene a alguien.
                    #if usuario_autenticado:
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
                                    print("2. Disponibilidad de un producto")#Eliminar producto: muestra una lista de productos con sus IDs, 
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
                                            nombre=input("Nombre del producto: ").strip().replace(" ","")#nombre del plato a registrar
                                        
                                            if not nombre:#en caso de nombre vacio
                                                print('Este campo es obligatorio. Ingrese un nombre')
                                                continue#volvemos al inicio
                                            if not es_letras_y_espacios(nombre):#verificacion de los datos para nombre del producto
                                                print('Error: Ingrese unicamente letras')
                                                continue#volvemso al inicio
                                        
                                            #si el nombre no es vacio y contiene las letras
                                            existe=False
                                            for producto in inventario.lista_productos:#buscar  que no hayan nombre repetidos
                                                if producto.nombre.replace(" ","").lower()==nombre.lower():
                                                    existe=True
                                                    break
                                            if existe:
                                                print('Ese nombre ya esta en uso. Ingrese un nombre diferente')
                                                continue#reinicia al while hasta el principio
                                            else:#paso todas las verificaciones
                                                break#si llegamos aqui todo esta bien
                                        
                                        
                                        
                                        while True:#Validacion del precio del producto
                                            precio=input("Precio a la venta del producto: ").strip()
                                            if not precio:#precio vacio 
                                                print("Este campo es obligatorio. Ingrese un precio")#mensaje de advertencia
                                                continue#vuelve a pedir el precio
                                    
                                            if not precio.isdigit():
                                                print('Ingrese un precio numerico sin espacios ni puntos ni comas')
                                                continue#vuelve a pedir el precio
                                            #si el precio no es vacio
                                            precio=float(precio)#intentar pasarlo a numero flotante
                                            if precio<=0:#si el precio es inferior o igual a 0 
                                                print('Precio incorrecto, ingrese un precio mayor a 0')
                                                continue#vuelve al while
                                            else:#si llego aqui el precio es totalmente correcto
                                                break

                                    
                                        while True:#Validacion de la categoria del produto
                                            categoria=input(f"Categoria del producto {nombre}: ").strip()
                                        #La función 'es_letras_y_espacios' verifica que el nombre contenga solo letras y espacios, y que no esté vacío.
                                            if  not categoria:#en caso de categoria vacia
                                                print('Este campo es obligatorio. Ingrese una categoria')
                                                continue#vuelve a pedir la categoria
                                            if not es_letras_y_espacios(categoria):#se verifica que no contenga ni numeros ni caracteres especiales
                                                print('Error: Categoria invalida. Ingrese unicamente letras y espacios')
                                                continue#reinicia el bucle
                                            break#si las validaciones son correctas
                                
            
                                        while True: #validacion del stock del producto
                                            stock=input(f"Cantidad de stock del prodcuto {nombre}: ").strip()
                                    
                                            if not stock:#en caso de que sea vacio
                                                print('Este campo es obligatorio. Ingrese un stock')
                                                continue#reinicia el while
                                            if not stock.isnumeric():#en caso de que no contenga numeros
                                                print('Ingrese unicamente numeros enteros')
                                                continue#reinicia el while
                                    
                                            stock=int(stock)
                                            if stock<=0:
                                                print('Ingresa un stock mayor a 0')
                                                continue#reinicia el while
                                            break#Solo llaga aqui si el stock es valido
                
                                        id_producto=inventario.generar_id_productos()#generador de Ids para los productos creados
                
                                        #CREACION Y GUARDADO 
                                        #Una vez que tenemos todos los datos validados, creamos un nuevo objeto de tipo Productos con estos datos
                                        #agregamos el producto al inventario del menu
                                        trabajador.agregar_productos(inventario,Productos(id_producto,nombre,precio,categoria,stock))
                                        print(f'Producto agregado con ID automatico {id_producto}')
            
            
                                    #OPCION 2: DESACTIVAR UN PRODUCTO o cambiar la disponiblidad 
                                    elif opcion_inventario == 2:
                                        print(f"\n--- DISPONIBILIDAD DE PRODUCTOS DEL INVENTARIO ---")
                                        trabajador.ver_inventario(inventario)#muestra el inventario para saber que producto eliminar
                                        try:
                                            codigo_producto=int(input('\nIngrese el codigo del producto a cambiar la disponibilidad: '))
                                        except:
                                            print('Error: Ingrese un numero valido')#en caso de ingresar letras u otros tipos de caracteres
                                            continue
                               
                                        trabajador.cambiar_disponibilidad_producto(inventario,codigo_producto)
                               
    
                                    #OPCION 3: EDITAR UN PRODUCTO (nombre, precio, categoria o stock)
                                    elif opcion_inventario == 3:
                                        clave_editar="jabon"#clave que da acceso al menu de editar
                                        #solo los usuario que tengan la clave tendran acceso
                                        pedir_clave=input('Ingrese la contraseña para acceser al menu de editar: ')#el usuario ingresa la clave para acceder al menu de editar
                                        
                                        if pedir_clave!=clave_editar:
                                            print('\n!Clave incorrecta¡ !Acceso denegado¡')
                                            continue
                                        else:
                                            print(f'\n!Acceso concedido¡ Bienvenido usuario === {usuario_autenticado.nombre} ===')
                                        #verificamos si hay productos 
                                            if not inventario.lista_productos:
                                                print('\n'+'!'*40)
                                                print('El inventario se encuentra vacio')
                                                print('!'*40)
                                                print(' --- Agregue productos antes --- ')
                                                continue
                                            try:
                                                trabajador.ver_inventario(inventario)
                                                id_p=int(input('\nIngrese el codigo del producto a editar: '))#id_p es el ID del producto qe se quiere editar
                                            except:
                                                print('Error: Ingrese un numero valido')#en caso de que se ingrese una opcion incorrecta
                                                continue
                                
                                            #suamos inventario.buscar_producto_id() para obtener la referencia el objeto producto
                                            producto=inventario.buscar_producto_id(id_p) 
                                
                                            if producto is None:
                                                #si no existe un producto con ese OCDIGO, informamos y volvemos al submenu
                                                print('Producto no encontrado')
                                                continue
                                
                                            while True:#si el plato existe entramos el menu de opciones a editar
                                                #se debe mostrar toda la informacion del producto
                                                print(f"\n{'Codigo':<10} | {'Nombre':<20} | {'Precio':<10} | {'Stock':<10} | {'Categoría':<15} | {'Disponibilidad':<20}")
                                                print("-" * 100)
                                                print(producto.mostrar_informacion())
                                                print(f'\n --- Editando: {producto.nombre} --- ')
                                                print('1).Nombre\n2).Precio\n3).Stock\n4).Categoria\n5).Volver al menu anterior')
                                    
                                                try:#se pide qe opcion se desea editar
                                                    op=int(input(f'¿Que desea editar del producto {producto.nombre}?: ' ))#se pregunta que se desea editar del plato que ingresamos'))
                                                except:
                                                    print('Error. Entrada invalida')#en caso de una entrada no valida vuelve al menu
                                                    continue
                                    
                                                if op<1 or op>5:
                                                    print('Error:Opcion fuera de rango')
                                                    #continue #vuelve al menu
                                    
                                                elif op==1:#editar ell nombre
                                                    while True:
                                                        nuevo_nombre=input('Ingrese el nuevo nombre del producto: ').strip()#se pide un nuevo nombre                            
                                                        if nuevo_nombre=="":#si se deja vacio el sistema dejara el nombre que tiene sin modificar
                                                            producto.nombre=producto.nombre#se asigna nuevamente el mismo nombre
                                                            print(f'EL nombre del producto {producto.nombre} quedo igual: {producto.nombre}')#se da aviso de que el nombre quedo igual
                                                            break# y se rompe el ciclo para el nombre
                                                        if not es_letras_y_espacios(nuevo_nombre):#si el nombre no contiene letras se da aviso
                                                            print('El nuevo nombre debe contenes solo letrasy')#se repite el ciclo hasta que se ingrese un nombre valido
                                                            continue
                                                        existe=False
                                                        for producto in inventario.lista_productos:
                                                            if producto.nombre.lower().replace(" ","")==nuevo_nombre.lower().replace(" ",""):
                                                                existe=True
                                                                break
                                                        if existe:
                                                            print('Ese nombre ya esta en uso. Ingrese un nombre diferente')
                                                            continue
                                                        else:#llega hasta aca si pasa todas las pruebas
                                                            trabajador.editar_productos(inventario,id_p,nuevo_nombre=nuevo_nombre)#si pasa las validaciones el nombre se agrega correctamente
                                                            break #y se rompe el ciclo para nombre
                                        
                                                elif op==2:#editar el precio
                                                    nuevo_precio=input('Ingrese el nuevo precio del producto: ')#se pide el nuevo precio del producto
                                                    if nuevo_precio=="":#si el nuevo precio es vacio se deja como estaba antes
                                                        producto.precio=producto.precio #se hace la asignacion correspondiente
                                                        print(f'El precio del producto {producto.nombre} quedo igual: {producto.precio}\n')#se muestra el mensaje
                                                        continue#vuelve al menu de los atributos a editar
                                                    if  nuevo_precio.isdigit():#se verifica que el nuevo precio sea un numero
                                                        nuevo_precio=int(nuevo_precio)#si es un sigito lo convierte de str a entero
                                        
                                                        if nuevo_precio>0:#si este numero es mayor a 0 
                                                            trabajador.editar_productos(inventario,id_p,nuevo_precio=nuevo_precio)#el neuvo precio se agrega correctamente
                                                            continue
                                            
                                                        elif nuevo_precio<=0:#en caso de que el entero sea inferior o igual a 0
                                                            print('El precio debe ser mayor a 0')
                                                            continue
                                                    else:
                                                        print(f'El precio debe ser un numero\n')#en caso de ingresar valores diferentes a numeros
                                                        continue
                                            
                                                elif op==3:#editar el stock
                                                    nuevo_stock=input('Ingrese el nuevo stock del producto: ')#se pide el nuevo stock
                                                    if nuevo_stock=="":#si el nuevo stock es vacio se deja como estaba antes
                                                        producto.stock=producto.stock#se hace la asignacion correspondiente
                                                        print(f'El stock del producto {producto.nombre} quedo igual: {producto.stock}\n')#se muestra el mensaje
                                                        continue#vuelve al menu de los atributos a editar
                                                    if nuevo_stock.isdigit():#se verifica que el nuevo precio sea un numero
                                                        nuevo_stock=int(nuevo_stock)#si es un numero lo convierte a entero                

                                                        if nuevo_stock>=0:#en caso de que sea mayor o igual a 0
                                                            trabajador.editar_productos(inventario,id_p,nuevo_stock=nuevo_stock)#el nuevo stock se agrega correctamente
                                                            continue
                                                    
                                                        elif nuevo_stock<0:#en caso de que sea inferior a 0 o sea numeros negativos
                                                            print('El stock debe ser mayor o igual a 0')
                                                            continue
                                                    else:
                                                        print('El stock debe ser un numero')
                                                        continue
                                                                    
                                                elif op==4:#editar categoria
                                                    nueva_categoria=input('Ingrese la nueva categoria del producto: ')
                                                    if nueva_categoria=="":#si la categoria esta vacia se deja como antes
                                                        print(f'La categoria del producto {producto.nombre} quedo igual: {producto.categoria}')#se muestra el mensaje
                                                        continue
                                                    if not es_letras_y_espacios(nueva_categoria):#se hace la validacion de que contenga letras y espacios
                                                        print('La categoria debe contener solo letras')
                                                        continue
                                                    else:#en caso de que la validacion sea correcta
                                                        trabajador.editar_productos(inventario,id_p,nueva_categoria=nueva_categoria)#procede a cambiar el estado de la categoria
                                                        continue
                                    
                                                elif op==5:#volver al menu anterios
                                                    break#rompe el codigo
                                                                                              
                                    elif  opcion_inventario == 4:  #ver inventario     
                                        inventario.mostrar_inventario()
                                           
                                    elif opcion_inventario==5:
                                        print('Regresando al menu anterior....')
                                        break
                                       
                            elif opcion_gestion == 2: #REGISTRAR COMPRAS DEL LOCAL
                            # Aquí llamaríamos a la función que maneja las compras, pasando 'usuario' e 'inventario'.
                            #COMPRAS ENTRADAS DE PRODUCTOS POR PARTE DE LOS PROVEEDORES
                              while True:
                                print('\n === REGISTRAR COMPRAS ===')#menu de compras
                                print(f'Bienvenido usuario {usuario_autenticado.nombre}')#usuario que usa el sistema
                                print('1)Registrar compras de productos')#registrar compras en las facturas
                                print('2)Ver facturas de compras')#permite ver todas facturas creadas
                                print('3)Volver al menu anterior')#regresa al menu anterior a esteKT
                                
                                try:
                                    op_compras=int(input('Ingrese una opcion a ejecutar: '))#opciones del menu de compras
                                except:
                                    print('Ingrese un numero valido')#en caso de ingresar letras
                                    continue#volver a pedir una opcion
                                
                                if op_compras<1 or op_compras>3:#en caso de poner numeros mas grandes o menores a 0
                                    print('Opcion fuera de rango')
                                    continue#volver a pedir una opcion
                                
                                elif op_compras==1:#registrar compras/generar facturas de compras
                                    id_compra=inventario.generar_id_compra()#generar el id de cada factura de compra
                                    factura=Compra(id_compra) #crear el objeto de compra (factura)
                                    confirmada=False 
                                    while True:                                        
                                        #facturas individuales cada una de las facturas
                                        print(f'\n=== FACTURA DE COMPRA {id_compra}===')#aca se muestra el numero de la factura a la que le vamos añadir productos
                                        print('1)Agregar productos a la compra')#añadir productos a la factura (ya sea productos nuevos o productos en el inventario)
                                        
                                        #vizualizar cada uno de los productos que hay hasta el momento en esta factura
                                        #se vizualiza con los atributos de la clase detalleCompra (nombre,cantidad a comprar,precio de compra,precio a la venta,total de este producto)
                                        print('2)Ver productos de la compra')
                                        
                                        #aca se confirman los productos de la factura(compra) y se piden los datos del provedor 
                                        #tambien se preguntan si se quiere editar la factura, los datos del proveedor o eliminar alguna informacion
                                        #tambien se advierte que una vez confirmada no se puede editar ni eliminar 
                                        print('3)Confirmar compra')
                                        
                                        #aca se cancela la factura(compra) totalmente tenga o no tenga productos,no se efectua el ID de esa factura y se deja libre 
                                        #para que se pueda usar en la siguiente factura
                                        print('4)Cancelar compra')
                                        
                                        try:
                                            opcion_factura=int(input('Ingrese una opcion: '))#opcion de lo que queremos hacer en el menu interno de cada factura
                                        except:
                                            print('Ingrese un opcion valida\n')#en caso de ingresar letras
                                            continue#regresa a pedir la opcion
                                        
                                        if opcion_factura<1 or opcion_factura>4:#en caso de ingresar numeros superiores o inferiores a las opciones
                                            print('opcion fuera de rango')
                                            continue#vuelve a pedir la opcion
                                        
                                        
                                        elif opcion_factura==1: #aca empieza a agregar productos a la factura de compra
                                           
                                            producto_buscar=input('\nIngrese el nombre del producto: ').strip()#pedimos el nombre del producto a comprar
                                        
                                            if not producto_buscar:#si se agrega un nombre vacio 
                                                print('Este campo es obligatorio. Ingrese un nombre')#se lanza un mensaje de que el nombre es obligatorio
                                                continue#y vuelve a pedirlo
                                            if not es_letras_y_espacios(producto_buscar):#verificacion de los datos para nombre del producto
                                                print('Error: Ingrese unicamente letras')#enc caso de ingresar numeros y caracteres especiales
                                                continue#volvemso al inicio
                                            
                                            #apartado para verificar los productos duplicados en la misma factura
                                            encontrado_en_factura= False #bandera para verificar si hay duplicados
                                            for detalle in factura.lista_detalles:#recorrer la lista donde se guardaran los productos de cada factura(compra)
                                                
                                                #se guarda cada detalle(producto) guardado en la factura(compra)
                                                nombre_actual = detalle.producto.nombre.lower().replace(" ", "")
                                                nombre_nuevo = producto_buscar.lower().replace(" ", "")#el nombre del producto que nosotros estamos comrprando se guarda
                                                #en esta variable
    
                                                if nombre_actual == nombre_nuevo:#se compara ambas varibales para verificar duplicados
                                                    encontrado_en_factura= True #si encunetra duplicados activa la bandera como positiva
                                                    break#deja de buscar porque ya encontro

                                            if encontrado_en_factura:#si encuentra que se esta intentado agregar un producto previamente ya agregado a la factura
                                                print(f"\n{producto_buscar} ya está en la factura.No se permiten productos duplicados")#lanza la advertencia  de que el producto ya esta en esa factura y no se permite duplicados
                                                continue#regresa al menu de la factura
                                            
                                            
                                            #BUSCAR SI EL PRODUCTO YA ESTA EN EL INVENTARIO (o sea si ya esta previamente registrado)
                                            
                                            #producto_encontrado sera la variable para agregar productos a la factura(compra)
                                            #sea nuevo o no nuevo el producto
                                            producto_encontrado=None#no se sabe si existe entonces se deja en None (vacio)
                                            for producto in inventario.lista_productos:#recorre todos los productos del inventario
                                            #si algun nombre que este registrado en el inventario sin importar espacios o mayusculas/minusculas
                                            #coincide con el producto que estamos ingresado sin importar espacios/mayusculas/minusculas
                                                if producto.nombre.lower().replace(" ","")==producto_buscar.lower().replace(" ",""):
                                                    producto_encontrado=producto#si lo encuentra la vandera que estaba en None pasa a ser ese producto encontrado en
                                                    #inventario
                                                    break#deja de buscar porque ya lo encontro
                                                
                                            if producto_encontrado:#si el producto ya se encuentra previamente registrado
                                                #solo tendremos que pedir los atributos de la clase detalleCompra 
                                                # objeto producto(el que encontramos),cantidad a comprar de ese producto,precio al cual compramos ese prodcuto
                                                #precio al cual vamos a vender ese producto 
                                                #si la factura(compra) de estos productos (o sea ya previamente registrados en inventario) se confirma
                                                #la cantidad comprada y el previo a la venta se deben actualizar en el inventario
                                                print(f'\nProducto "{producto_encontrado.nombre}" encontrado en inventario.')#se lanza un mensaje de que se encontro
                                                #el producto en el inventario y tambien se muestra la cantidad actual y el precio a la venta por lo mencionado anteriormente
                                                es_nuevo = False  #se crea una bandera para identificar que el producto no es nuevo                                          
                                            
                                                
                                                
                                                #aqui solo se piden los atributos de la clase detalleCompra
                                                #el objeto producto ya lo tenemos porque lo encontramos
                                                
                                                while True:#atributo cantidad de la clase detalleCompra
                                                    #cantidad a comprar del producto
                                                    #en caso de confirmarse el producto esto debe sumar al stock y actualizarse en el inventario
                                                    cantidad_comprar=input(f'Ingrese la cantidad a comprar de {producto_encontrado.nombre}: ')
                                                    
                                                    if not cantidad_comprar:#en caso de que sea una cantidad vacia
                                                        print('Este campo es obligatorio.')
                                                        continue#reinicia el bucle
                                                    if not cantidad_comprar.isnumeric():#en caso de que no contenga numero
                                                        print('Ingrese unicamente numeros')
                                                        continue
                                                    
                                                    cantidad_comprar=int(cantidad_comprar)
                                                    if cantidad_comprar<=0:
                                                        print('Ingresa una cantidad mayor a 0 ')
                                                        continue#reinicia el while
                                                    
                                                    break#solo llega aca si la cantidad pasa todas las pruebas
                                                
                                                
                                                while True:
                                                    #precio unitario de compra atributo de la clse detalleCompra
                                                    precio_compra=input(f"Precio de compra del producto {producto_buscar}: ").strip()
                                                    if not precio_compra:#precio vacio 
                                                        print("Este campo es obligatorio. Ingrese un precio")#mensaje de advertencia
                                                        continue#vuelve a pedir el precio
                                    
                                                    if not precio_compra.isdigit():
                                                        print('Ingrese un precio numerico sin espacios ni puntos ni comas')
                                                        continue#vuelve a pedir el precio
                                                    #si el precio no es vacio
                                                    precio_compra=float(precio_compra)#intentar pasarlo a numero flotante
                                                    if precio_compra<=0:#si el precio es inferior o igual a 0 
                                                        print('Precio incorrecto, ingrese un precio mayor a 0')
                                                        continue#vuelve al while
                                                    else:#si llego aqui el precio es totalmente correcto
                                                        break

                                                
                                                while True: #precio de venta al publico atributo de la clase detalleCompra
                                                    #en caso de confirmarse el producto esto debe actualizarse en el inventario
                                                    precio_venta=input("Precio a la venta del producto: ").strip()
                                                    if not precio_venta:#precio vacio 
                                                        print("Este campo es obligatorio. Ingrese un precio")#mensaje de advertencia
                                                        continue#vuelve a pedir el precio
                                    
                                                    if not precio_venta.isdigit():
                                                        print('Ingrese un precio numerico sin espacios ni puntos ni comas')
                                                        continue#vuelve a pedir el precio
                                                    #si el precio no es vacio
                                                    precio_venta=float(precio_venta)#intentar pasarlo a numero flotante
                                                    if precio_venta<=0:#si el precio es inferior o igual a 0 
                                                        print('Precio incorrecto, ingrese un precio mayor a 0')
                                                        continue#vuelve al while
                                                    else:#si llego aqui el precio es totalmente correcto
                                                        break
                                                

                                            # en caso de que el producto no exista o no este previamente registrado en el inventario
                                            else:
                                                #se lanza un mensaje de que el producto se registrara totalmente nuevo
                                                print(f'\nEl producto {producto_buscar} no existe en el inventario. Se registrará uno nuevo.')

                                                    #empezamos a pedir los datos para crear un producto nuevo
                                                    
                                                    #el nombre del producto sera el mismo que registramos al principio
                                                    
                                                    #validamos la categoria (que vendria siendo un atributo de cada producto como se ve en la creacion)
                                                while True:#Validacion de la categoria del produto
                                                    categoria=input(f"Categoria del producto {producto_buscar}: ").strip()
                                                    #La función 'es_letras_y_espacios' verifica que el nombre contenga solo letras y espacios, y que no esté vacío.
                                                    if  not categoria:#en caso de categoria vacia
                                                        print('Este campo es obligatorio. Ingrese una categoria')
                                                        continue#vuelve a pedir la categoria
                                                    if not es_letras_y_espacios(categoria):#se verifica que no contenga ni numeros ni caracteres especiales
                                                        print('Error: Categoria invalida. Ingrese unicamente letras y espacios')
                                                        continue#reinicia el bucle
                                                    break#si las validaciones son correctas
                                                
                                                
                                                #ahora ponemos los atributos del objeto detalleCompra
                                                while True:
                                                    #cantidad a comprar del producto
                                                    cantidad_comprar=input(f'Ingrese la cantidad a comprar de {producto_buscar}: ')
                                                    
                                                    if not cantidad_comprar:#en caso de que sea una cantidad vacia
                                                        print('Este campo es obligatorio.')
                                                        continue#reinicia el bucle
                                                    if not cantidad_comprar.isnumeric():#en caso de que no contenga numero
                                                        print('Ingrese unicamente numeros')
                                                        continue
                                                    
                                                    cantidad_comprar=int(cantidad_comprar)
                                                    if cantidad_comprar<=0:
                                                        print('Ingresa una cantidad mayor a 0 ')
                                                        continue#reinicia el while
                                                    
                                                    break#solo llega aca si la cantidad pasa todas las pruebas
                                                
                                                
                                                while True:
                                                    #precio unitario de compra
                                                    precio_compra=input(f"Precio de compra del producto {producto_buscar}: ").strip()
                                                    if not precio_compra:#precio vacio 
                                                        print("Este campo es obligatorio. Ingrese un precio")#mensaje de advertencia
                                                        continue#vuelve a pedir el precio
                                    
                                                    if not precio_compra.isdigit():
                                                        print('Ingrese un precio numerico sin espacios ni puntos ni comas')
                                                        continue#vuelve a pedir el precio
                                                    #si el precio no es vacio
                                                    precio_compra=float(precio_compra)#intentar pasarlo a numero flotante
                                                    if precio_compra<=0:#si el precio es inferior o igual a 0 
                                                        print('Precio incorrecto, ingrese un precio mayor a 0')
                                                        continue#vuelve al while
                                                    else:#si llego aqui el precio es totalmente correcto
                                                        break

                                                
                                                while True: #precio de venta al publico
                                                    precio_venta=input("Precio a la venta del producto: ").strip()
                                                    if not precio_venta:#precio vacio 
                                                        print("Este campo es obligatorio. Ingrese un precio")#mensaje de advertencia
                                                        continue#vuelve a pedir el precio
                                    
                                                    if not precio_venta.isdigit():
                                                        print('Ingrese un precio numerico sin espacios ni puntos ni comas')
                                                        continue#vuelve a pedir el precio
                                                    #si el precio no es vacio
                                                    precio_venta=float(precio_venta)#intentar pasarlo a numero flotante
                                                    if precio_venta<=0:#si el precio es inferior o igual a 0 
                                                        print('Precio incorrecto, ingrese un precio mayor a 0')
                                                        continue#vuelve al while
                                                    else:#si llego aqui el precio es totalmente correcto
                                                        break
                                                
                                                     
                                                
                                                #creamos el nuevo producto (temporal) sin agregarlo a inventario aun 
                                                id_nuevo_producto=inventario.generar_id_productos()#generador de Ids para los productos creados
                                                #objeto de tipo producto (se agrefa el ID generado,el nombre pues es el mismo que ingremos al principio
                                                # precio=0 por ahora,)
                                                #producto encontrado sera el nuevo producto(agregado temporalmente a la factura)
                                                producto_encontrado=Productos(id_nuevo_producto,producto_buscar,0,categoria,0)#
                                                es_nuevo=True
                                            
                                            
                                            #######################
                                            # crear el detalle(producto) y se agrega a la factura(compra)
                                            
                                            #objeto de tipo detalleCompra donde se crearan las facturas(compras) con los productos
                                            #producto encontrado 
                                            detalle = DetalleCompra(producto_encontrado, cantidad_comprar, precio_compra, precio_venta)
                                            # le agregamos un atributo extra al objeto detalle llamado es_nuevo
                                            # es_nuevo es True si el producto no existia en inventario y False si ya existia
                                            # esto lo necesitamos despues al confirmar para saber que hacer con cada producto:
                                            # - si es_nuevo=True → agregar el producto al inventario
                                            # - si es_nuevo=False → solo sumarle stock y actualizar precio de venta
                                            detalle.es_nuevo = es_nuevo
                                            
                                            
                                            # agregar_detalle es un metodo de la clase Compra
                                            # lo que hace es meter este detalle dentro de factura.lista_detalles
                                            # es como escribir una fila nueva en la factura
                                            # despues de esto len(factura.lista_detalles) aumenta en 1
                                            factura.agregar_detalle(detalle)
                                            
                                            # mensaje de confirmacion visual para el usuario
                                            # usa el nombre del producto y el ID de la factura actual
                                            print(f'\n✓ "{producto_encontrado.nombre}" agregado a la factura {id_compra}.')       
                                            continue
                                        # continue vuelve al inicio del while True
                                        # esto hace que se muestre nuevamente el menu:
                                        # 1) Agregar productos a la compra
                                        # 2) Confirmar compra
                                        # 3) Cancelar compra
                                               
                                                
                                                
                                        #VER PRODUCTOS REGISTRADOS EN LA FACTURA
                                        elif opcion_factura==2:
                                            if len(factura.lista_detalles)==0:#se verifica que hayan productos en la factura
                                                print('\nNo hay productos registrados en esta compra')#si no hay productos se lanza un mensaje
                                                continue #regresa al menu anterior
                                            
                                                
                                            
                                            #encabezado de la tabla
                                            print(f'\n=== PRODUCTOS EN LA FACTUA {id_compra} ===')# se muestra en que factura estamos
                                            # las f-strings con :<N alinean el texto a la izquierda ocupando N caracteres
                                            # esto hace que todas las columnas queden alineadas visualmente
                                            print(f'{"#":<5} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                            print('-'*110)#linea separadora de 100 guiones
                                            
                                            # recorremos cada detalle(producto) de la factura y mostramos sus datos
                                             # acumulador del total general de la factura
                                             #empieza en 0 y aumenta conforme va recorriendo cada detalle(producto de la factura)
                                            total_factura = 0 
                                            
                                            # enumerate recorre la lista y nos da dos cosas a la vez:
                                            # i = el numero de fila (empieza en 1 gracias al segundo parametro)
                                            # detalle = el objeto DetalleCompra de esa posicion
                                            for i, detalle in enumerate(factura.lista_detalles, 1):#el 1 es le segundo parametro que hace que i empiece en 1
                                                
                                                # detalle.subtotal ya viene calculado desde la clase DetalleCompra
                                                # se calculo automaticamente cuando se creo el objeto: cantidad_compra * precio_compra
                                                # entonces no necesitamos calcularlo aqui, solo sumarlo al total
                                                total_factura += detalle.subtotal
                                                
                                                
                                                #en las banderas de agregar producto, esta funcion determina si un producto fue registrado nuevo(True)
                                                # o si ya existia antes en el inventario(False)
                                                if detalle.es_nuevo:#si el producto es nuevo
                                                    tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                else:#de lo contrario si el producto ya se encontraba en el inventario
                                                    tipo="Producto de Inventario"#se marca como producto proveniente de inventario
        
                                                    # mostramos cada columna de la fila con el mismo formato de alineacion
                                                    # detalle.producto.nombre  → accedemos al objeto Producto dentro del DetalleCompra
                                                    # tipo hace referecencia a que tipo de producto es si estaba en inventario o es nuevo
                                                    # detalle.cantidad_compra  → cuantas unidades se compraron
                                                    # detalle.precio_compra    → precio al que se le compro al proveedor
                                                    # detalle.precio_venta_nuevo → precio al que se va a vender al publico
                                                    # detalle.subtotal         → total de ese producto (cantidad * precio_compra)
                                                print(f'{i:<5} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')

                                            print('-' * 110)#linea separadora final
                                            
                                                # mostramos el total general de toda la factura
                                                # :<91 empuja el texto "TOTAL COMPRA:" hacia la izquierda para que el valor
                                                # quede alineado con la columna Total de arriba
                                            print(f'{"TOTAL COMPRA:":<91} ${total_factura}')
                                            continue   
                                        
                                        
                                        #CONFIRMAR COMPRA
                                        elif opcion_factura==3:
                                            pass        
                                                
    
                                                

                                                
                                        elif opcion_factura==4:
                                            inventario.liberar_id_compra()
                                            print('Compra cancelada.')
                                            break
                                        break

                                            
                
                
                
                                elif op_compras==2:
                                    pass 
                                #se muestran todas las facturas que se hayan creado
                                elif op_compras==3:#volver al menu anterior
                                    break
                            
                        
                            elif opcion_gestion == 3:
                                # Aquí llamaríamos a la función que maneja las ventas, pasando 'usuario' e 'inventario'.
                                pass  # Reemplaza con la llamada a tu función de gestión de ventas
                            elif opcion_gestion == 4:
                                print(f"¡Hasta luego, {usuario_autenticado.nombre}!")
                                break
                    else:
                        print("\nError: El número de documento o la contraseña son incorrectos.")
            #Cerrar el sistrema
        elif op_inicio==3:#Si el usuario elige 3 en el menú principal, imprimimos un mensaje y salimos
            print("Gracias por usar el sistema")
            break
            
            




            
            