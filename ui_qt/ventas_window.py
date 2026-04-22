# =============================================================================
# ui_qt/ventas_window.py
# =============================================================================
# Módulo de registro de ventas (salidas del inventario).
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from services.venta_service    import VentaService
from services.producto_service import ProductoService
from services.auth_service     import AuthService
from models.cliente import Cliente
from validators.campo_validator import (
    NombreValidator, CantidadValidator,
    DocumentoValidator, TelefonoValidator
)
from exceptions.app_exceptions import AppError
from ui_qt import styles


class VentasWindow(QWidget):
    """Módulo de ventas — registro de facturas de salida."""

    def __init__(self, venta_svc: VentaService,
                 prod_svc: ProductoService,
                 auth_svc: AuthService):
        super().__init__()
        self._venta_svc  = venta_svc
        self._prod_svc   = prod_svc
        self._auth_svc   = auth_svc
        self._v_nombre   = NombreValidator()
        self._v_cantidad = CantidadValidator()
        self._factura_activa = None
        self._construir_ui()

    def _construir_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        titulo = QLabel("Registro de ventas")
        titulo.setStyleSheet(styles.label_title())
        lay.addWidget(titulo)
        sub = QLabel("Registra las salidas de productos del inventario")
        sub.setStyleSheet(styles.label_subtitle())
        lay.addWidget(sub)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {styles.COLOR_BORDER};
                border-radius: 8px;
                background: {styles.COLOR_SURFACE};
            }}
            QTabBar::tab {{
                padding: 8px 20px;
                font-size: 13px;
                color: {styles.COLOR_TEXT_MUTED};
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {styles.COLOR_PRIMARY};
                border-bottom: 2px solid {styles.COLOR_PRIMARY};
                font-weight: bold;
            }}
        """)
        tabs.addTab(self._tab_nueva_venta(), "Nueva venta")
        tabs.addTab(self._tab_historial(),   "Historial de ventas")
        lay.addWidget(tabs)

    # -------------------------------------------------------------------------
    # TAB: NUEVA VENTA
    # -------------------------------------------------------------------------

    def _tab_nueva_venta(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        self._btn_iniciar = QPushButton("🛒 Iniciar nueva factura de venta")
        self._btn_iniciar.setStyleSheet(styles.btn_primary())
        self._btn_iniciar.setFixedHeight(42)
        self._btn_iniciar.clicked.connect(self._iniciar_factura)
        lay.addWidget(self._btn_iniciar)

        self._lbl_factura = QLabel("No hay una factura activa.")
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 13px;"
        )
        lay.addWidget(self._lbl_factura)

        # Tabla de productos en la factura
        self._tabla_factura = QTableWidget()
        self._tabla_factura.setStyleSheet(styles.table_style())
        self._tabla_factura.setColumnCount(5)
        self._tabla_factura.setHorizontalHeaderLabels([
            "Cód.", "Producto", "Precio unit.", "Cantidad", "Subtotal"
        ])
        self._tabla_factura.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._tabla_factura.verticalHeader().setVisible(False)
        self._tabla_factura.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        lay.addWidget(self._tabla_factura)

        self._lbl_total = QLabel("Total: $0")
        self._lbl_total.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        self._lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        lay.addWidget(self._lbl_total)

        btns = QHBoxLayout()

        self._btn_agregar = QPushButton("+ Agregar producto")
        self._btn_agregar.setStyleSheet(styles.btn_secondary())
        self._btn_agregar.setEnabled(False)
        self._btn_agregar.clicked.connect(self._dlg_agregar_producto)
        btns.addWidget(self._btn_agregar)

        btns.addStretch()

        self._btn_cancelar = QPushButton("✕ Cancelar venta")
        self._btn_cancelar.setStyleSheet(styles.btn_danger())
        self._btn_cancelar.setEnabled(False)
        self._btn_cancelar.clicked.connect(self._cancelar_factura)
        btns.addWidget(self._btn_cancelar)

        self._btn_confirmar = QPushButton("✓ Confirmar venta")
        self._btn_confirmar.setStyleSheet(styles.btn_success())
        self._btn_confirmar.setEnabled(False)
        self._btn_confirmar.clicked.connect(self._dlg_confirmar)
        btns.addWidget(self._btn_confirmar)

        lay.addLayout(btns)
        return w

    # -------------------------------------------------------------------------
    # TAB: HISTORIAL
    # -------------------------------------------------------------------------

    def _tab_historial(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(QLabel("Facturas de venta confirmadas"))
        header.addStretch()
        btn_ref = QPushButton("↻ Actualizar")
        btn_ref.setStyleSheet(styles.btn_secondary())
        btn_ref.clicked.connect(self._cargar_historial)
        header.addWidget(btn_ref)
        lay.addLayout(header)

        self._tabla_historial = QTableWidget()
        self._tabla_historial.setStyleSheet(styles.table_style())
        self._tabla_historial.setColumnCount(5)
        self._tabla_historial.setHorizontalHeaderLabels([
            "ID", "Cliente", "Empleado", "Fecha", "Total"
        ])
        self._tabla_historial.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._tabla_historial.verticalHeader().setVisible(False)
        self._tabla_historial.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        lay.addWidget(self._tabla_historial)

        self._cargar_historial()
        return w

    def _cargar_historial(self):
        ventas = self._venta_svc.obtener_todas_las_ventas()
        self._tabla_historial.setRowCount(len(ventas))
        for i, v in enumerate(ventas):
            self._tabla_historial.setItem(
                i, 0, self._celda(str(v.id_venta))
            )
            self._tabla_historial.setItem(
                i, 1, self._celda(
                    v.cliente.nombre_cliente if v.cliente else "-"
                )
            )
            self._tabla_historial.setItem(i, 2, self._celda("-"))
            self._tabla_historial.setItem(
                i, 3, self._celda(v.fecha or "-")
            )
            self._tabla_historial.setItem(
                i, 4, self._celda(f"${v.total_venta:,.0f}")
            )
            self._tabla_historial.setRowHeight(i, 44)

    # -------------------------------------------------------------------------
    # LÓGICA DE FACTURA
    # -------------------------------------------------------------------------

    def _iniciar_factura(self):
        if self._prod_svc.inventario_vacio():
            QMessageBox.warning(
                self, "Sin productos",
                "El inventario está vacío. Registra productos antes de vender."
            )
            return

        self._factura_activa = self._venta_svc.iniciar_factura()
        self._lbl_factura.setText(
            f"Factura #{self._factura_activa.id_venta} en proceso"
        )
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_PRIMARY}; font-size: 13px; font-weight: bold;"
        )
        self._btn_iniciar.setEnabled(False)
        self._btn_agregar.setEnabled(True)
        self._btn_cancelar.setEnabled(True)
        self._btn_confirmar.setEnabled(True)
        self._actualizar_tabla()

    def _cancelar_factura(self):
        resp = QMessageBox.question(
            self, "Cancelar",
            "¿Cancelar esta factura de venta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resp == QMessageBox.StandardButton.Yes:
            self._venta_svc.cancelar_factura()
            self._resetear()

    def _resetear(self):
        self._factura_activa = None
        self._lbl_factura.setText("No hay una factura activa.")
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 13px;"
        )
        self._lbl_total.setText("Total: $0")
        self._tabla_factura.setRowCount(0)
        self._btn_iniciar.setEnabled(True)
        self._btn_agregar.setEnabled(False)
        self._btn_cancelar.setEnabled(False)
        self._btn_confirmar.setEnabled(False)

    def _actualizar_tabla(self):
        if not self._factura_activa:
            return
        detalles = self._factura_activa.productos_vendidos
        self._tabla_factura.setRowCount(len(detalles))
        total = 0
        for i, d in enumerate(detalles):
            self._tabla_factura.setItem(
                i, 0, self._celda(str(d.id_detalle_ventas))
            )
            self._tabla_factura.setItem(
                i, 1, self._celda(d.objeto_producto.nombre)
            )
            self._tabla_factura.setItem(
                i, 2, self._celda(f"${d.precio_venta:,.0f}")
            )
            self._tabla_factura.setItem(
                i, 3, self._celda(str(d.cantidad_vender))
            )
            self._tabla_factura.setItem(
                i, 4, self._celda(f"${d.subtotal:,.0f}")
            )
            total += d.subtotal
            self._tabla_factura.setRowHeight(i, 44)
        self._lbl_total.setText(f"Total: ${total:,.0f}")

    # -------------------------------------------------------------------------
    # DIÁLOGOS
    # -------------------------------------------------------------------------

    def _dlg_agregar_producto(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar producto a la venta")
        dlg.setFixedSize(380, 220)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        lay.addWidget(QLabel("Producto a vender"))

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre   = self._inp("Nombre del producto")
        inp_cantidad = self._inp("Cantidad a vender")

        form.addRow("Nombre:",   inp_nombre)
        form.addRow("Cantidad:", inp_cantidad)
        lay.addLayout(form)

        lbl_info = QLabel("")
        lbl_info.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 11px;"
        )
        lay.addWidget(lbl_info)

        def buscar():
            nombre = inp_nombre.text().strip()
            if not nombre:
                return
            p = self._prod_svc.buscar_por_nombre(nombre)
            if p and p.esta_disponible():
                lbl_info.setText(
                    f"✓ Disponible. Stock: {p.stock} | Precio: ${p.precio:,.0f}"
                )
                lbl_info.setStyleSheet(
                    f"color: {styles.COLOR_SUCCESS}; font-size: 11px;"
                )
            elif p:
                lbl_info.setText("✗ Producto no disponible.")
                lbl_info.setStyleSheet(
                    f"color: {styles.COLOR_DANGER}; font-size: 11px;"
                )
            else:
                lbl_info.setText("✗ No existe en inventario.")
                lbl_info.setStyleSheet(
                    f"color: {styles.COLOR_DANGER}; font-size: 11px;"
                )

        inp_nombre.textChanged.connect(buscar)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Agregar")
        btn_ok.setStyleSheet(styles.btn_primary())
        btn_ok.clicked.connect(
            lambda: self._agregar_producto(dlg, inp_nombre, inp_cantidad)
        )

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)
        dlg.exec()

    def _agregar_producto(self, dlg, inp_nombre, inp_cantidad):
        nombre   = inp_nombre.text().strip()
        cantidad = inp_cantidad.text().strip()

        for valor, validator, campo in [
            (nombre,   self._v_nombre,   "nombre"),
            (cantidad, self._v_cantidad, "cantidad"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                QMessageBox.warning(self, "Error", f"{campo}: {e}")
                return

        try:
            self._venta_svc.agregar_producto_a_factura(nombre, int(cantidad))
            self._actualizar_tabla()
            dlg.accept()
        except AppError as e:
            QMessageBox.warning(self, "Error", str(e))

    def _dlg_confirmar(self):
        if not self._factura_activa or not self._factura_activa.productos_vendidos:
            QMessageBox.warning(self, "Error",
                                "La factura no tiene productos.")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Confirmar venta — datos del cliente")
        dlg.setFixedSize(380, 260)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        lay.addWidget(QLabel("Datos del cliente"))

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre = self._inp("Nombre completo")
        inp_doc    = self._inp("Documento (8-10 dígitos)")
        inp_tel    = self._inp("Teléfono (10 dígitos)")

        form.addRow("Nombre:",    inp_nombre)
        form.addRow("Documento:", inp_doc)
        form.addRow("Teléfono:",  inp_tel)
        lay.addLayout(form)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Confirmar venta")
        btn_ok.setStyleSheet(styles.btn_success())
        btn_ok.clicked.connect(
            lambda: self._confirmar_venta(dlg, inp_nombre, inp_doc, inp_tel)
        )

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)
        dlg.exec()

    def _confirmar_venta(self, dlg, inp_nombre, inp_doc, inp_tel):
        nombre = inp_nombre.text().strip()
        doc    = inp_doc.text().strip()
        tel    = inp_tel.text().strip()

        v_nom = NombreValidator()
        v_doc = DocumentoValidator()
        v_tel = TelefonoValidator()

        for valor, validator, campo in [
            (nombre, v_nom, "nombre"),
            (doc,    v_doc, "documento"),
            (tel,    v_tel, "teléfono"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                QMessageBox.warning(self, "Error", f"{campo}: {e}")
                return

        cliente = Cliente(nombre, int(doc), int(tel))
        try:
            confirmada = self._venta_svc.confirmar_factura(cliente)
            QMessageBox.information(
                self, "Venta confirmada",
                f"Factura #{confirmada.id_venta} confirmada.\n"
                f"Total: ${confirmada.total_venta:,.0f}"
            )
            dlg.accept()
            self._resetear()
            self._cargar_historial()
        except AppError as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------------------------------------------------------------------------
    # UTILIDADES
    # -------------------------------------------------------------------------

    def _celda(self, texto: str) -> QTableWidgetItem:
        item = QTableWidgetItem(texto)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def _inp(self, placeholder: str) -> QLineEdit:
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setStyleSheet(styles.input_field())
        inp.setFixedHeight(36)
        return inp