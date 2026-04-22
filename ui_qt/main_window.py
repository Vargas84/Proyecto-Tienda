# =============================================================================
# ui_qt/main_window.py
# =============================================================================
# Ventana principal del sistema después del login.
# Tiene un menú lateral con los módulos y un área de contenido
# que muestra la ventana correspondiente a cada módulo.
# =============================================================================

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.auth_service     import AuthService
from services.producto_service import ProductoService
from services.compra_service   import CompraService
from services.venta_service    import VentaService
from ui_qt import styles


class MainWindow(QMainWindow):
    """
    Ventana principal después del login.
    Contiene el menú lateral y el área de contenido con los módulos.
    Emite cerrar_sesion cuando el usuario cierra sesión.
    """

    cerrar_sesion = pyqtSignal()

    def __init__(self, usuario, auth_svc: AuthService,
                 prod_svc: ProductoService,
                 compra_svc: CompraService,
                 venta_svc: VentaService):
        super().__init__()
        self._usuario   = usuario
        self._auth_svc  = auth_svc
        self._prod_svc  = prod_svc
        self._compra_svc = compra_svc
        self._venta_svc = venta_svc

        self._construir_ui()

    def _construir_ui(self):
        self.setWindowTitle(f"Sistema de Inventarios — {self._usuario.nombre}")
        self.setMinimumSize(1100, 680)
        self.setStyleSheet(f"background-color: {styles.COLOR_BG};")

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Menú lateral ────────────────────────────────────────────
        sidebar = self._construir_sidebar()
        root.addWidget(sidebar)

        # ── Área de contenido ────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setStyleSheet(f"background-color: {styles.COLOR_BG};")
        root.addWidget(self._stack, stretch=1)

        # Importamos aquí para evitar importaciones circulares
        from ui_qt.inventario_window import InventarioWindow
        from ui_qt.compras_window    import ComprasWindow
        from ui_qt.ventas_window     import VentasWindow

        self._inventario_win = InventarioWindow(self._prod_svc)
        self._compras_win    = ComprasWindow(
            self._compra_svc, self._prod_svc, self._auth_svc
        )
        self._ventas_win     = VentasWindow(
            self._venta_svc, self._prod_svc, self._auth_svc
        )

        self._stack.addWidget(self._inventario_win)  # índice 0
        self._stack.addWidget(self._compras_win)     # índice 1
        self._stack.addWidget(self._ventas_win)      # índice 2

        # Mostramos inventario por defecto
        self._cambiar_modulo(0)

    def _construir_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            f"background-color: {styles.COLOR_SIDEBAR}; border: none;"
        )

        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Encabezado con nombre de usuario
        header = QFrame()
        header.setStyleSheet(
            f"background-color: {styles.COLOR_SIDEBAR}; "
            f"border-bottom: 1px solid #334155;"
        )
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(20, 20, 20, 16)

        ico = QLabel("📦")
        ico.setStyleSheet("font-size: 28px; border: none;")
        h_lay.addWidget(ico)

        nombre_lbl = QLabel(self._usuario.nombre)
        nombre_lbl.setStyleSheet(
            "color: white; font-size: 14px; font-weight: bold; border: none;"
        )
        nombre_lbl.setWordWrap(True)
        h_lay.addWidget(nombre_lbl)

        rol_lbl = QLabel("Empleado")
        rol_lbl.setStyleSheet(
            "color: #94A3B8; font-size: 11px; border: none;"
        )
        h_lay.addWidget(rol_lbl)

        lay.addWidget(header)
        lay.addSpacing(8)

        # Botones de módulos
        modulos = [
            ("📋  Inventario",    0),
            ("📦  Compras",       1),
            ("🛒  Ventas",        2),
        ]

        self._btns_modulo = []
        for texto, idx in modulos:
            btn = self._sidebar_btn(texto, idx)
            self._btns_modulo.append(btn)
            lay.addWidget(btn)

        lay.addStretch()

        # Botón cerrar sesión
        btn_salir = QPushButton("↩  Cerrar sesión")
        btn_salir.setStyleSheet(f"""
            QPushButton {{
                color: #94A3B8;
                background: transparent;
                border: none;
                text-align: left;
                padding: 14px 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                color: white;
                background-color: {styles.COLOR_SIDEBAR_HOVER};
            }}
        """)
        btn_salir.clicked.connect(self._hacer_logout)
        lay.addWidget(btn_salir)
        lay.addSpacing(8)

        return sidebar

    def _sidebar_btn(self, texto: str, idx: int) -> QPushButton:
        btn = QPushButton(texto)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: #CBD5E1;
                background: transparent;
                border: none;
                text-align: left;
                padding: 14px 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                color: white;
                background-color: {styles.COLOR_SIDEBAR_HOVER};
            }}
        """)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda _, i=idx: self._cambiar_modulo(i))
        return btn

    def _cambiar_modulo(self, idx: int):
        self._stack.setCurrentIndex(idx)
        # Resaltar el botón activo
        for i, btn in enumerate(self._btns_modulo):
            if i == idx:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        color: white;
                        background-color: {styles.COLOR_SIDEBAR_ACTIVE};
                        border: none;
                        border-left: 3px solid white;
                        text-align: left;
                        padding: 14px 20px;
                        font-size: 13px;
                        font-weight: bold;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        color: #CBD5E1;
                        background: transparent;
                        border: none;
                        text-align: left;
                        padding: 14px 20px;
                        font-size: 13px;
                    }}
                    QPushButton:hover {{
                        color: white;
                        background-color: {styles.COLOR_SIDEBAR_HOVER};
                    }}
                """)

    def _hacer_logout(self):
        self.cerrar_sesion.emit()
        self.close()