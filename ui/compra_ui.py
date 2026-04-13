# =============================================================================
# ui/compra_ui.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Maneja toda la interacción del usuario para registrar compras:
#   - Menú principal de compras
#   - Crear y gestionar una factura en proceso
#   - Confirmar o cancelar la factura
#   - Ver facturas guardadas
#
# ANTES: bloque elif opcion_gestion == 2 con ~300 líneas anidadas.
# AHORA: métodos separados, máximo 2-3 niveles de indentación.
# =============================================================================

from datetime import datetime
from services.compra_service import CompraService
from models.proveedor import Proveedor
from validators.campo_validator import (
    NombreValidator,
    PrecioValidator,
    CantidadValidator,
    CategoriaValidator,
)
from exceptions.app_exceptions import (
    AppError,
    FacturaVaciaError,
    ProductoDuplicadoEnFacturaError,
    ProductoNoEncontradoError,
)
from ui.ui_utils import pedir_dato, pedir_opcion, separador, titulo

ANCHO = 110  # ancho de las tablas en consola


class CompraUI:
    """Interfaz de usuario para la gestión de facturas de compra."""

    def __init__(self, compra_service: CompraService, auth_ui):
        self._compra_svc = compra_service
        # Recibimos auth_ui para reutilizar recoger_datos_persona()
        # y no duplicar la lógica de recoger datos de proveedor.
        self._auth_ui    = auth_ui
        self._v_nombre   = NombreValidator()
        self._v_precio   = PrecioValidator()
        self._v_cantidad = CantidadValidator()
        self._v_categoria = CategoriaValidator()

    # -------------------------------------------------------------------------
    # MENÚ PRINCIPAL DE COMPRAS
    # -------------------------------------------------------------------------

    def ejecutar(self, nombre_usuario: str) -> None:
        """
        Menú principal de compras.
        ANTES: while True dentro de elif opcion_gestion == 2.
        """
        while True:
            print(f"\n=== REGISTRAR COMPRAS === "
                  f"(Usuario: {nombre_usuario})")
            print("1. Registrar compra")
            print("2. Ver facturas de compras")
            print("3. Volver al menú anterior")

            opcion = pedir_opcion("Ingrese una opción: ", 1, 3)

            if opcion == 1:
                self._gestionar_factura(nombre_usuario)
            elif opcion == 2:
                self._ver_facturas(nombre_usuario)
            elif opcion == 3:
                break

    # -------------------------------------------------------------------------
    # GESTIONAR FACTURA (crear, agregar productos, confirmar/cancelar)
    # -------------------------------------------------------------------------

    def _gestionar_factura(self, nombre_usuario: str) -> None:
        """
        Ciclo completo de una factura: crear → agregar productos
        → confirmar o cancelar.
        ANTES: while True anidado con banderas factura_confirmada
        y factura_cancelada controlando el flujo.
        AHORA: el service maneja el estado; la UI solo llama métodos.
        """
        factura = self._compra_svc.iniciar_factura()
        print(f"\n=== FACTURA DE COMPRA {factura.id_factura} ===")

        while True:
            print(f"\n--- Factura {factura.id_factura} ---")
            print("1. Agregar productos a la compra")
            print("2. Ver productos de la compra")
            print("3. Confirmar compra")
            print("4. Cancelar compra")

            opcion = pedir_opcion("Ingrese una opción: ", 1, 4)

            if opcion == 1:
                self._agregar_producto_a_factura(factura)

            elif opcion == 2:
                self._mostrar_factura(factura, nombre_usuario)

            elif opcion == 3:
                # _confirmar_factura retorna:
                #   True  → compra confirmada exitosamente
                #   False → cancelada (manual, por vacía, o error)
                # En ambos casos distintos a "seguir editando", salimos.
                resultado = self._confirmar_factura(factura, nombre_usuario)
                if resultado is not None:
                    break

            elif opcion == 4:
                self._compra_svc.cancelar_factura()
                print("\nCompra cancelada.")
                break

    # -------------------------------------------------------------------------
    # AGREGAR PRODUCTO A LA FACTURA
    # -------------------------------------------------------------------------

    def _agregar_producto_a_factura(self, factura) -> None:
        """
        Pide el nombre del producto, detecta si es nuevo o existente,
        pide los datos necesarios y lo agrega a la factura.
        ANTES: opcion_factura == 1, ~80 líneas con dos ramas if/else.
        """
        nombre = pedir_dato(
            "\nNombre del producto: ", self._v_nombre
        ).strip()

        cantidad    = int(pedir_dato(
            f"Cantidad a comprar de '{nombre}': ",
            self._v_cantidad
        ))
        precio_c    = float(pedir_dato(
            f"Precio de compra de '{nombre}': ",
            self._v_precio
        ))
        precio_v    = float(pedir_dato(
            "Precio de venta al público: ",
            self._v_precio
        ))

        # Categoría solo si es producto nuevo — el service determina
        # si existe o no, así que siempre la pedimos por si acaso.
        # Si el producto ya existe en inventario, el service ignora
        # la categoría (usa la que ya tiene).
        categoria = pedir_dato(
            f"Categoría de '{nombre}' (solo si es nuevo): ",
            self._v_categoria
        )

        try:
            detalle = self._compra_svc.agregar_producto_a_factura(
                nombre, cantidad, precio_c, precio_v, categoria
            )
            tipo = "nuevo" if detalle.es_nuevo else "del inventario"
            print(f"\n'{detalle.producto.nombre}' ({tipo}) "
                  f"agregado a la factura {factura.id_factura}.")
        except (ProductoDuplicadoEnFacturaError, AppError) as e:
            print(f"\nError: {e}")

    # -------------------------------------------------------------------------
    # MOSTRAR FACTURA
    # -------------------------------------------------------------------------

    def _mostrar_factura(self, factura, nombre_usuario: str,
                         fecha: str = "") -> None:
        """
        Imprime la tabla de productos de la factura activa.
        ANTES: opcion_factura == 2, código de tabla inline.
        """
        if not factura.lista_detalles:
            print("\nNo hay productos registrados en esta compra.")
            return

        print(f"\n=== PRODUCTOS EN LA FACTURA {factura.id_factura} ===")
        self._imprimir_tabla(factura, nombre_usuario, fecha)

    def _imprimir_tabla(self, factura, nombre_usuario: str,
                        fecha: str = "") -> None:
        """Imprime la tabla completa de una factura."""
        separador(ANCHO)
        if fecha:
            print(f"Factura: {factura.id_factura} | "
                  f"Empleado: {nombre_usuario} | Fecha: {fecha}")
            separador(ANCHO)

        # Mostramos los datos del proveedor si ya fueron registrados
        if factura.proveedor is not None:
            p = factura.proveedor
            print(f"Proveedor: {p.nombre_empresa} | "
                  f"NIT/CC: {p.documento} | "
                  f"Tel: {p.telefono}")
            separador(ANCHO)

        encabezado = (
            f"{'Codigo':<9} {'Nombre':<20} {'Tipo':<25} "
            f"{'Cantidad':<12} {'P.Compra':<12} {'P.Venta':<12} {'Total'}"
        )
        print(encabezado)
        separador(ANCHO)

        total = 0
        for d in factura.lista_detalles:
            total += d.subtotal
            tipo = "Producto nuevo" if d.es_nuevo else "Producto inventario"
            print(
                f"{d.id_detalle:<9} {d.producto.nombre:<20} {tipo:<25} "
                f"{d.cantidad_compra:<12} {d.precio_compra:<12} "
                f"{d.precio_venta_nuevo:<12} ${d.subtotal}"
            )

        separador(ANCHO)
        print(f"{'TOTAL COMPRA:':<95} ${total}")
        separador(ANCHO)

    # -------------------------------------------------------------------------
    # CONFIRMAR FACTURA
    # -------------------------------------------------------------------------

    def _confirmar_factura(self, factura, nombre_usuario: str) -> bool:
        """
        Muestra el resumen, recopila datos del proveedor y confirma.
        Retorna True si se confirmó, False si se canceló en el proceso.

        ANTES: opcion_factura == 3 → menú de confirmación con submenús
        de editar productos, editar proveedor, confirmar y cancelar.
        Todo anidado en ~150 líneas.
        """
        if not factura.lista_detalles:
            print("\nNo puedes confirmar una compra sin productos.")
            return False

        fecha = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self._imprimir_tabla(factura, nombre_usuario, fecha)

        # Recoger datos del proveedor reutilizando auth_ui
        datos = self._auth_ui.recoger_datos_persona("proveedor")
        proveedor = Proveedor(
            datos["nombre"], datos["documento"], datos["telefono"]
        )

        # Menú de confirmación final
        while True:
            print(f"\n=== CONFIRMAR FACTURA {factura.id_factura} ===")
            print("1. Editar productos de la factura")
            print("2. Editar datos del proveedor")
            print("3. Confirmar compra")
            print("4. Cancelar compra")

            op = pedir_opcion("Ingrese una opción: ", 1, 4)

            if op == 1:
                cancelada = self._editar_productos_factura(
                    factura, nombre_usuario, fecha
                )
                # Si _editar_productos_factura retorna True, la factura
                # quedó vacía y fue cancelada — salimos de _confirmar_factura
                # también, así el flujo regresa directamente al menú de compras.
                if cancelada:
                    return False

            elif op == 2:
                # Editamos el proveedor campo por campo mostrando el
                # valor actual — Enter vacío conserva el valor original.
                proveedor = self._editar_proveedor(proveedor)

            elif op == 3:
                try:
                    confirmada = self._compra_svc.confirmar_factura(
                        proveedor, nombre_usuario
                    )
                    titulo(
                        f"FACTURA {confirmada.id_factura} CONFIRMADA",
                        ANCHO
                    )
                    print(f"\n¡Factura guardada correctamente!")
                    return True
                except FacturaVaciaError as e:
                    print(f"\nError: {e}")

            elif op == 4:
                self._compra_svc.cancelar_factura()
                print("\nCompra cancelada.")
                return False

    def _editar_proveedor(self, proveedor: Proveedor) -> Proveedor:
        """
        Edita los datos del proveedor campo por campo.
        Enter vacío en cualquier campo conserva el valor actual.
        Retorna el objeto Proveedor actualizado.
        """
        print(f"\n--- Editar datos del proveedor ---")
        print(f"  Nombre actual:    {proveedor.nombre_empresa}")
        print(f"  Documento actual: {proveedor.documento}")
        print(f"  Teléfono actual:  {proveedor.telefono}")
        print("  (Enter para conservar cada valor)")

        # --- Nombre ---
        nuevo_nombre = input(
            f"\nNuevo nombre [{proveedor.nombre_empresa}]: "
        ).strip()
        if nuevo_nombre:
            try:
                self._auth_ui._v_nombre.validar(nuevo_nombre)
                proveedor.nombre_empresa = nuevo_nombre
                print(f"  Nombre actualizado a '{nuevo_nombre}'.")
            except Exception as e:
                print(f"  Error: {e}. Nombre quedó igual.")
        else:
            print(f"  Nombre quedó igual: {proveedor.nombre_empresa}")

        # --- Documento ---
        nuevo_doc = input(
            f"Nuevo documento [{proveedor.documento}]: "
        ).strip()
        if nuevo_doc:
            try:
                self._auth_ui._v_documento.validar(nuevo_doc)
                doc_int = int(nuevo_doc)
                # Verificar que no sea documento de un empleado
                if self._auth_ui._auth_svc.documento_de_empleado_existe(doc_int):
                    print("  Error: ese documento pertenece a un empleado. "
                          "Documento quedó igual.")
                else:
                    proveedor.documento = doc_int
                    print(f"  Documento actualizado a {doc_int}.")
            except Exception as e:
                print(f"  Error: {e}. Documento quedó igual.")
        else:
            print(f"  Documento quedó igual: {proveedor.documento}")

        # --- Teléfono ---
        nuevo_tel = input(
            f"Nuevo teléfono [{proveedor.telefono}]: "
        ).strip()
        if nuevo_tel:
            try:
                self._auth_ui._v_telefono.validar(nuevo_tel)
                tel_int = int(nuevo_tel)
                if self._auth_ui._auth_svc.telefono_de_empleado_existe(tel_int):
                    print("  Error: ese teléfono pertenece a un empleado. "
                          "Teléfono quedó igual.")
                else:
                    proveedor.telefono = tel_int
                    print(f"  Teléfono actualizado a {tel_int}.")
            except Exception as e:
                print(f"  Error: {e}. Teléfono quedó igual.")
        else:
            print(f"  Teléfono quedó igual: {proveedor.telefono}")

        return proveedor

    def _editar_productos_factura(self, factura, nombre_usuario: str,
                                  fecha: str) -> bool:
        """
        Submenú para editar o eliminar productos de la factura.
        Retorna True si la factura fue cancelada al quedar vacía,
        False si se salió normalmente.
        """
        while True:
            self._imprimir_tabla(factura, nombre_usuario, fecha)
            print("\n1. Editar un producto")
            print("2. Eliminar un producto")
            print("3. Regresar")

            op = pedir_opcion("Ingrese una opción: ", 1, 3)

            if op == 1:
                self._editar_detalle(factura)
            elif op == 2:
                cancelada = self._eliminar_detalle(factura)
                if cancelada:
                    # La factura quedó vacía y fue cancelada automáticamente.
                    # Retornamos True para que _confirmar_factura y
                    # _gestionar_factura sepan que deben salir también.
                    print("\nLa factura fue cancelada por quedar sin productos.")
                    return True
            elif op == 3:
                break
        return False

    def _editar_detalle(self, factura) -> None:
        """Edita los atributos de un detalle dentro de la factura."""
        try:
            codigo = int(input("Código del producto a editar: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return

        # Verificamos PRIMERO que el código existe en la factura.
        # Si no existe mostramos el error de inmediato y regresamos
        # sin mostrar el submenú — ese era el bug reportado.
        if not any(d.id_detalle == codigo for d in factura.lista_detalles):
            print(f"\n  Error: No existe un producto con el código "
                  f"{codigo} en la factura.")
            return

        # Solo si el código existe mostramos el submenú de edición
        print("\n1. Editar nombre (solo productos nuevos)")
        print("2. Editar cantidad")
        print("3. Editar precio de compra")
        print("4. Editar precio de venta")
        print("5. Cancelar")

        # Obtenemos el detalle para mostrar el valor actual al editar.
        # Así el usuario sabe qué tiene y puede decidir si cambiarlo.
        detalle = next(
            d for d in factura.lista_detalles if d.id_detalle == codigo
        )

        op = pedir_opcion("¿Qué desea editar?: ", 1, 5)

        try:
            if op == 1:
                # Enter vacío = dejar el nombre como estaba
                nuevo = input(
                    f"Nuevo nombre [{detalle.producto.nombre}] "
                    f"(Enter para no cambiar): "
                ).strip()
                if not nuevo:
                    print(f"  Nombre quedó igual: {detalle.producto.nombre}")
                    return
                self._compra_svc.editar_nombre_detalle(codigo, nuevo)

            elif op == 2:
                # Enter vacío = dejar la cantidad como estaba
                nueva_str = input(
                    f"Nueva cantidad [{detalle.cantidad_compra}] "
                    f"(Enter para no cambiar): "
                ).strip()
                if not nueva_str:
                    print(f"  Cantidad quedó igual: {detalle.cantidad_compra}")
                    return
                try:
                    self._v_cantidad.validar(nueva_str)
                except AppError as e:
                    print(f"  Error: {e}")
                    return
                self._compra_svc.editar_cantidad_detalle(
                    codigo, int(nueva_str)
                )

            elif op == 3:
                # Enter vacío = dejar el precio de compra como estaba
                nuevo_p_str = input(
                    f"Nuevo precio de compra [{detalle.precio_compra}] "
                    f"(Enter para no cambiar): "
                ).strip()
                if not nuevo_p_str:
                    print(f"  Precio de compra quedó igual: {detalle.precio_compra}")
                    return
                try:
                    self._v_precio.validar(nuevo_p_str)
                except AppError as e:
                    print(f"  Error: {e}")
                    return
                self._compra_svc.editar_precio_compra_detalle(
                    codigo, float(nuevo_p_str)
                )

            elif op == 4:
                # Enter vacío = dejar el precio de venta como estaba
                nuevo_pv_str = input(
                    f"Nuevo precio de venta [{detalle.precio_venta_nuevo}] "
                    f"(Enter para no cambiar): "
                ).strip()
                if not nuevo_pv_str:
                    print(f"  Precio de venta quedó igual: {detalle.precio_venta_nuevo}")
                    return
                try:
                    self._v_precio.validar(nuevo_pv_str)
                except AppError as e:
                    print(f"  Error: {e}")
                    return
                self._compra_svc.editar_precio_venta_detalle(
                    codigo, float(nuevo_pv_str)
                )

            elif op == 5:
                return
            print("  Actualizado correctamente.")
        except (AppError, PermissionError, ProductoNoEncontradoError) as e:
            print(f"  Error: {e}")

    def _eliminar_detalle(self, factura) -> bool:
        """
        Elimina un producto de la factura.
        Retorna True si la factura fue cancelada (quedó vacía).
        """
        try:
            codigo = int(input("Código del producto a eliminar: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return False

        # Verificamos PRIMERO que el código existe en la factura.
        # Si no existe mostramos el error de inmediato y regresamos
        # sin pedir confirmación — ese era el bug reportado.
        if not any(d.id_detalle == codigo for d in factura.lista_detalles):
            print(f"\n  Error: No existe un producto con el código "
                  f"{codigo} en la factura.")
            return False

        confirmacion = input(
            f"¿Confirma la eliminación? (si/no): "
        ).strip().lower()

        if confirmacion != "si":
            print("  Eliminación cancelada.")
            return False

        try:
            _, cancelada = self._compra_svc.eliminar_detalle(codigo)
            if cancelada:
                return True
            print("  Producto eliminado de la factura.")
            return False
        except ProductoNoEncontradoError as e:
            print(f"  Error: {e}")
            return False

    # -------------------------------------------------------------------------
    # VER FACTURAS GUARDADAS
    # -------------------------------------------------------------------------

    def _ver_facturas(self, nombre_usuario: str) -> None:
        """
        Submenú para ver facturas guardadas (todas o por mes/año).
        ANTES: op_compras == 2 con el while True de búsqueda anidado.
        """
        if not self._compra_svc.hay_compras():
            print("\nNo hay facturas registradas.")
            return

        while True:
            print("\n=== VER FACTURAS DE COMPRAS ===")
            print("1. Buscar por mes y año")
            print("2. Ver todas las facturas")
            print("3. Regresar")

            op = pedir_opcion("Ingrese una opción: ", 1, 3)

            if op == 1:
                self._ver_facturas_por_mes(nombre_usuario)
            elif op == 2:
                self._ver_todas_las_facturas(nombre_usuario)
            elif op == 3:
                break

    def _ver_facturas_por_mes(self, nombre_usuario: str) -> None:
        try:
            mes  = int(input("Mes (1-12): "))
            anio = int(input("Año (ej: 2026): "))
        except ValueError:
            print("  Error: Ingrese números válidos.")
            return

        facturas = self._compra_svc.buscar_compras_por_mes(mes, anio)
        if not facturas:
            print(f"\nNo hay facturas para {mes:02d}/{anio}.")
            return

        print(f"\n=== FACTURAS DE {mes:02d}/{anio} "
              f"({len(facturas)} encontradas) ===")
        for f in facturas:
            self._imprimir_tabla(f, nombre_usuario, f.fecha_hora)

    def _ver_todas_las_facturas(self, nombre_usuario: str) -> None:
        facturas = self._compra_svc.obtener_todas_las_compras()
        print(f"\n=== TODAS LAS FACTURAS ({len(facturas)}) ===")
        for f in facturas:
            self._imprimir_tabla(f, nombre_usuario, f.fecha_hora)