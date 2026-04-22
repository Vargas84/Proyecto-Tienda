# =============================================================================
# main.py — Punto de entrada con interfaz gráfica PyQt6
# =============================================================================
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from repositories.usuario_repository_sql  import UsuarioRepositorySQL
from repositories.producto_repository_sql import ProductoRepositorySQL
from repositories.compra_repository_sql   import CompraRepositorySQL
from repositories.venta_repository_sql    import VentaRepositorySQL
from repositories.db.conexion import cerrar

from services.auth_service     import AuthService
from services.producto_service import ProductoService
from services.compra_service   import CompraService
from services.venta_service    import VentaService

from ui_qt.login_window import LoginWindow
from ui_qt.main_window  import MainWindow


def main():
    app = QApplication(sys.argv)

    # Fuente global del sistema
    fuente = QFont("Segoe UI", 10)
    app.setFont(fuente)

    # Construir services
    repo_u = UsuarioRepositorySQL()
    repo_p = ProductoRepositorySQL()
    repo_c = CompraRepositorySQL()
    repo_v = VentaRepositorySQL()

    auth_svc   = AuthService(repo_u)
    prod_svc   = ProductoService(repo_p)
    compra_svc = CompraService(repo_c, repo_p)
    venta_svc  = VentaService(repo_v, repo_p)

    # Ventana de login
    login_win = LoginWindow(auth_svc)

    # Referencia a ventana principal (para mantenerla viva)
    main_win_ref = [None]

    def abrir_main(usuario):
        """Se ejecuta cuando el login es exitoso."""
        login_win.hide()
        main_win = MainWindow(
            usuario, auth_svc, prod_svc, compra_svc, venta_svc
        )
        main_win_ref[0] = main_win

        def volver_a_login():
            main_win_ref[0] = None
            login_win.show()

        main_win.cerrar_sesion.connect(volver_a_login)
        main_win.show()

    login_win.login_exitoso.connect(abrir_main)
    login_win.show()

    try:
        sys.exit(app.exec())
    finally:
        cerrar()


if __name__ == "__main__":
    main()