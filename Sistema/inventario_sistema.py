from Modelos.inventario import Inventario
from Modelos.usuarios import Usuarios
from Modelos.productos import Productos
from Modelos.compras import Compra
from Modelos.detalleCompra import DetalleCompra
from utils import es_letras_y_espacios
from Modelos.proveedores import Proveedor

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
                                        #verificamos que el inventario tenga productos antes de continuar
                                        # si esta vacio no tiene sentido pedir un codigo porque no hay nada que modificar
                                        if len(inventario.lista_productos) == 0:
                                            print('\nNo hay productos registrados en el inventario.')
                                            continue  # regresa al menu anterior sin hacer nada mas
                                        
                                        
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
                                                            print(f'EL nombre del producto {producto.nombre} quedo igual: {producto.nombre}')#se da aviso de que el nombre quedo igual
                                                            break# y se rompe el ciclo para el nombre
                                                        if not es_letras_y_espacios(nuevo_nombre):#si el nombre no contiene letras se da aviso
                                                            print('El nuevo nombre debe contenes solo letrasy')#se repite el ciclo hasta que se ingrese un nombre valido
                                                            continue
                                                        existe=False
                                                        for p in inventario.lista_productos: #p -> producto
                                                            if p.nombre.lower().replace(" ","")==nuevo_nombre.lower().replace(" ",""):
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
                                    factura_cancelada=False
                                    factura_confirmada=False
                                    inventario.detalle_id=1 #se inicia el id de cada detalle en 1 para que siempre que se cree un nuevo de talle en las facturas
                                    #inicien en 1
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
                                                #id_nuevo_producto sera NONE mientras el producto se confirma para inventario
                                                #objeto de tipo producto (se agrefa el ID generado,el nombre pues es el mismo que ingremos al principio
                                                # precio=0 por ahora,)
                                                #producto encontrado sera el nuevo producto(agregado temporalmente a la factura)
                                                producto_encontrado=Productos(None,producto_buscar,0,categoria,0)#
                                                es_nuevo=True#bandera para controlar los productos nuevos en la factura
                                            
                                            
                                            #######################
                                            # crear el detalle(producto) y se agrega a la factura(compra)
                                            
                                            #objeto de tipo detalleCompra donde se crearan las facturas(compras) con los productos
                                            #producto encontrado 
                                            id_detalle=inventario.generar_id_detalle()#identificador de cada detalle dentro de una factura
                                            detalle = DetalleCompra(id_detalle,producto_encontrado, cantidad_comprar, precio_compra, precio_venta)
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
                                            print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                            print('-'*110)#linea separadora de 100 guiones
                                            
                                            # recorremos cada detalle(producto) de la factura y mostramos sus datos
                                             # acumulador del total general de la factura
                                             #empieza en 0 y aumenta conforme va recorriendo cada detalle(producto de la factura)
                                            total_factura = 0 
                                            
                                            # enumerate recorre la lista y nos da dos cosas a la vez:
                                            # i = el numero de fila (empieza en 1 gracias al segundo parametro)
                                            # detalle = el objeto DetalleCompra de esa posicion
                                            for detalle in factura.lista_detalles:#el 1 es le segundo parametro que hace que i empiece en 1
                                                
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
                                                print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')

                                            print('-' * 110)#linea separadora final
                                            
                                                # mostramos el total general de toda la factura
                                                # :<91 empuja el texto "TOTAL COMPRA:" hacia la izquierda para que el valor
                                                # quede alineado con la columna Total de arriba
                                            print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                            continue   
                                        
                                        
                                        #CONFIRMAR COMPRA
                                        elif opcion_factura==3:#aca se confirman los prodcutos añadidos a esta factura
                                            
                                            if len(factura.lista_detalles)==0:#recorre la lista para verificar que no hayan vacios
                                                print('\nNo puedes confirmar una compra sin productos dentro')
                                                continue
                                            
                                            
                                            #importamos datetime para obtener la fecha y la hora actual
                                            from datetime import datetime
                                            #nos servira para buscar las facturas en la lista de facturas
                                            fecha_hora=datetime.now().strftime('%d/%m/%Y %H:%M:%S')#obtenemos la fecha y hora exactas
                                            
                                            #encabezado de la factura
                                            print(f'CONFIRMACION DE FACTURA {id_compra}.'.center(110))
                                            print('-'*110)
                                            print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')#informacion general
                                            print('-'*110)
                                            print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                            print('-'*110)

                                            
                                            
                                            
                                            #filas de cada producto
                                            total_factura=0#el total de la factura inicia en 0
                                            for detalle in factura.lista_detalles:#recorre todos los detalles(productos) guardados en la factura
                                                total_factura+=detalle.subtotal#se calcula el total directamente desde la clase de detalles
                                                        
                                                if detalle.es_nuevo:#si el producto es nuevo
                                                    tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                else:#de lo contrario si el producto ya se encontraba en el inventario
                                                    tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                    
                                                    
                                                print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')


                                            print('-'*110)
                                            print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                            print('-'*110)
                                            print('\n')


                                            #DATOS DEL PROVEDOR DE ESA FACTURA
                                            #aqui agregaremos los datos del provedor o la persona a la cual le estamos haciendo la compra
                                            while True: #Bucle para validar que se ingrese un nombre correctament
                                                nombre_proveedor= input("Ingrese el nombre del proveedor:  ")#nombre del proveedor
                                                    #La función 'es_letras_y_espacios' verifica que el nombre contenga solo letras y espacios, y que no esté vacío.
                                                if not es_letras_y_espacios(nombre_proveedor) or nombre_proveedor is None:#verificacion de los datos para nombre de administrador
                                                    print("Nombre invalido. Use solo letras y espacios")
                                                else:
                                                    break
            
                                            while True: #bucle para validar que se ingrese un documento correctamente
                                                documento_proveedor= input(f"Registre el documento del proveedor {nombre_proveedor}: ")#documento del provedor
                                                if not documento_proveedor: #documento vacio
                                                    print('Debes ingresar un documento. Este campo es obligatorio para el registro')
                                                    continue #reiniciar al while
                                                elif not documento_proveedor.isdigit():
                                                    print('Ingrese unicamente numeros')
                                                    continue #reiniciar el while
                
                                                elif len(documento_proveedor)>=8 and len(documento_proveedor)<=10:#si el documento contiene de 8 a 10 numeros
                                                    try:
                                                        documento_proveedor=int(documento_proveedor)#convertimos a entero cuando sean validos
                                                        #validar si existe ya en la base de datos
                                                        existe=False#variable para verificar si existe o no
                                                        for usuario in inventario.usuarios_registrados:
                                                            if usuario.documento ==documento_proveedor:
                                                                existe=True
                                                                break#dejarlo de buscar si lo encuentra
                                                        if existe:
                                                            print(f'El documento {documento_proveedor} No es correcto. Intente nuevamente')
                                                            #no hay break aqui asi que el while True se repite
                                                        else:
                                                            #paso todas las pruebas
                                                            #documento=documento #guardamos el valor validado
                                                            break   #rompe el while y pasa al siguiente requisito    
                
                                                    except:
                                                        print('Ingrese el numero de documento sin espacios ni puntos')
                                                        continue
                                                    else:
                                                        print('Ingrese un documento con minimo 8 numeros y maximo 10 numeros')
               
               
                                            while True: #bucle para validar que se ingrese un telefono correctamente
                                                telefono_proveedor= input(f"Registre el telefono del provedor {nombre_proveedor}: ")
                                                if not telefono_proveedor:#telefono vacio
                                                    print('Debes ingresar un telefono. Este campo es obligatorio para el registro')
                                                    continue# reiniciar el while
                                                elif not telefono_proveedor.isdigit():
                                                    print('Ingrese unicamente numeros')
                                                    continue#reinicie el while
                                                elif len(telefono_proveedor)==10:#si la longitud del telefono es 10
                                                    try:
                                                        telefono_proveedor=int(telefono_proveedor)#convertios a entero el numero de telefoono
                                                        #validar si existe ya en la base de datos
                                                        existe=False#variable para verificar si existe o no
                                                        for usuario in inventario.usuarios_registrados:
                                                            if usuario.telefono==telefono_proveedor:
                                                                existe=True
                                                                break#dejarlo de buscar si lo encuentra
                                                        if existe:
                                                            print(f'El telefono {telefono_proveedor} No es correcto. Intente nuevamente')
                                                            #el while se repite
                    
                                                        else:
                                                        #si llegamos aqui pasamos todas las pruebas
                                                            break# rompe el codigo y guarda el telefono
                                                    except:
                                                        print('Ingrese el telefono sin espacios ni puntos')
                                                        continue
                                                else:
                                                    print('Ingrese un telefono con maximo 10 numeros')




                                            #una vez validados los atributos del objeto de tipo proveedor
                                            #creamos el objeto de tipo proveedor al que pertenece esta factura
                                            proveedor=Proveedor(nombre_proveedor,documento_proveedor,telefono_proveedor)
                                                     
                                            #MENU DE CONFIRMACION DE FACTURA
                                            while True:#menu para la confirmacion de facturas(compras)
                                                                                                
                                                #encabezado de la factura
                                                #mostramos como quedaria la factura para hacer su respectiva confirmacion
                                                #o edicionde algun elemento dentro de ella
                                                print('\n')
                                                print(f'CONFIRMACION DE FACTURA {id_compra}.'.center(110))
                                                print('-'*110)
                                                print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                print('-'*110)
                                                print(f'Proveedor:{proveedor.nombre_empresa}  |  Telefono: {proveedor.telefono}  |  NIT/CC: {proveedor.documento}')
                                                print('-'*110)
                                                print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                print('\n')
                                                total_factura=0
                                                for detalle in factura.lista_detalles:
                                                    total_factura+=detalle.subtotal
                                                            
                                                    if detalle.es_nuevo:#si el producto es nuevo
                                                        tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                    else:#de lo contrario si el producto ya se encontraba en el inventario
                                                        tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                        
                                                        
                                                    print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                print('-'*110)
                                                print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                print('-'*110)
                                                print('!!! IMPORTANTE: Revise muy bien la informacion de la factura.'.center(110))#mensaje de advertecia antes de confirmar la factura
                                                print('    Una vez confirmada, no se podra eliminar, ni editar ¡¡¡'.center(110))
                                                print('\n')
                                                print(f'MENU DE CONFIRMACION FACTURA {id_compra} === ')
                                                print('1)Editar informacion de productos')
                                                print('2)Editar informacion de proveedor')
                                                print('3)Confirmar compra')
                                                print('4)Cancelar compra')
                                                
                                                
                                                #se hacen las respectivas validaciones
                                                try:
                                                    op_confir_factura=int(input('Ingrese una opcion: '))#opcion de lo que queremos hacer en el menu interno de cada factura
                                                except:
                                                    print('Ingrese un opcion valida\n')#en caso de ingresar letras
                                                    continue#regresa a pedir la opcion
                                        
                                                if op_confir_factura<1 or op_confir_factura>4:#en caso de ingresar numeros superiores o inferiores a las opciones
                                                    print('opcion fuera de rango')
                                                    continue#vuelve a pedir la opcion
                                                
                                                
                                                #EDITAR INFORMACION DE PRODUCTOS
                                                elif op_confir_factura==1:
                                                    #aca se va poder acomodar la informacion de los detalles(productos en factura)
                                                    #corregir los atributos de los productos o incluso eliminarlos de la factura
                                                    while True:
                                                        #se muestra unicamente la informacionde los productos en la factura
                                                        print(f'INFORMACION DE LOS PRODUCTOS EN LA FACTURA {id_compra}'.center(110))
                                                        print('-'*110)
                                                        print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                        print('-'*110)
                                                        print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                        total_factura=0
                                                        for detalle in factura.lista_detalles:
                                                            total_factura+=detalle.subtotal
                                                        
                                                            if detalle.es_nuevo:#si el producto es nuevo
                                                                tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                            else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                    
                                                    
                                                            print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                        print('-'*110)
                                                        print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                        print('-'*110)
                                                        print('\n')
                                                    
                                                    
                                                        #EDITAR INFORMACION DE PRODUCTOS
                                                        #submenu para editar informacion o eliminar productos en la factura
                                                        print('Editar informacion de productos')
                                                        print('1)Editar productos de la factura')
                                                        print('2)Eliminar productos de la factura')
                                                        print('3)Regresar al menu anterior')
                                                        
                                                        
                                                         
                                                        #se hacen las respectivas validaciones
                                                        try:
                                                            #variable del menu del menu EDITAR informacion de productos
                                                            op_editar_infor=int(input('Ingrese una opcion: '))#opcion de lo que queremos hacer en el menu interno de cada factura
                                                        except:
                                                            print('Ingrese un opcion valida\n')#en caso de ingresar letras
                                                            continue#regresa a pedir la opcion
                                        
                                                        if op_editar_infor<1 or op_editar_infor>3:#en caso de ingresar numeros superiores o inferiores a las opciones
                                                            print('opcion fuera de rango')
                                                            continue#vuelve a pedir la opcion
                                                         
                                                         
                                                        elif op_editar_infor==1:#EDITAR LOS ATRIBUTOS DE LOS PRODUCTOS DENTRO DE LA FACTURA
                                                            
                                                            
                                                            # se pide el codigo del producto a editar(codigo que aparece en la factura) si no lo encuentra salta el mensaje de qeu no lo encontro
                                                            # y nuevamente regresa al menu EDITAR INFORMACION DE PRODUCTOS
                                                            #
                                                            print('Editar productos de la factura')
                                                            #se muestra unicamente la informacionde los productos en la factura
                                                            print(f'INFORMACION DE LOS PRODUCTOS EN LA FACTURA {id_compra}'.center(110))
                                                            print('-'*110)
                                                            print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                            print('-'*110)
                                                            print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                            total_factura=0
                                                            for detalle in factura.lista_detalles:
                                                                total_factura+=detalle.subtotal
                                                            
                                                                if detalle.es_nuevo:#si el producto es nuevo
                                                                    tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                                else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                    tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                        
                                                        
                                                                print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                            print('-'*110)
                                                            print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                            print('-'*110)
                                                            print('\n')
                                                        
                                                            # pedir el codigo del detalle a editar
                                                            try:
                                                                codigo_buscar = int(input('\nIngrese el codigo del producto a editar: '))#variable para buscar el codigo a editar
                                                            except:
                                                                print('Ingrese un codigo valido.')
                                                                continue
                                                            
                                                            # buscar el detalle por su id dentro de la factura
                                                            detalle_editar = None #si encuentra algun detalle que coincida lo guardara aqui
                                                            for detalle in factura.lista_detalles:#busca el detall(producto)
                                                                if detalle.id_detalle == codigo_buscar:#si encuentra 
                                                                    detalle_editar = detalle#lo guarda
                                                                    break#y deja de buscar
                                                            
                                                            if detalle_editar is None:  # no se encontro el codigo
                                                                print(f'\nNo se encontro ningun producto con el codigo {codigo_buscar} en la factura.\n')
                                                                continue  # regresa al menu editar informacion
                                                            
                                                            # si lo encontro entramos al menu de edicion
                                                            while True:
                                                                print(f'\n=== EDITAR PRODUCTO: {detalle_editar.producto.nombre} ===\n')
                                                                print('-'*110)
                                                                print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                                print('-'*110)
                                                                print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                                total_factura=0
                                                                for detalle in factura.lista_detalles:
                                                                    total_factura+=detalle.subtotal
                                                                
                                                                    if detalle.es_nuevo:#si el producto es nuevo
                                                                        tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                                    else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                        tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                            
                                                            
                                                                    print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                                print('-'*110)
                                                                print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                                print('-'*110)
                                                                print('\n')
                                                                print(f'\n=== EDITAR PRODUCTO: {detalle_editar.producto.nombre} ===\n')
                                                                print('1) Editar nombre del producto')
                                                                print('2) Editar cantidad del producto')
                                                                print('3) Editar precio de compra')
                                                                print('4) Editar precio de venta')
                                                                print('5) Regresar al menu anterior')
                                                                
                                                                try:
                                                                    op_editar_producto = int(input('Ingrese una opcion: '))
                                                                except:
                                                                    print('Ingrese una opcion valida.')
                                                                    continue
                                                                
                                                                if op_editar_producto < 1 or op_editar_producto > 5:
                                                                    print('Opcion fuera de rango.')
                                                                    continue
                                                                
                                                                elif op_editar_producto == 1:  # editar nombre
                                                                    # solo se puede editar el nombre si es un producto nuevo
                                                                    # si es un producto del inventario el nombre no se puede cambiar
                                                                    if not detalle_editar.es_nuevo:
                                                                        print('\nNo se puede editar el nombre de un producto que ya existe en el inventario.')
                                                                        continue#se devuelve al menu
                                                                    
                                                                    while True:#validaciones para el nuevo nombre
                                                                        nuevo_nombre = input(f'Nuevo nombre de [{detalle_editar.producto.nombre}]: ').strip()
                                                                        if nuevo_nombre=="":#si se deja vacio el sistema dejara el nombre que tiene sin modificar
                                                                            print(f'EL nombre del producto [{detalle_editar.producto.nombre}] quedo igual: {detalle_editar.producto.nombre}')#se da aviso de que el nombre quedo igual
                                                                            break# y se rompe el ciclo para el nombre
                                                                        if not es_letras_y_espacios(nuevo_nombre):
                                                                            print('Solo letras y espacios.')
                                                                            continue#se vuelve a ingresar el nombre
                                                                        
                                                                        #se hace la actualizacion del nombre
                                                                        detalle_editar.producto.nombre = nuevo_nombre
                                                                        print(f'Nombre actualizado a "{nuevo_nombre}".')
                                                                        break
                                                                
                                                                elif op_editar_producto == 2:  # editar cantidad
                                                                    while True:#validaciones para la nueva cantidad
                                                                        nueva_cantidad= input(f'Nueva cantidad de [{detalle_editar.producto.nombre}]: ').strip()
                                                                        if nueva_cantidad=="":
                                                                            print(f'La cantidad del producto [{detalle_editar.producto.nombre}] quedo igual: {detalle_editar.cantidad_compra}')
                                                                            break#se rompe el ciclo para cantidad
                                                                        if not nueva_cantidad.isnumeric():
                                                                            print('Solo numeros enteros.')
                                                                            continue#se vuelve a pedir la cantidad
                                                                        nueva_cantidad = int(nueva_cantidad)
                                                                        if nueva_cantidad <= 0:
                                                                            print('Debe ser mayor a 0.')
                                                                            continue#se vuelve a pedir la cantidad
                                                                        
                                                                        
                                                                        # actualizamos la cantidad y recalculamos el subtotal
                                                                        detalle_editar.cantidad_compra = nueva_cantidad
                                                                        detalle_editar.subtotal = nueva_cantidad * detalle_editar.precio_compra#se vuelve a recalcular el subtotal
                                                                        print(f'Cantidad actualizada a {nueva_cantidad}.')
                                                                        break
                                                                
                                                                elif op_editar_producto == 3:  # editar precio de compra
                                                                    while True:#validaciones para el precio de compra
                                                                        nuevo_precio_compra = input(f'Nuevo precio de compra de [{detalle_editar.producto.nombre}]: ').strip()
                                                                        if nuevo_precio_compra=="":
                                                                            print(f'El precio de compra del producto [{detalle_editar.producto.nombre}] quedo igual: {detalle_editar.precio_compra}')
                                                                            break#rompe el ciclo pra el precio de compra
                                                                        if not nuevo_precio_compra.isdigit():
                                                                            print('Solo numeros sin puntos ni comas.')
                                                                            continue
                                                                        nuevo_precio_compra = float(nuevo_precio_compra)
                                                                        if nuevo_precio_compra <= 0:
                                                                            print('Debe ser mayor a 0.')
                                                                            continue
                                                                        
                                                                        
                                                                        # actualizamos el precio de compra y recalculamos el subtotal
                                                                        detalle_editar.precio_compra = nuevo_precio_compra
                                                                        detalle_editar.subtotal = detalle_editar.cantidad_compra * nuevo_precio_compra#se recalcula el sub total
                                                                        print(f'Precio de compra actualizado a ${nuevo_precio_compra}.')
                                                                        break
                                                                
                                                                elif op_editar_producto == 4:  # editar precio de venta
                                                                    while True:#validaciones para el precio de venta
                                                                        nuevo_precio_venta = input(f'Nuevo precio de venta de [{detalle_editar.producto.nombre}]: ').strip()
                                                                        if nuevo_precio_venta=="":
                                                                            print(f'El precio de venta del producto [{detalle_editar.producto.nombre}] quedo igual: {detalle_editar.precio_venta_nuevo}')
                                                                            break#rompe el ciclo para precio de venta
                                                                        if not nuevo_precio_venta.isdigit():
                                                                            print('Solo numeros sin puntos ni comas.')
                                                                            continue#se vuelve a pedir el precio de venta
                                                                        nuevo_precio_venta = float(nuevo_precio_venta)
                                                                        if nuevo_precio_venta <= 0:
                                                                            print('Debe ser mayor a 0.')
                                                                            continue#se vuelve a pedir el precio de vent
                                                                        detalle_editar.precio_venta_nuevo = nuevo_precio_venta
                                                                        print(f'Precio de venta actualizado a ${nuevo_precio_venta}.')
                                                                        break
                                                                
                                                                elif op_editar_producto == 5:  # regresar
                                                                    break  # sale al menu editar informacion
                                                                                                                   
                                                        elif op_editar_infor==2:#ELIMINAR PRODUCTOS DE LA FACTURA
                                                            
                                                            # advertencia cuando solo queda un producto, ANTES de cualquier accion
                                                            # advertencia cuando solo queda un producto
                                                            if len(factura.lista_detalles) == 1:
                                                                print('\n!!! ADVERTENCIA: La factura solo tiene un producto !!!'.center(110))
                                                                print('Si lo eliminas la factura quedara vacia y sera cancelada automaticamente.\n')
                                                                
                                                                # mostrar el unico producto que queda
                                                                detalle_unico = factura.lista_detalles[0]  # accedemos directamente al unico elemento
                                                                if detalle_unico.es_nuevo:#si el producto es nuevo
                                                                    tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                                else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                    tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                                    
                                                                print(f'\n{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                                print('-' * 110)
                                                                print(f'{detalle_unico.id_detalle:<9} {detalle_unico.producto.nombre:<20} {tipo:<25} {detalle_unico.cantidad_compra:<12} {detalle_unico.precio_compra:<12} {detalle_unico.precio_venta_nuevo:<12} ${detalle_unico.subtotal}')
                                                                print('-' * 110)
                                                                
                                                                # preguntar si desea eliminarlo
                                                                #si se elimina la factura queda vacia por ende tambien se elimina la factura
                                                                while True:
                                                                    continuar = input(f'\n¿Deseas eliminar "{detalle_unico.producto.nombre}"? (si/no): ').strip().lower()
                                                                    if not continuar:#en caso de una respuesta vacia
                                                                        print('Este campo es obligatorio. Ingrese si o no.')
                                                                        continue#se vuelve a preguntar nuevamente
                                                                    if not es_letras_y_espacios(continuar):
                                                                        print('Ingrese unicamente letras.')
                                                                        continue#en caso de ingresar numeros o caracteres especiales
                                                                    if continuar not in ['si', 'no']:
                                                                        print('Opcion invalida. Ingrese si o no.')#en caso de ingresar cualquier cosa diferente a si o no
                                                                        continue
                                                                    break#solo sale cuando se igrese si o no 

                                                                if continuar == 'no':#si se ingresa 'no', no se hace la eliminacion, por ende se cancela la eliminacion
                                                                    print('\nOperacion cancelada.')
                                                                    continue  # regresa al menu editar informacion

                                                                # si dijo si — eliminar y cancelar la factura automaticamente
                                                                factura.lista_detalles.remove(detalle_unico)#se remueve el unico detalle existente en la factura
                                                                inventario.liberar_id_compra()#se libera el ID de la factura , para que pueda ser usado en la siguiente factura
                                                                print(f'\n!!! La factura {id_compra} fue cancelada automaticamente por quedar sin productos !!!'.center(110))
                                                                factura_cancelada = True#se activa la bandera que indica al resto del sistema, la cancelacion de la factura
                                                                break  # sale del while de op_editar_infor

                                                            # pedir el codigo del detalle a eliminar
                                                            #se muestra la informacion de todos los productos en la factura para saber cual eliminar
                                                            print(f'INFORMACION DE LOS PRODUCTOS EN LA FACTURA {id_compra}'.center(110))
                                                            print('-'*110)
                                                            print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                            print('-'*110)
                                                            print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                            total_factura=0
                                                            for detalle in factura.lista_detalles:
                                                                total_factura+=detalle.subtotal
                                                            
                                                                if detalle.es_nuevo:#si el producto es nuevo
                                                                    tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                                else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                    tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                        
                                                        
                                                                print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                            print('-'*110)
                                                            print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                            print('-'*110)
                                                            print('\n')
                                                            try:
                                                                codigo_eliminar = int(input('\nIngrese el codigo del producto a eliminar: '))#codigo del producto dentro de la factura
                                                            except:
                                                                print('Ingrese un codigo valido.')
                                                                continue  # regresa al menu editar informacion

                                                            # buscar el detalle por su id dentro de la factura
                                                            detalle_eliminar = None
                                                            for detalle in factura.lista_detalles:
                                                                if detalle.id_detalle == codigo_eliminar:
                                                                    detalle_eliminar = detalle
                                                                    break#deja de buscar

                                                            # si no se encontro el codigo
                                                            if detalle_eliminar is None:
                                                                print(f'\nNo se encontro ningun producto con el codigo {codigo_eliminar} en la factura.')
                                                                continue  # regresa al menu editar informacion

                                                            # si lo encontro mostramos su informacion antes de confirmar
                                                            if detalle_eliminar.es_nuevo:#si el producto es nuevo
                                                                tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                            else:#de lo contrario si el producto ya se encontraba en el inventario
                                                                tipo="Producto de Inventario"#se marca como producto proveniente de inventario

                                                            print(f'\n{"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                            print('-' * 90)
                                                            print(f'{detalle_eliminar.producto.nombre:<20} {tipo:<25} {detalle_eliminar.cantidad_compra:<12} {detalle_eliminar.precio_compra:<12} {detalle_eliminar.precio_venta_nuevo:<12} ${detalle_eliminar.subtotal}')
                                                            print('-' * 90)
                                                            print(f'\nEl producto sera eliminado de la factura {id_compra}.')
                                                            
                                                            
                                                            #se vuelve a preguntar si se desea confirmar la informacion de este producto
                                                            print('\n')
                                                            print('1)Confirmar eliminacion')
                                                            print('2)Cancelar y volver al menu anterior')

                                                            try:
                                                                op_eliminar = int(input('Ingrese una opcion: '))
                                                            except:
                                                                print('Opcion invalida.')
                                                                continue  # regresa al menu editar informacion

                                                            if op_eliminar < 1 or op_eliminar > 2:
                                                                print('Opcion fuera de rango.')
                                                                continue  # regresa al menu editar informacion

                                                            elif op_eliminar == 1:  # confirmar eliminacion
                                                                nombre_eliminado = detalle_eliminar.producto.nombre  # guardamos nombre antes de eliminar
                                                                factura.lista_detalles.remove(detalle_eliminar)  # eliminamos el detalle de la lista
                                                                print(f'\nProducto "{nombre_eliminado}" eliminado de la factura {id_compra} correctamente.\n')

                                                                # si la factura quedo vacia se cancela automaticamente
                                                                if len(factura.lista_detalles) == 0:
                                                                    inventario.liberar_id_compra()  # devolvemos el ID
                                                                    print(f'\nLa factura {id_compra} quedo sin productos y fue cancelada automaticamente.')
                                                                    factura_cancelada = True  # activamos la bandera
                                                                    break  # sale del while de op_editar_infor

                                                                continue  # regresa al menu editar informacion con cambios reflejados

                                                            elif op_eliminar == 2:  # cancelar
                                                                print('\nEliminacion cancelada.')
                                                                continue  # regresa sin cambios
                                                                                                                
                                                        
                                                        elif op_editar_infor==3:#regresar al menu confirmacion
                                                            break           
                                                
                                                    if factura_cancelada:#si la factura se cancela se rompe todo el codigo y se regresa al menu Registrar compras
                                                        #sin pedir provedores ni nada, ni confirmar
                                                        break
                                            
                                                elif op_confir_factura==2:#EDITAR INFORMACION DEL PROVEEDOR
    
                                                    while True:
                                                        # mostrar informacion actualizada del proveedor antes de cada opcion
                                                        print('\n')
                                                        print(f'EDITAR INFORMACION DEL PROVEEDOR'.center(110))
                                                        print('-' * 110)
                                                        print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                        print('-' * 110)
                                                        print(f'Proveedor: {proveedor.nombre_empresa}  |  Telefono: {proveedor.telefono}  |  NIT/CC: {proveedor.documento}')
                                                        print('-' * 110)
                                                        print('\nEditar informacion del proveedor')
                                                        print('1) Editar nombre del proveedor')
                                                        print('2) Editar telefono del proveedor')
                                                        print('3) Editar documento')
                                                        print('4) Regresar al menu anterior')
                                                        
                                                        try:
                                                            op_editar_prov = int(input('Ingrese una opcion: '))#que se quiere editar del proveedor
                                                        except:
                                                            print('Ingrese una opcion valida.')
                                                            continue#vuelve a pedir que se quiere editar
                                                        
                                                        if op_editar_prov < 1 or op_editar_prov > 4:
                                                            print('Opcion fuera de rango.')
                                                            continue#vuelve a pedir que se quiere editar
                                                        
                                                        elif op_editar_prov == 1:  # editar nombre
                                                            while True:#validaciones para el nombre
                                                                nuevo_nombre = input(f'Nuevo nombre [{proveedor.nombre_empresa}]: ').strip()
                                                                if not nuevo_nombre:#si el nombre queda vacio se deja el que estaba
                                                                    print(f'El nombre quedo igual: {proveedor.nombre_empresa}')
                                                                    break#se rompe el codigo y se regresa al menu de editar proveedor
                                                                elif not es_letras_y_espacios(nuevo_nombre):#en caso de numeros o caracteres especiales
                                                                    print('Solo letras y espacios. Sin cambios.')
                                                                    continue#se vuelve a pedir
                                                                else:#solo llega aca si todo esta bien
                                                                    proveedor.nombre_empresa = nuevo_nombre#actualiza el nuevo nombre
                                                                    print(f'Nombre actualizado a "{nuevo_nombre}".')
                                                                    break#vuelve al menu anterior con la informacion actualizada
                                                                
                                                                
                                                        elif op_editar_prov == 2:  # editar telefono
                                                            while True:#validaciones para el telefono
                                                                nuevo_tel = input(f'Nuevo telefono [{proveedor.telefono}]: ').strip()
                                                                if not nuevo_tel:#si no se ingrea el nombre queda igual
                                                                    print(f'El telefono quedo igual: {proveedor.telefono}')
                                                                    break#se rompe el codigo y se regresa al menu de editar proveedor
                                                                elif not nuevo_tel.isdigit():
                                                                    print('Solo numeros. Sin cambios.')
                                                                    continue#se vuelve a pedir el numero en caso de ingresar letras o caracteres especiales
                                                                elif len(nuevo_tel) != 10:#es caso de que no se ingrese un numero con 10 numeros
                                                                    print('El telefono debe tener 10 numeros. Sin cambios.')
                                                                    continue#se vuelve a pedir el numero de telefono
                                                                else:#solo llega aca si todo esta correcto
                                                                    proveedor.telefono = int(nuevo_tel)#se pasa a entero el numero de telefono
                                                                    print(f'Telefono actualizado a {nuevo_tel}.')
                                                                    break#vuelve al menu anterios con la informacion actualizada
                                                                
                                                                
                                                                
                                                        elif op_editar_prov == 3:  # editar documento
                                                            while True:#validaciones para el docuemnto
                                                                nuevo_doc = input(f'Nuevo documento [{proveedor.documento}]: ').strip()
                                                                if not nuevo_doc:#en caso de quedar vacio se deja como estaba
                                                                    print(f'El documento quedo igual: {proveedor.documento}')
                                                                    break#vuelve al menu anterior con la informacion actualizada
                                                                elif not nuevo_doc.isdigit():#en caso no ingresar numeros
                                                                    print('Solo numeros.')
                                                                    continue#vuelve a pedir el documento
                                                                elif len(nuevo_doc) < 8 or len(nuevo_doc) > 10:#en caso de que el documento sea menor a 8 y mayor a 10
                                                                    print('El documento debe tener entre 8 y 10 numeros.')
                                                                    continue#volver a pedir el documento
                                                                else:#solo llega aca cuando se haya validado satisfactoriamente la informacion
                                                                    proveedor.documento = int(nuevo_doc)#se actualiza en la factura
                                                                    print(f'Documento actualizado a {nuevo_doc}.')#se lanza el mensaje de actualizacion
                                                                    break#se rompre el codigo y vuelve con la informacion actualizada
                                                        elif op_editar_prov == 4:  # regresar
                                                            break  # sale al menu de confirmacion
                                                
                                                elif op_confir_factura==3:#CONFIRMAR COMPRA    
                                                    # mostramos toda la informacion de la factura antes de confirmar
                                                    # para que el usuario pueda ver el resumen final de lo que se va a guardar
                                                    print('\n')
                                                    print(f'FACTURA CONFIRMADA {id_compra}'.center(110))  # titulo centrado
                                                    print('-' * 110)  # linea separadora
                                                    
                                                    # informacion general de la factura: ID, empleado que la creo y fecha/hora
                                                    print(f'Factura: {id_compra} | Empleado: {usuario_autenticado.nombre} | Fecha: {fecha_hora}')
                                                    print('-' * 110)
                                                    
                                                    # informacion del proveedor al que se le hizo la compra
                                                    print(f'Proveedor: {proveedor.nombre_empresa}  |  Telefono: {proveedor.telefono}  |  NIT/CC: {proveedor.documento}')
                                                    print('-' * 110)
                                                    
                                                    # encabezado de la tabla de productos
                                                    print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                    print('-' * 110)
                                                    
                                                    # recorremos todos los detalles(productos) de la factura para mostrarlos
                                                    total_factura = 0  # acumulador del total general, empieza en 0
                                                    for detalle in factura.lista_detalles:
                                                        
                                                        # sumamos el subtotal de cada producto al total general
                                                        # subtotal ya viene calculado desde la clase DetalleCompra (cantidad * precio_compra)
                                                        total_factura += detalle.subtotal
                                                        
                                                        # determinamos el tipo de producto para mostrarlo en la tabla
                                                        if detalle.es_nuevo:#si el producto es nuevo
                                                            tipo="Producto nuevo"#se marca el tipo de producto como nuevo
                                                        else:#de lo contrario si el producto ya se encontraba en el inventario
                                                            tipo="Producto de Inventario"#se marca como producto proveniente de inventario
                                                        
                                                        # mostramos cada fila de la tabla con sus datos alineados
                                                        print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                    
                                                    print('-' * 110)  # linea separadora final
                                                    
                                                    # mostramos el total general de toda la factura
                                                    print(f'{"TOTAL COMPRA:":<95} ${total_factura}')
                                                    print('-' * 110)
                                                    
                                                    # mensaje de confirmacion — avisa que la factura ya no se puede modificar
                                                    print(f'\n!!! La factura {id_compra} ha sido confirmada. No se puede editar ni eliminar !!!'.center(110))
                                                    print('\n')
                                                                                                
                                                    # recorremos todos los detalles de la factura para actualizar el inventario
                                                    for detalle in factura.lista_detalles:
                                                        # factura.lista_detalles es la lista que contiene todos los productos
                                                        # que se agregaron a esta factura
                                                        # cada 'detalle' es un objeto DetalleCompra que contiene:
                                                        # - detalle.producto → el objeto Productos (nombre, codigo, precio, stock, categoria)
                                                        # - detalle.cantidad_compra → cuantas unidades compramos
                                                        # - detalle.precio_compra → a cuanto le compramos al proveedor
                                                        # - detalle.precio_venta_nuevo → a cuanto lo vamos a vender al publico
                                                        # - detalle.es_nuevo → True si es producto nuevo, False si ya estaba en inventario
                                                        
                                                        
                                                        if detalle.es_nuevo:  # si el producto es nuevo
                                                            
                                                            # recien aqui generamos el ID del producto nuevo
                                                            # lo habiamos dejado en None hasta que la factura fuera confirmada
                                                            id_nuevo = inventario.generar_id_productos()
                                                            #lo que hace es acceder al objeto producto de ese detalle y ahi mismo
                                                            #accede a los atributos de ese objeto producto y los asigna
                                                            detalle.producto.codigo = id_nuevo  # le asignamos el ID generado
                                                            
                                                            # asignamos la cantidad comprada como stock inicial del producto
                                                            detalle.producto.stock = detalle.cantidad_compra
                                                            
                                                            # asignamos el precio de venta al publico
                                                            detalle.producto.precio = detalle.precio_venta_nuevo
                                                            
                                                            # la categoria ya fue asignada cuando se creo el producto temporal
                                                            # no necesitamos hacer nada con ella
                                                            
                                                            # finalmente agregamos el producto al inventario
                                                            inventario.lista_productos.append(detalle.producto)
                                                            print(f'Producto nuevo "{detalle.producto.nombre}" agregado al inventario con ID {id_nuevo}.')

                                                        
                                                        else:  # producto que ya existia en el inventario
                                                            # buscamos el producto original en el inventario por su codigo
                                                            # necesitamos encontrar ese producto dentro de inventario.lista_productos
                                                            # para poder modificar sus atributos directamente
                                                            # no podemos usar detalle.producto directamente para modificar el inventario
                                                            # porque detalle.producto es una referencia al objeto que encontramos
                                                            # cuando buscamos en el inventario al principio
                                                            # pero para ser seguros buscamos por codigo
                                                            for producto in inventario.lista_productos:
                                                                 # recorremos toda la lista de productos del inventario
                                                                 # buscando el que tenga el mismo codigo que el producto de este detalle
            
                                                                if producto.codigo == detalle.producto.codigo:
                                                                    # cuando encontramos el producto en el inventario que coincide
                                                                    # con el producto de este detalle, actualizamos sus atributos
                                                                    
                                                                    # ACTUALIZAMOS EL STOCK:
                                                                    # producto.stock es la cantidad que habia antes en inventario
                                                                    # detalle.cantidad_compra es la cantidad que compramos ahora
                                                                    # con += sumamos ambas cantidades
                                                                    # ejemplo: habia 10 en stock y compramos 25
                                                                    # 10 += 25 → producto.stock queda en 35
                                                                    
                                                                    # sumamos la cantidad comprada al stock actual del inventario
                                                                    # ejemplo: tenia 10 en stock, compramos 25 → queda en 35
                                                                    producto.stock += detalle.cantidad_compra
                                                                    
                                                                    # actualizamos el precio de venta con el nuevo precio ingresado en la factura
                                                                    # el precio anterior se reemplaza por el nuevo
                                                                    # ACTUALIZAMOS EL PRECIO DE VENTA:
                                                                    # reemplazamos el precio anterior con el nuevo precio
                                                                    # que ingresamos cuando agregamos el producto a la factura
                                                                    # ejemplo: precio anterior era 2000, nuevo precio es 2500
                                                                    # producto.precio queda en 2500
                                                                    producto.precio = detalle.precio_venta_nuevo
                                                                    
                                                                    print(f'Producto "{producto.nombre}" actualizado en inventario.')
                                                                    print(f'Stock anterior + {detalle.cantidad_compra} unidades compradas = {producto.stock} unidades totales.')
                                                                    print(f'Precio de venta actualizado a ${producto.precio}.')
                                                                    
                                                                    break  # dejamos de buscar porque ya lo encontramos y actualizamos
                                
                                                    
                                                    #marcamos la factura como confirmada
                                                    # PASO 1: marcar la factura como confirmada
                                                    # factura es el objeto Compra que venimos trabajando desde el inicio
                                                    # confirmada es el atributo que acabamos de agregar a la clase Compra
                                                    # al ponerlo en True le decimos al sistema que esta factura ya fue cerrada
                                                    # esto sirve para que en el futuro cuando alguien intente editarla
                                                    # el sistema pueda verificar: "si factura.confirmada == True, no dejes editar"
                                                    factura.factura_confirmada=True #esto  para evitar que se edite o elimina mas adelante
                                                    
                                                    
                                                    #guardamos el total de la factura(total_factura creada desde que se confirmo la factura)
                                                    #o sea a 'factura' en el atributo total_factura le guardamos el total previamente calculado
                                                    # PASO 2: guardar el total en la factura
                                                    # total_factura es la variable que calculamos en el for de arriba
                                                    # sumando detalle.subtotal de cada producto
                                                    # ejemplo: jabon $25000 + colonia $600000 = total_factura $625000
                                                    # factura.total_factura es el atributo de la clase Compra donde guardamos ese valor
                                                    # esto sirve para que cuando consultemos la factura despues
                                                    # no tengamos que recalcular el total, ya lo tenemos guardado
                                                    factura.total_factura=total_factura 
                                                    
                                                    #guardamos el provedor(objeto proveedor creado antes) en la factura
                                                    #en el atributo proveedor de la factura guardamos el objeto proveedor
                                                    # PASO 3: guardar el proveedor en la factura
                                                    # proveedor es el objeto Proveedor que creamos cuando pedimos
                                                    # el nombre, documento y telefono del proveedor
                                                    # factura.proveedor es el atributo de la clase Compra que dejamos en None al inicio
                                                    # aqui le asignamos el objeto proveedor que ya teniamos creado
                                                    # esto une el proveedor con su factura para siempre
                                                    # ejemplo: factura 1 → proveedor "Distribuidora XYZ"
                                                    factura.proveedor=proveedor
                                                    
                                                    #finalmente guardamos la factura en el inventario (almacen de facturas de compra)
                                                    #en el objeto inventario en la lista de compras guardamos los objetos de tipo factura de compras
                                                    # PASO 4: agregar la factura al almacen de facturas
                                                    # inventario.lista_compras es la lista que acabamos de agregar a la clase Inventario
                                                    # .append() es un metodo de las listas de Python que agrega un elemento al final
                                                    # le estamos pasando el objeto factura completo con todo adentro:
                                                    #   - factura.id_factura → el ID de la factura
                                                    #   - factura.proveedor → el objeto proveedor
                                                    #   - factura.lista_detalles → todos los productos con sus datos
                                                    #   - factura.total_factura → el total calculado
                                                    #   - factura.confirmada → True
                                                    # a partir de este momento la factura queda guardada en el sistema
                                                    
                                                    
                                                    factura.fecha_hora=fecha_hora #se guarda la fecha y hora dentro del objeto factura para poder buscar 
                                                    #en la lista de facturas confirmadas
                                                    inventario.lista_compras.append(factura)

                                                    
                                                    print(f'\nFactura {id_compra} guardada correctamente en el almacen de facturas.')
                                                    
                                                    #salimos de todos los menus y volvemos al menu de compras
                                                    factura_confirmada=True
                                                    break
                                                
                                                
                                                
                                                
                                                if factura_confirmada:
                                                    break#sale del while de op_confir_factura
                                                
                                                elif op_confir_factura==4:#CANCELAR COMPRA
                                                    inventario.liberar_id_compra()
                                                    print('\nCompra cancelada.\n')
                                                    break
                                                    
                                                    pass
                                            if factura_cancelada:
                                                break               
                                            if factura_confirmada:
                                                break                
                                                                                            
                                        elif opcion_factura==4:#SE CANCELA LA COMPRA
                                            inventario.liberar_id_compra()
                                            print('\nCompra cancelada.\n')
                                            break
                                                   
                                        # cierre del while True de opcion_factura
                                    if factura_cancelada or factura_confirmada:
                                        continue  # vuelve al menu de compras (op_compras)           
                                                   
                                                   
                                                   
                                                   
                                elif op_compras==2:
                                #se muestran todas las facturas que se hayan creado
                                                                            # verificamos que haya facturas guardadas
                                    if len(inventario.lista_compras) == 0:
                                        print('\nNo hay facturas registradas.')
                                        break
                                        
                                        
                                    while True:#menu para buscar las facturas
                                        print('\n=== VER FACTURAS DE COMPRAS ===')
                                        print('1) Buscar facturas por mes y año')
                                        print('2) Ver todas las facturas')
                                        print('3) Regresar al menu anterior')

                                        try:
                                            op_ver_facturas = int(input('Ingrese una opcion: '))
                                        except:
                                            print('Ingrese un numero valido.')
                                            continue#se devuelve al menu

                                        if op_ver_facturas < 1 or op_ver_facturas > 3:
                                            print('Opcion fuera de rango.')
                                            continue#se devuelve al menu

                                        elif op_ver_facturas == 1:  # BUSCAR POR MES Y AÑO

                                            # verificamos que haya facturas guardadas
                                            if len(inventario.lista_compras) == 0:
                                                print('\nNo hay facturas registradas.')

                                            # en caso contrario pedimos el mes
                                            while True:
                                                try:#PEDIR MES con sus respectivas validaciones
                                                    mes = int(input('Ingrese el mes (1-12): '))
                                                    if mes < 1 or mes > 12:#en caso de ingresar un mes menor o mayor a 12
                                                        print('Mes invalido. Ingrese un numero entre 1 y 12.')
                                                        continue#vuelve a pedir el mes
                                                    break#si se ingresa bien se rompe el ciclo y continua 
                                                except:
                                                    print('Ingrese un numero valido.')
                                                    continue#vuelve a pedir el mes en caso de ingresar letras o caracteres especiales

                                            # pedimos el año
                                            while True:#VALIDACIONES PARA EL AÑO
                                                try:
                                                    anio = int(input('Ingrese el año (ej: 2026): '))
                                                    if anio < 2000 or anio > 2100:#Se pone un limite de años
                                                        print('Año invalido.')
                                                        continue#en caso de ingresar un años fuera del rango
                                                    break#en acaso contrario se rompre el codigo y continua
                                                except:
                                                    print('Ingrese un numero valido.')
                                                    continue#vuelve a pedir el año en caso de ingresar letras o especiales
                                            
                                            
                                            
                                            
                                            
                                            #cuando todas las validaciones sean correctas
                                            # filtramos las facturas que correspondan a ese mes y año
                                            # factura.fecha_hora tiene formato 'dd/mm/yyyy hh:mm:ss'
                                            # dividimos el string por '/' para obtener dia, mes y año
                                            
                                            #en esta lista se guardaran las facturas que correspondan al mes y año que el usuario ingreso
                                            facturas_filtradas = []
                                            
                                            #vamos a recorrer todas las facturas guardadas en el inventario
                                            #la variable factura_guardada es cada objeto Compra de la lista
                                            for factura_guardada in inventario.lista_compras:
                                                
                                                # factura_guardada.fecha_hora es un string con formato 'dd/mm/yyyy hh:mm:ss'
                                                # ejemplo: '16/03/2026 10:35:22'
                                                # .split('/') divide ese string cada vez que encuentra un '/'
                                                # el resultado es una lista con 3 partes:
                                                # partes[0] = '16'              → el dia
                                                # partes[1] = '03'              → el mes
                                                # partes[2] = '2026 10:35:22'   → el año pegado con la hora
                                                partes = factura_guardada.fecha_hora.split('/')  # ['16', '03', '2026 10:35:22']
                                                
                                                # partes[1] es el mes como string '03'
                                                # int() lo convierte a numero entero 3
                                                # asi podemos compararlo con el mes que ingreso el usuario
                                                mes_factura = int(partes[1])       # '03' → 3
                                                
                                                # partes[2] es '2026 10:35:22' — tiene el año pegado con la hora
                                                # [:4] toma solo los primeros 4 caracteres → '2026'
                                                # int() lo convierte a numero entero 2026
                                                anio_factura = int(partes[2][:4])  # '2026 10:35:22' → '2026' → 2026
                                                
                                                
                                                
                                                # comparamos el mes y año de esta factura
                                                # con el mes y año que ingreso el usuario
                                                # si ambos coinciden, esta factura pertenece al periodo buscado
                                                if mes_factura == mes and anio_factura == anio:
                                                    # agregamos esta factura a la lista de facturas filtradas
                                                    facturas_filtradas.append(factura_guardada)


                                            # despues del for verificamos si encontramos algo
                                            # si la lista sigue vacia significa que no hay facturas en ese periodo
                                            if len(facturas_filtradas) == 0:
                                                # {mes:02d} muestra el mes con 2 digitos, ejemplo: 3 → '03'
                                                print(f'\nNo se encontraron facturas para {mes:02d}/{anio}.')
                                                continue #regresa al menu sinhacer mas



                                            # mostrar las facturas encontradas
                                            print(f'\n=== FACTURAS DE {mes:02d}/{anio} ===')
                                            print(f'Total de facturas encontradas: {len(facturas_filtradas)}')
                                            print('-' * 110)

                                            for factura_guardada in facturas_filtradas:
                                                print(f'\nFactura: {factura_guardada.id_factura} | Empleado: {usuario_autenticado.nombre} | Fecha: {factura_guardada.fecha_hora}')
                                                print(f'Proveedor: {factura_guardada.proveedor.nombre_empresa} | Tel: {factura_guardada.proveedor.telefono} | NIT/CC: {factura_guardada.proveedor.documento}')
                                                print('-' * 110)
                                                print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                print('-' * 110)
                                                for detalle in factura_guardada.lista_detalles:
                                                    tipo = 'Producto nuevo' if detalle.es_nuevo else 'Producto de Inventario'
                                                    print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                print('-' * 110)
                                                print(f'{"TOTAL COMPRA:":<95} ${factura_guardada.total_factura}')
                                                print('-' * 110)

                                        elif op_ver_facturas == 2:  # VER TODAS LAS FACTURAS

                                            # verificamos que haya facturas guardadas
                                            if len(inventario.lista_compras) == 0:
                                                print('\nNo hay facturas registradas.')

                                            #de lo contraio si hay facturas guardadas las muestra todas
                                            print(f'\n=== TODAS LAS FACTURAS DE COMPRAS ===')
                                            print(f'Total de facturas: {len(inventario.lista_compras)}')

                                            for factura_guardada in inventario.lista_compras:
                                                print('\n')
                                                print(f'FACTURA {factura_guardada.id_factura}'.center(110))
                                                print('-' * 110)
                                                print(f'Factura: {factura_guardada.id_factura} | Empleado: {usuario_autenticado.nombre} | Fecha: {factura_guardada.fecha_hora}')
                                                print(f'Proveedor: {factura_guardada.proveedor.nombre_empresa} | Tel: {factura_guardada.proveedor.telefono} | NIT/CC: {factura_guardada.proveedor.documento}')
                                                print('-' * 110)
                                                print(f'{"Codigo":<9} {"Nombre":<20} {"Tipo":<25} {"Cantidad":<12} {"P.Compra":<12} {"P.Venta":<12} {"Total"}')
                                                print('-' * 110)
                                                for detalle in factura_guardada.lista_detalles:
                                                    tipo = 'Producto nuevo' if detalle.es_nuevo else 'Producto de Inventario'
                                                    print(f'{detalle.id_detalle:<9} {detalle.producto.nombre:<20} {tipo:<25} {detalle.cantidad_compra:<12} {detalle.precio_compra:<12} {detalle.precio_venta_nuevo:<12} ${detalle.subtotal}')
                                                print('-' * 110)
                                                print(f'{"TOTAL COMPRA:":<95} ${factura_guardada.total_factura}')
                                                print('-' * 110)

                                        elif op_ver_facturas == 3:  # regresar
                                            break  # sale al menu de compras
                                                                
                                
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
            
            




            
            