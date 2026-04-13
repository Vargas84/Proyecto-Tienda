# =============================================================================
# main.py
# =============================================================================
# PUNTO DE ENTRADA ÚNICO DEL SISTEMA DE INVENTARIOS
#
# ¿QUÉ HACE ESTE ARCHIVO?
# Es el "ensamblador" del sistema. Su único trabajo es:
#   1. Crear los repositories (almacenamiento)
#   2. Crear los services (lógica de negocio), inyectándoles los repos
#   3. Crear las UIs, inyectándoles los services
#   4. Arrancar el bucle principal
#
# PRINCIPIO APLICADO — DIP (Dependency Inversion):
# Ningún service crea su propio repository.
# Ninguna UI crea su propio service.
# Todo se construye aquí y se pasa hacia abajo.
# Eso significa que si mañana quieres cambiar el almacenamiento a
# una base de datos, solo cambias los repositories en este archivo.
# El resto del sistema no sabe ni le importa.
#
# ANTES: todo el sistema vivía en inventarioSistema(), una función
# de 700+ líneas que mezclaba UI, lógica de negocio y datos.
# AHORA: cada capa tiene su lugar. main.py solo conecta las piezas.
# =============================================================================

# --- Repositories ---
from repositories.usuario_repository import UsuarioRepository
from repositories.producto_repository import ProductoRepository
from repositories.compra_repository import CompraRepository
from repositories.venta_repository import VentaRepository

# --- Services ---
from services.auth_service import AuthService
from services.producto_service import ProductoService
from services.compra_service import CompraService
from services.venta_service import VentaService

# --- UI ---
from ui.auth_ui import AuthUI
from ui.inventario_ui import InventarioUI
from ui.compra_ui import CompraUI
from ui.venta_ui import VentaUI


def construir_sistema():
    """
    Crea e interconecta todas las capas del sistema.

    El orden importa:
      1. Primero los repositories (no dependen de nadie)
      2. Luego los services (dependen de repositories)
      3. Finalmente las UIs (dependen de services)

    Retorna una tupla con las UIs listas para usar.
    """
    # -------------------------------------------------------------------------
    # CAPA 1: REPOSITORIES
    # Cada uno gestiona su propia lista en memoria.
    # En el futuro, reemplazar estas líneas por versiones con BD.
    # -------------------------------------------------------------------------
    repo_usuarios  = UsuarioRepository()
    repo_productos = ProductoRepository()
    repo_compras   = CompraRepository()
    repo_ventas    = VentaRepository()

    # -------------------------------------------------------------------------
    # CAPA 2: SERVICES
    # Reciben los repositories que necesitan — no los crean ellos mismos.
    # -------------------------------------------------------------------------
    auth_svc    = AuthService(repo_usuarios)
    prod_svc    = ProductoService(repo_productos)

    # CompraService y VentaService necesitan DOS repositories cada uno:
    # el suyo propio y el de productos (para actualizar el inventario
    # al confirmar facturas).
    compra_svc  = CompraService(repo_compras, repo_productos)
    venta_svc   = VentaService(repo_ventas, repo_productos)

    # -------------------------------------------------------------------------
    # CAPA 3: UI
    # Cada UI recibe el service que necesita.
    # AuthUI también se pasa a CompraUI y VentaUI para reutilizar
    # recoger_datos_persona() sin duplicar código.
    # -------------------------------------------------------------------------
    auth_ui      = AuthUI(auth_svc)
    inventario_ui = InventarioUI(prod_svc)
    compra_ui    = CompraUI(compra_svc, auth_ui)
    venta_ui     = VentaUI(venta_svc, prod_svc, auth_ui)

    return auth_ui, inventario_ui, compra_ui, venta_ui


def menu_gestion(usuario, inventario_ui: InventarioUI,
                 compra_ui: CompraUI, venta_ui: VentaUI) -> None:
    """
    Menú principal después del login exitoso.

    ANTES: este era el while True interno con opcion_gestion == 1,2,3,4
    dentro del bloque de login exitoso en inventarioSistema().
    AHORA: función limpia que delega a cada UI.
    """
    while True:
        print(f"\n======== MENÚ DE GESTIÓN "
              f"(Usuario: {usuario.nombre}) ========")
        print("1. Inventario")
        print("2. Registrar entrada (Compra)")
        print("3. Registrar salida (Venta)")
        print("4. Cerrar sesión")

        from ui.ui_utils import pedir_opcion
        opcion = pedir_opcion("Seleccione una opción: ", 1, 4)

        if opcion == 1:
            inventario_ui.ejecutar()
        elif opcion == 2:
            compra_ui.ejecutar(usuario.nombre)
        elif opcion == 3:
            venta_ui.ejecutar(usuario.nombre)
        elif opcion == 4:
            print(f"\n¡Hasta luego, {usuario.nombre}!")
            break


def main() -> None:
    """
    Función principal. Arranca el sistema.

    Flujo:
      1. Construye el sistema (repositories → services → UIs)
      2. Muestra el menú de autenticación en bucle
      3. Cuando el login es exitoso, muestra el menú de gestión
      4. Al cerrar sesión, vuelve al menú de autenticación
      5. Al elegir 'Salir', termina el programa
    """
    print("=" * 50)
    print("  SISTEMA DE INVENTARIOS".center(50))
    print("=" * 50)

    # Construimos el sistema una sola vez al arrancar
    auth_ui, inventario_ui, compra_ui, venta_ui = construir_sistema()

    # Bucle principal: login → gestión → logout → login → ...
    while True:
        # auth_ui.ejecutar() retorna el Usuario si el login fue exitoso,
        # o None si el usuario eligió "Salir del sistema"
        usuario = auth_ui.ejecutar()

        if usuario is None:
            # El usuario eligió salir — terminamos el programa
            break

        # Login exitoso — mostramos el menú de gestión
        menu_gestion(usuario, inventario_ui, compra_ui, venta_ui)
        # Al volver de menu_gestion, el usuario cerró sesión
        # y el while True vuelve a mostrar el menú de login


if __name__ == "__main__":
    # Este bloque garantiza que main() solo se ejecuta cuando
    # corres el archivo directamente (python main.py), no cuando
    # lo importas desde otro módulo.
    main()