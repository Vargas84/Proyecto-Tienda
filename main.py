# =============================================================================
# main.py
# =============================================================================
# PUNTO DE ENTRADA ÚNICO DEL SISTEMA DE INVENTARIOS
#
# ¿QUÉ CAMBIÓ RESPECTO A LA VERSIÓN ANTERIOR?
# Solo 4 líneas en construir_sistema() — los repositories en memoria
# se reemplazan por los SQL. Todo lo demás queda exactamente igual.
# Eso es el DIP funcionando: ninguna capa superior sabe ni le importa
# qué hay debajo.
#
# También se agrega cerrar() al salir para que SQLite escriba todos
# los datos pendientes en disco antes de terminar el programa.
# =============================================================================

# --- Repositories SQL (versión con base de datos) ---
from repositories.usuario_repository_sql  import UsuarioRepositorySQL
from repositories.producto_repository_sql import ProductoRepositorySQL
from repositories.compra_repository_sql   import CompraRepositorySQL
from repositories.venta_repository_sql    import VentaRepositorySQL

# --- Conexión (para cerrar al salir) ---
from repositories.db.conexion import cerrar

# --- Services (no cambian) ---
from services.auth_service     import AuthService
from services.producto_service import ProductoService
from services.compra_service   import CompraService
from services.venta_service    import VentaService

# --- UI (no cambia) ---
from ui.auth_ui       import AuthUI
from ui.inventario_ui import InventarioUI
from ui.compra_ui     import CompraUI
from ui.venta_ui      import VentaUI


def construir_sistema():
    """
    Crea e interconecta todas las capas del sistema.

    CAMBIO RESPECTO A LA VERSIÓN ANTERIOR:
    Antes usábamos repositories en memoria (listas).
    Ahora usamos repositories SQL (SQLite).
    Los services y la UI no saben que cambió nada — DIP en acción.
    """
    # -------------------------------------------------------------------------
    # CAPA 1: REPOSITORIES SQL
    # Cada uno se conecta a la BD a través del singleton de conexion.py.
    # La BD se crea automáticamente si no existe (inventario.db).
    # -------------------------------------------------------------------------
    repo_usuarios  = UsuarioRepositorySQL()
    repo_productos = ProductoRepositorySQL()
    repo_compras   = CompraRepositorySQL()
    repo_ventas    = VentaRepositorySQL()

    # -------------------------------------------------------------------------
    # CAPA 2: SERVICES — exactamente igual que antes
    # -------------------------------------------------------------------------
    auth_svc   = AuthService(repo_usuarios)
    prod_svc   = ProductoService(repo_productos)
    compra_svc = CompraService(repo_compras, repo_productos)
    venta_svc  = VentaService(repo_ventas, repo_productos)

    # -------------------------------------------------------------------------
    # CAPA 3: UI — exactamente igual que antes
    # -------------------------------------------------------------------------
    auth_ui       = AuthUI(auth_svc)
    inventario_ui = InventarioUI(prod_svc)
    compra_ui     = CompraUI(compra_svc, auth_ui)
    venta_ui      = VentaUI(venta_svc, prod_svc, auth_ui)

    return auth_ui, inventario_ui, compra_ui, venta_ui


def menu_gestion(usuario, inventario_ui: InventarioUI,
                 compra_ui: CompraUI, venta_ui: VentaUI) -> None:
    """Menú principal después del login exitoso."""
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
    Al salir cierra la conexión a la BD para garantizar
    que todos los datos se escriben en disco.
    """
    print("=" * 50)
    print("  SISTEMA DE INVENTARIOS".center(50))
    print("=" * 50)

    auth_ui, inventario_ui, compra_ui, venta_ui = construir_sistema()

    try:
        while True:
            usuario = auth_ui.ejecutar()

            if usuario is None:
                break

            menu_gestion(usuario, inventario_ui, compra_ui, venta_ui)

    finally:
        # finally garantiza que cerrar() se ejecuta SIEMPRE,
        # incluso si ocurre un error inesperado en el sistema.
        # Así SQLite siempre hace flush de los datos pendientes.
        cerrar()
        print("\nConexión a la base de datos cerrada.")


if __name__ == "__main__":
    main()