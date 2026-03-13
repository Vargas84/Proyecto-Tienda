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
                                            nombre=input("Nombre del producto: ").strip()#nombre del plato a registrar
                                        
                                            if not nombre:#en caso de nombre vacio
                                                print('Este campo es obligatorio. Ingrese un nombre')
                                                continue#volvemos al inicio
                                            if not es_letras_y_espacios(nombre):#verificacion de los datos para nombre del producto
                                                print('Error: Ingrese unicamente letras')
                                                continue#volvemso al inicio
                                        
                                            #si el nombre no es vacio y contiene las letras
                                            existe=False
                                            for producto in inventario.lista_productos:#buscar  que no hayan nombre repetidos
                                                if producto.nombre.lower()==nombre.lower():
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
                                                        if producto.nombre.lower()==nuevo_nombre.lower():
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
                        print("\nError: El número de documento o la contraseña son incorrectos.")
            #Cerrar el sistrema
        elif op_inicio==3:#Si el usuario elige 3 en el menú principal, imprimimos un mensaje y salimos
            print("Gracias por usar el sistema")
            break
            
            




            
            