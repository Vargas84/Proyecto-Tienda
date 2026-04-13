# =============================================================================
# ui/venta_ui.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Maneja la interacción del usuario para registrar ventas:
#   - Menú principal de ventas
#   - Crear y gestionar una factura de venta
#   - Confirmar o cancelar la venta
#   - Ver facturas de ventas guardadas
#
# ANTES: bloque elif opcion_gestion == 3 con ~300 líneas anidadas.
# AHORA: métodos separados, máximo 2-3 niveles de indentación.
# =============================================================================

from services.venta_service import VentaService
from services.producto_service import ProductoService
from models.cliente import Cliente
from validators.campo_validator import (
    NombreValidator,
    CantidadValidator,
)
from exceptions.app_exceptions import (
    AppError,
    ProductoNoEncontradoError,
    ProductoDuplicadoEnFacturaError,
    ProductoNoDisponibleError,
    StockInsuficienteError,
    FacturaVaciaError,
)
from ui.ui_utils import pedir_dato, pedir_opcion, separador, titulo

ANCHO = 110


class VentaUI:
    """Interfaz de usuario para la gestión de facturas de venta."""

    def __init__(self, venta_service: VentaService,
                 producto_service: ProductoService,
                 auth_ui):
        self._venta_svc  = venta_service
        self._prod_svc   = producto_service
        self._auth_ui    = auth_ui
        self._v_nombre   = NombreValidator()
        self._v_cantidad = CantidadValidator()

    # -------------------------------------------------------------------------
    # MENÚ PRINCIPAL DE VENTAS
    # -------------------------------------------------------------------------

    def ejecutar(self, nombre_usuario: str) -> None:
        """
        Menú principal de ventas.
        ANTES: while True dentro de elif opcion_gestion == 3.
        """
        if self._prod_svc.inventario_vacio():
            print("\nEl inventario está vacío. Agregue productos antes.")
            return

        while True:
            print(f"\n=== MENÚ DE VENTAS === (Usuario: {nombre_usuario})")
            print("1. Registrar venta")
            print("2. Ver facturas de ventas")
            print("3. Volver al menú anterior")

            opcion = pedir_opcion("Ingrese una opción: ", 1, 3)

            if opcion == 1:
                self._gestionar_factura(nombre_usuario)
            elif opcion == 2:
                self._ver_facturas(nombre_usuario)
            elif opcion == 3:
                break

    # -------------------------------------------------------------------------
    # GESTIONAR FACTURA DE VENTA
    # -------------------------------------------------------------------------

    def _gestionar_factura(self, nombre_usuario: str) -> None:
        """
        Ciclo completo de una factura de venta.
        ANTES: while True con banderas venta_confirmada y venta_cancelada.
        """
        factura = self._venta_svc.iniciar_factura()
        print(f"\n=== FACTURA DE VENTA {factura.id_venta} ===")

        while True:
            print(f"\n--- Factura de venta {factura.id_venta} ---")
            print("1. Agregar productos a la venta")
            print("2. Ver productos de la venta")
            print("3. Eliminar producto de la venta")
            print("4. Editar cantidad de un producto")
            print("5. Cancelar venta")
            print("6. Confirmar venta")

            opcion = pedir_opcion("Ingrese una opción: ", 1, 6)

            if opcion == 1:
                self._agregar_producto(factura)
            elif opcion == 2:
                self._mostrar_factura(factura, nombre_usuario)
            elif opcion == 3:
                cancelada = self._eliminar_producto(factura)
                if cancelada:
                    break
            elif opcion == 4:
                self._editar_cantidad(factura)
            elif opcion == 5:
                self._venta_svc.cancelar_factura()
                print("\nVenta cancelada.")
                break
            elif opcion == 6:
                confirmada = self._confirmar_venta(
                    factura, nombre_usuario
                )
                if confirmada:
                    break

    # -------------------------------------------------------------------------
    # AGREGAR PRODUCTO A LA FACTURA
    # -------------------------------------------------------------------------

    def _agregar_producto(self, factura) -> None:
        """
        Muestra el inventario, pide el producto y la cantidad.
        Verifica existencia, disponibilidad y duplicados ANTES
        de pedir la cantidad — así no se pide información innecesaria.
        """
        print(self._prod_svc.formatear_inventario())
        print("Solo se pueden agregar productos con disponibilidad.")

        nombre = pedir_dato(
            "\nNombre del producto: ", self._v_nombre
        ).strip()

        # ── Verificaciones en la UI antes de pedir cantidad ──────────────
        # 1. Existe en inventario
        producto = self._prod_svc.buscar_por_nombre(nombre)
        if producto is None:
            print(f"\n  Error: '{nombre}' no existe en el inventario. "
                  "Solo se pueden vender productos registrados.")
            return

        # 2. Está disponible
        if not producto.esta_disponible():
            print(f"\n  Error: '{producto.nombre}' no está disponible "
                  "para la venta.")
            return

        # 3. No está ya en esta factura
        nombre_norm = nombre.lower().replace(" ", "")
        ya_en_factura = any(
            d.objeto_producto.nombre.lower().replace(" ", "") == nombre_norm
            for d in factura.productos_vendidos
        )
        if ya_en_factura:
            print(f"\n  Error: '{nombre}' ya fue agregado a esta factura. "
                  "No pueden existir productos duplicados.")
            return

        # ── Solo si pasó todas las verificaciones pedimos la cantidad ─────
        # Mostramos el stock disponible para que el usuario sepa el límite.
        print(f"  Stock disponible: {producto.stock} unidades.")
        cantidad = int(pedir_dato(
            f"Cantidad a vender de '{producto.nombre}': ",
            self._v_cantidad
        ))

        # Verificamos stock suficiente antes de llamar al service
        if cantidad > producto.stock:
            print(f"\n  Error: Stock insuficiente. "
                  f"Solo hay {producto.stock} unidades de '{producto.nombre}'.")
            return

        try:
            detalle = self._venta_svc.agregar_producto_a_factura(
                nombre, cantidad
            )
            print(f"\n'{detalle.objeto_producto.nombre}' agregado "
                  f"a la factura {factura.id_venta}.")
        except (
            ProductoNoEncontradoError,
            ProductoDuplicadoEnFacturaError,
            ProductoNoDisponibleError,
            StockInsuficienteError,
        ) as e:
            print(f"\nError: {e}")

    # -------------------------------------------------------------------------
    # MOSTRAR FACTURA
    # -------------------------------------------------------------------------

    def _mostrar_factura(self, factura, nombre_usuario: str,
                         fecha: str = "") -> None:
        if not factura.productos_vendidos:
            print("\nNo hay productos registrados en esta venta.")
            return
        self._imprimir_tabla(factura, nombre_usuario, fecha)

    def _imprimir_tabla(self, factura, nombre_usuario: str,
                        fecha: str = "") -> None:
        separador(ANCHO)
        if fecha:
            print(f"Factura: {factura.id_venta} | "
                  f"Empleado: {nombre_usuario} | Fecha: {fecha}")
            separador(ANCHO)

        # Mostramos los datos del cliente si ya fueron registrados
        if factura.cliente is not None:
            cl = factura.cliente
            print(f"Cliente: {cl.nombre_cliente} | "
                  f"NIT/CC: {cl.documento} | "
                  f"Tel: {cl.telefono}")
            separador(ANCHO)

        print(
            f"{'Codigo':<9} {'Nombre':<20} {'Precio unit.':<20} "
            f"{'Cantidad':<20} {'Total'}"
        )
        separador(ANCHO)

        total = 0
        for d in factura.productos_vendidos:
            total += d.subtotal
            print(
                f"{d.id_detalle_ventas:<9} "
                f"{d.objeto_producto.nombre:<20} "
                f"{d.precio_venta:<20} "
                f"{d.cantidad_vender:<20} "
                f"${d.subtotal}"
            )

        separador(ANCHO)
        print(f"{'TOTAL VENTA:':<75} ${total}")
        separador(ANCHO)

    # -------------------------------------------------------------------------
    # ELIMINAR PRODUCTO DE LA FACTURA
    # -------------------------------------------------------------------------

    def _eliminar_producto(self, factura) -> bool:
        """
        Elimina un producto de la factura.
        Retorna True si la factura quedó vacía y fue cancelada.
        ANTES: op_factura_venta == 3, con advertencia especial
        cuando solo quedaba un producto.
        """
        if not factura.productos_vendidos:
            print("\nNo hay productos en esta venta.")
            return False

        if len(factura.productos_vendidos) == 1:
            print("\n¡ADVERTENCIA: La factura solo tiene un producto!")
            print("Si lo eliminas, la factura será cancelada.")

        self._imprimir_tabla(factura, "")

        try:
            codigo = int(input("Código del producto a eliminar: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return False

        # Verificamos PRIMERO que el código existe en la factura.
        # Si no existe mostramos el error sin pedir confirmación.
        if not any(d.id_detalle_ventas == codigo
                   for d in factura.productos_vendidos):
            print(f"\n  Error: No existe un producto con el código "
                  f"{codigo} en la factura.")
            return False

        confirmacion = input(
            "¿Confirma la eliminación? (si/no): "
        ).strip().lower()
        if confirmacion != "si":
            print("  Eliminación cancelada.")
            return False

        try:
            _, cancelada = self._venta_svc.eliminar_detalle(codigo)
            if cancelada:
                print(f"\nLa factura {factura.id_venta} fue cancelada "
                      "automáticamente por quedar sin productos.")
                return True
            print("  Producto eliminado de la factura.")
            return False
        except ProductoNoEncontradoError as e:
            print(f"  Error: {e}")
            return False

    # -------------------------------------------------------------------------
    # EDITAR CANTIDAD
    # -------------------------------------------------------------------------

    def _editar_cantidad(self, factura) -> None:
        """
        Actualiza la cantidad de un producto en la factura.
        ANTES: op_factura_venta == 4.
        """
        if not factura.productos_vendidos:
            print("\nNo hay productos en esta venta.")
            return

        self._imprimir_tabla(factura, "")

        try:
            codigo = int(input("Código del producto a editar: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return

        # Verificamos PRIMERO que el código existe en la factura.
        # Si no existe mostramos el error de inmediato sin pedir cantidad.
        detalle = next(
            (d for d in factura.productos_vendidos
             if d.id_detalle_ventas == codigo), None
        )
        if detalle is None:
            print(f"\n  Error: No existe un producto con el código "
                  f"{codigo} en la factura.")
            return

        # Solo si existe mostramos el stock disponible y pedimos la cantidad
        print(f"  Stock disponible: {detalle.objeto_producto.stock} unidades.")
        nueva = input(
            f"Nueva cantidad [{detalle.cantidad_vender}] "
            f"(Enter para mantener): "
        ).strip()
        if not nueva:
            print(f"  Cantidad sin cambios: {detalle.cantidad_vender}.")
            return

        try:
            self._v_cantidad.validar(nueva)
            detalle_actualizado = self._venta_svc.editar_cantidad_detalle(
                codigo, int(nueva)
            )
            print(f"  Cantidad de '{detalle_actualizado.objeto_producto.nombre}' "
                  f"actualizada a {detalle_actualizado.cantidad_vender}.")
        except (AppError, StockInsuficienteError,
                ProductoNoEncontradoError) as e:
            print(f"  Error: {e}")

    # -------------------------------------------------------------------------
    # CONFIRMAR VENTA
    # -------------------------------------------------------------------------

    def _confirmar_venta(self, factura, nombre_usuario: str) -> bool:
        """
        Muestra el resumen, recoge datos del cliente y confirma la venta.
        Retorna True si se confirmó, False si se canceló.
        ANTES: op_factura_venta == 6 → op_confir_venta == 1,2,3
        todo anidado con banderas.
        """
        if not factura.productos_vendidos:
            print("\nNo puedes confirmar una venta sin productos.")
            return False

        from datetime import datetime
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self._imprimir_tabla(factura, nombre_usuario, fecha)

        # Recoger datos del cliente por primera vez
        datos = self._auth_ui.recoger_datos_persona("cliente")
        cliente = Cliente(
            datos["nombre"], datos["documento"], datos["telefono"]
        )

        # Menú de confirmación final
        while True:
            print(f"\n=== CONFIRMAR FACTURA DE VENTA "
                  f"{factura.id_venta} ===")
            print("1. Editar datos del cliente")
            print("2. Confirmar venta")
            print("3. Regresar al menú anterior")

            op = pedir_opcion("Ingrese una opción: ", 1, 3)

            if op == 1:
                # Editamos campo por campo — Enter vacío conserva el valor actual
                cliente = self._editar_cliente(cliente)

            elif op == 2:
                try:
                    confirmada = self._venta_svc.confirmar_factura(cliente)
                    titulo(
                        f"FACTURA {confirmada.id_venta} CONFIRMADA",
                        ANCHO
                    )
                    print(f"\n¡Venta guardada correctamente!")
                    return True
                except FacturaVaciaError as e:
                    print(f"\nError: {e}")

            elif op == 3:
                return False

    # -------------------------------------------------------------------------
    # VER FACTURAS DE VENTAS
    # -------------------------------------------------------------------------

    def _editar_cliente(self, cliente: Cliente) -> Cliente:
        """
        Edita los datos del cliente campo por campo.
        Enter vacío en cualquier campo conserva el valor actual.
        Retorna el objeto Cliente actualizado.
        """
        print(f"\n--- Editar datos del cliente ---")
        print(f"  Nombre actual:    {cliente.nombre_cliente}")
        print(f"  Documento actual: {cliente.documento}")
        print(f"  Teléfono actual:  {cliente.telefono}")
        print("  (Enter para conservar cada valor)")

        # --- Nombre ---
        nuevo_nombre = input(
            f"\nNuevo nombre [{cliente.nombre_cliente}]: "
        ).strip()
        if nuevo_nombre:
            try:
                self._auth_ui._v_nombre.validar(nuevo_nombre)
                cliente.nombre_cliente = nuevo_nombre
                print(f"  Nombre actualizado a '{nuevo_nombre}'.")
            except Exception as e:
                print(f"  Error: {e}. Nombre quedó igual.")
        else:
            print(f"  Nombre quedó igual: {cliente.nombre_cliente}")

        # --- Documento ---
        nuevo_doc = input(
            f"Nuevo documento [{cliente.documento}]: "
        ).strip()
        if nuevo_doc:
            try:
                self._auth_ui._v_documento.validar(nuevo_doc)
                doc_int = int(nuevo_doc)
                if self._auth_ui._auth_svc.documento_de_empleado_existe(doc_int):
                    print("  Error: ese documento pertenece a un empleado. "
                          "Documento quedó igual.")
                else:
                    cliente.documento = doc_int
                    print(f"  Documento actualizado a {doc_int}.")
            except Exception as e:
                print(f"  Error: {e}. Documento quedó igual.")
        else:
            print(f"  Documento quedó igual: {cliente.documento}")

        # --- Teléfono ---
        nuevo_tel = input(
            f"Nuevo teléfono [{cliente.telefono}]: "
        ).strip()
        if nuevo_tel:
            try:
                self._auth_ui._v_telefono.validar(nuevo_tel)
                tel_int = int(nuevo_tel)
                if self._auth_ui._auth_svc.telefono_de_empleado_existe(tel_int):
                    print("  Error: ese teléfono pertenece a un empleado. "
                          "Teléfono quedó igual.")
                else:
                    cliente.telefono = tel_int
                    print(f"  Teléfono actualizado a {tel_int}.")
            except Exception as e:
                print(f"  Error: {e}. Teléfono quedó igual.")
        else:
            print(f"  Teléfono quedó igual: {cliente.telefono}")

        return cliente

    def _ver_facturas(self, nombre_usuario: str) -> None:
        if not self._venta_svc.hay_ventas():
            print("\nNo hay facturas de ventas registradas.")
            return

        while True:
            print("\n=== VER FACTURAS DE VENTAS ===")
            print("1. Buscar por mes y año")
            print("2. Ver todas las facturas")
            print("3. Regresar")

            op = pedir_opcion("Ingrese una opción: ", 1, 3)

            if op == 1:
                self._ver_por_mes(nombre_usuario)
            elif op == 2:
                self._ver_todas(nombre_usuario)
            elif op == 3:
                break

    def _ver_por_mes(self, nombre_usuario: str) -> None:
        try:
            mes  = int(input("Mes (1-12): "))
            anio = int(input("Año (ej: 2026): "))
        except ValueError:
            print("  Error: Ingrese números válidos.")
            return

        ventas = self._venta_svc.buscar_ventas_por_mes(mes, anio)
        if not ventas:
            print(f"\nNo hay ventas para {mes:02d}/{anio}.")
            return

        print(f"\n=== VENTAS DE {mes:02d}/{anio} "
              f"({len(ventas)} encontradas) ===")
        for v in ventas:
            self._imprimir_tabla(v, nombre_usuario, v.fecha)

    def _ver_todas(self, nombre_usuario: str) -> None:
        ventas = self._venta_svc.obtener_todas_las_ventas()
        print(f"\n=== TODAS LAS VENTAS ({len(ventas)}) ===")
        for v in ventas:
            self._imprimir_tabla(v, nombre_usuario, v.fecha)