# =============================================================================
# ui/inventario_ui.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Maneja la interacción del usuario para gestionar el inventario:
#   - Ver inventario
#   - Agregar productos
#   - Cambiar disponibilidad
#   - Editar atributos de un producto
#
# ANTES: todo esto estaba en el bloque if opcion_gestion == 1 →
# while True → if opcion_inventario == 1,2,3,4,5
# con 12+ niveles de indentación.
#
# AHORA: un método por opción de menú. Máximo 2-3 niveles de indentación.
# =============================================================================

from services.producto_service import ProductoService
from validators.campo_validator import (
    NombreValidator,
    PrecioValidator,
    StockValidator,
    CategoriaValidator,
)
from exceptions.app_exceptions import (
    AppError,
    ProductoYaExisteError,
    ProductoNoEncontradoError,
)
from ui.ui_utils import pedir_dato, pedir_opcion, separador, titulo

# Clave de acceso al menú de edición.
# ANTES: estaba hardcodeada inline como clave_editar = "jabon"
# AHORA: constante con nombre descriptivo al tope del archivo.
CLAVE_EDICION = "jabon"


class InventarioUI:
    """Interfaz de usuario para la gestión del inventario."""

    def __init__(self, producto_service: ProductoService):
        self._prod_svc    = producto_service
        self._v_nombre    = NombreValidator()
        self._v_precio    = PrecioValidator()
        self._v_stock     = StockValidator()
        self._v_categoria = CategoriaValidator()

    # -------------------------------------------------------------------------
    # MENÚ PRINCIPAL DE INVENTARIO
    # -------------------------------------------------------------------------

    def ejecutar(self) -> None:
        """
        Muestra el menú de inventario en bucle.
        ANTES: while True con if opcion_inventario == 1..5 anidado
        dentro de if opcion_gestion == 1.
        """
        while True:
            print("\n--- MENÚ DE INVENTARIO ---")
            print("1. Agregar producto")
            print("2. Disponibilidad de un producto")
            print("3. Modificar producto")
            print("4. Ver inventario")
            print("5. Volver al menú anterior")

            opcion = pedir_opcion("Seleccione una opción: ", 1, 5)

            if opcion == 1:
                self._agregar_producto()
            elif opcion == 2:
                self._cambiar_disponibilidad()
            elif opcion == 3:
                self._editar_producto()
            elif opcion == 4:
                self._ver_inventario()
            elif opcion == 5:
                print("Regresando al menú anterior...")
                break

    # -------------------------------------------------------------------------
    # AGREGAR PRODUCTO
    # -------------------------------------------------------------------------

    def _agregar_producto(self) -> None:
        """
        Recopila datos del nuevo producto y lo registra.
        ANTES: if opcion_inventario == 1 con cuatro while True anidados.
        """
        print("\n--- AGREGAR PRODUCTO ---")

        # Nombre — validamos formato y que no esté duplicado
        while True:
            nombre = pedir_dato("Nombre del producto: ",
                                self._v_nombre)
            nombre = nombre.strip()
            if not self._prod_svc.nombre_disponible(nombre):
                print(f"  Error: '{nombre}' ya está en uso. "
                      "Ingrese un nombre diferente.")
            else:
                break

        precio    = float(pedir_dato("Precio de venta: ", self._v_precio))
        categoria = pedir_dato("Categoría: ", self._v_categoria)
        stock     = int(pedir_dato("Stock inicial: ", self._v_stock))

        try:
            producto = self._prod_svc.agregar_producto(
                nombre, precio, categoria, stock
            )
            print(f"\nProducto '{producto.nombre}' agregado con "
                  f"ID automático {producto.codigo}.")
        except ProductoYaExisteError as e:
            print(f"\nError: {e}")

    # -------------------------------------------------------------------------
    # CAMBIAR DISPONIBILIDAD
    # -------------------------------------------------------------------------

    def _cambiar_disponibilidad(self) -> None:
        """
        Muestra el inventario, pide el código y cambia la disponibilidad.
        ANTES: elif opcion_inventario == 2
        """
        print("\n--- DISPONIBILIDAD DE PRODUCTOS ---")

        if self._prod_svc.inventario_vacio():
            print("No hay productos registrados en el inventario.")
            return

        print(self._prod_svc.formatear_inventario())

        try:
            codigo = int(input("\nCódigo del producto: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return

        try:
            producto = self._prod_svc.cambiar_disponibilidad(codigo)
            print(f"Disponibilidad de '{producto.nombre}' "
                  f"cambiada a: {producto.disponibilidad}")
        except ProductoNoEncontradoError as e:
            print(f"\nError: {e}")

    # -------------------------------------------------------------------------
    # EDITAR PRODUCTO
    # -------------------------------------------------------------------------

    def _editar_producto(self) -> None:
        """
        Solicita la clave de acceso y luego permite editar atributos.
        ANTES: elif opcion_inventario == 3, con verificación de clave
        inline y el menú de edición anidado dentro.
        """
        clave = input("Contraseña para acceder al menú de edición: ")
        if clave != CLAVE_EDICION:
            print("\n¡Clave incorrecta! Acceso denegado.")
            return

        if self._prod_svc.inventario_vacio():
            print("\nEl inventario está vacío. Agregue productos antes.")
            return

        print(self._prod_svc.formatear_inventario())

        try:
            codigo = int(input("\nCódigo del producto a editar: "))
        except ValueError:
            print("  Error: Ingrese un número válido.")
            return

        try:
            producto = self._prod_svc.buscar_por_id(codigo)
        except ProductoNoEncontradoError as e:
            print(f"\nError: {e}")
            return

        # Submenú de edición
        while True:
            print(f"\n--- Editando: {producto.nombre} ---")
            print(producto.mostrar_informacion())
            print("\n1. Nombre\n2. Precio\n3. Stock"
                  "\n4. Categoría\n5. Volver")

            op = pedir_opcion("¿Qué desea editar?: ", 1, 5)

            if op == 1:
                self._editar_nombre(codigo, producto)
            elif op == 2:
                self._editar_precio(codigo, producto)
            elif op == 3:
                self._editar_stock(codigo, producto)
            elif op == 4:
                self._editar_categoria(codigo, producto)
            elif op == 5:
                break

    def _editar_nombre(self, codigo: int, producto) -> None:
        nuevo = input(f"Nuevo nombre [{producto.nombre}]: ").strip()
        if not nuevo:
            print(f"El nombre quedó igual: {producto.nombre}")
            return
        try:
            self._v_nombre.validar(nuevo)
            self._prod_svc.editar_nombre(codigo, nuevo)
            print(f"Nombre actualizado a '{nuevo}'.")
        except (AppError, ProductoYaExisteError) as e:
            print(f"  Error: {e}")

    def _editar_precio(self, codigo: int, producto) -> None:
        nuevo = input(f"Nuevo precio [{producto.precio}]: ").strip()
        if not nuevo:
            print(f"El precio quedó igual: {producto.precio}")
            return
        try:
            self._v_precio.validar(nuevo)
            self._prod_svc.editar_precio(codigo, float(nuevo))
            print(f"Precio actualizado a ${nuevo}.")
        except AppError as e:
            print(f"  Error: {e}")

    def _editar_stock(self, codigo: int, producto) -> None:
        nuevo = input(f"Nuevo stock [{producto.stock}]: ").strip()
        if not nuevo:
            print(f"El stock quedó igual: {producto.stock}")
            return
        try:
            self._v_stock.validar(nuevo)
            self._prod_svc.editar_stock(codigo, int(nuevo))
            print(f"Stock actualizado a {nuevo}.")
        except AppError as e:
            print(f"  Error: {e}")

    def _editar_categoria(self, codigo: int, producto) -> None:
        nueva = input(f"Nueva categoría [{producto.categoria}]: ").strip()
        if not nueva:
            print(f"La categoría quedó igual: {producto.categoria}")
            return
        try:
            self._v_categoria.validar(nueva)
            self._prod_svc.editar_categoria(codigo, nueva)
            print(f"Categoría actualizada a '{nueva}'.")
        except AppError as e:
            print(f"  Error: {e}")

    # -------------------------------------------------------------------------
    # VER INVENTARIO
    # -------------------------------------------------------------------------

    def _ver_inventario(self) -> None:
        """Muestra el inventario completo formateado."""
        print(self._prod_svc.formatear_inventario())