# =============================================================================
# ui_qt/compras_window.py
# =============================================================================
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QDialog, QFormLayout, QLineEdit, QMessageBox, QTabWidget,
    QSplitter, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from services.compra_service   import CompraService
from services.producto_service import ProductoService
from services.auth_service     import AuthService
from models.proveedor import Proveedor
from validators.campo_validator import (
    NombreValidator, PrecioValidator, CantidadValidator, CategoriaValidator,
    DocumentoValidator, TelefonoValidator
)
from exceptions.app_exceptions import AppError
from ui_qt import styles


class ComprasWindow(QWidget):
    """Módulo de compras — registro de facturas de entrada."""

    def __init__(self, compra_svc: CompraService,
             prod_svc: ProductoService,
             auth_svc: AuthService,
             usuario):
        super().__init__()
        self._compra_svc  = compra_svc
        self._prod_svc    = prod_svc
        self._auth_svc    = auth_svc
        self._usuario     = usuario
        self._v_nombre    = NombreValidator()
        self._v_precio    = PrecioValidator()
        self._v_cantidad  = CantidadValidator()
        self._v_categoria = CategoriaValidator()
        self._factura_activa = None
        self._construir_ui()

    def _construir_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        titulo = QLabel("Registro de compras")
        titulo.setStyleSheet(styles.label_title())
        lay.addWidget(titulo)
        sub = QLabel("Registra las entradas de mercancía al inventario")
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
        tabs.addTab(self._tab_nueva_compra(), "Nueva compra")
        tabs.addTab(self._tab_historial(),    "Historial de compras")
        lay.addWidget(tabs)

    # -------------------------------------------------------------------------
    # TAB: NUEVA COMPRA
    # -------------------------------------------------------------------------

    def _tab_nueva_compra(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        self._btn_iniciar = QPushButton("📄 Iniciar nueva factura de compra")
        self._btn_iniciar.setStyleSheet(styles.btn_primary())
        self._btn_iniciar.setFixedHeight(42)
        self._btn_iniciar.clicked.connect(self._iniciar_factura)
        lay.addWidget(self._btn_iniciar)

        self._lbl_factura = QLabel("No hay una factura activa.")
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 13px;"
        )
        lay.addWidget(self._lbl_factura)

        self._tabla_factura = QTableWidget()
        self._tabla_factura.setStyleSheet(styles.table_style())
        self._tabla_factura.setColumnCount(6)
        self._tabla_factura.setHorizontalHeaderLabels([
            "Cód.", "Producto", "Cantidad",
            "P. Compra", "P. Venta", "Subtotal"
        ])
        # assert garantiza a Pylance que horizontalHeader() no es None
        _hf = self._tabla_factura.horizontalHeader()
        assert _hf is not None
        _hf.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        _vf = self._tabla_factura.verticalHeader()
        assert _vf is not None
        _vf.setVisible(False)

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

        self._btn_agregar_prod = QPushButton("+ Agregar producto")
        self._btn_agregar_prod.setStyleSheet(styles.btn_secondary())
        self._btn_agregar_prod.setEnabled(False)
        self._btn_agregar_prod.clicked.connect(self._dlg_agregar_producto)
        btns.addWidget(self._btn_agregar_prod)

        btns.addStretch()

        self._btn_cancelar = QPushButton("✕ Cancelar factura")
        self._btn_cancelar.setStyleSheet(styles.btn_danger())
        self._btn_cancelar.setEnabled(False)
        self._btn_cancelar.clicked.connect(self._cancelar_factura)
        btns.addWidget(self._btn_cancelar)

        self._btn_confirmar = QPushButton("✓ Confirmar compra")
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

        hdr = QHBoxLayout()
        hdr.addWidget(QLabel("Facturas de compra confirmadas"))
        hdr.addStretch()
        btn_ref = QPushButton("↻ Actualizar")
        btn_ref.setStyleSheet(styles.btn_secondary())
        btn_ref.clicked.connect(self._cargar_historial)
        hdr.addWidget(btn_ref)
        lay.addLayout(hdr)

        self._tabla_historial = QTableWidget()
        self._tabla_historial.setStyleSheet(styles.table_style())
        self._tabla_historial.setColumnCount(5)
        self._tabla_historial.setHorizontalHeaderLabels([
            "ID", "Proveedor", "Empleado", "Fecha", "Total"
        ])

        _hh = self._tabla_historial.horizontalHeader()
        assert _hh is not None
        _hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        _vh = self._tabla_historial.verticalHeader()
        assert _vh is not None
        _vh.setVisible(False)

        self._tabla_historial.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        lay.addWidget(self._tabla_historial)
        # Doble clic en una fila abre el detalle de esa factura
        self._tabla_historial.doubleClicked.connect(self._ver_detalle_factura)

        self._cargar_historial()
        return w

    def _cargar_historial(self):
        compras = self._compra_svc.obtener_todas_las_compras()
        self._tabla_historial.setRowCount(len(compras))
        for i, c in enumerate(compras):
            self._tabla_historial.setItem(i, 0, self._celda(str(c.id_factura)))
            self._tabla_historial.setItem(
                i, 1, self._celda(
                    c.proveedor.nombre_empresa if c.proveedor else "-"
                )
            )
            self._tabla_historial.setItem(
                i, 2, self._celda(c.empleado_nombre or "-")
)
            self._tabla_historial.setItem(
                i, 3, self._celda(c.fecha_hora or "-")
            )
            self._tabla_historial.setItem(
                i, 4, self._celda(f"${c.total_factura:,.0f}")
            )
            self._tabla_historial.setRowHeight(i, 44)

    # -------------------------------------------------------------------------
    # LÓGICA DE FACTURA
    # -------------------------------------------------------------------------

    def _iniciar_factura(self):
        self._factura_activa = self._compra_svc.iniciar_factura()
        self._lbl_factura.setText(
            f"Factura #{self._factura_activa.id_factura} en proceso"
        )
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_PRIMARY}; font-size: 13px; font-weight: bold;"
        )
        self._btn_iniciar.setEnabled(False)
        self._btn_agregar_prod.setEnabled(True)
        self._btn_cancelar.setEnabled(True)
        self._btn_confirmar.setEnabled(True)
        self._actualizar_tabla_factura()

    def _cancelar_factura(self):
        confirmado = styles.mostrar_mensaje(
            self, "Cancelar",
            "¿Seguro que quieres cancelar esta factura?", "question"
)
        if confirmado:
            self._compra_svc.cancelar_factura()
            self._resetear_factura()

    def _resetear_factura(self):
        self._factura_activa = None
        self._lbl_factura.setText("No hay una factura activa.")
        self._lbl_factura.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 13px;"
        )
        self._lbl_total.setText("Total: $0")
        self._tabla_factura.setRowCount(0)
        self._btn_iniciar.setEnabled(True)
        self._btn_agregar_prod.setEnabled(False)
        self._btn_cancelar.setEnabled(False)
        self._btn_confirmar.setEnabled(False)

    def _actualizar_tabla_factura(self):
        if not self._factura_activa:
            return
        detalles = self._factura_activa.lista_detalles
        self._tabla_factura.setRowCount(len(detalles))
        total = 0
        for i, d in enumerate(detalles):
            tipo = "Nuevo" if d.es_nuevo else "Inventario"
            self._tabla_factura.setItem(i, 0, self._celda(str(d.id_detalle)))
            self._tabla_factura.setItem(
                i, 1, self._celda(f"{d.producto.nombre} ({tipo})")
            )
            self._tabla_factura.setItem(i, 2, self._celda(str(d.cantidad_compra)))
            self._tabla_factura.setItem(i, 3, self._celda(f"${d.precio_compra:,.0f}"))
            self._tabla_factura.setItem(i, 4, self._celda(f"${d.precio_venta_nuevo:,.0f}"))
            self._tabla_factura.setItem(i, 5, self._celda(f"${d.subtotal:,.0f}"))
            total += d.subtotal
            self._tabla_factura.setRowHeight(i, 44)
        self._lbl_total.setText(f"Total: ${total:,.0f}")

    # -------------------------------------------------------------------------
    # DIÁLOGOS
    # -------------------------------------------------------------------------

    def _dlg_agregar_producto(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar producto a la compra")
        dlg.setFixedSize(400, 360)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        lay.addWidget(QLabel("Agregar producto a la factura"))

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre    = self._inp("Nombre del producto")
        inp_cantidad  = self._inp("Unidades a comprar")
        inp_p_compra  = self._inp("Precio de compra unitario")
        inp_p_venta   = self._inp("Precio de venta al público")
        inp_categoria = self._inp("Categoría (solo si es nuevo)")

        form.addRow("Nombre:",    inp_nombre)
        form.addRow("Cantidad:",  inp_cantidad)
        form.addRow("P. Compra:", inp_p_compra)
        form.addRow("P. Venta:",  inp_p_venta)
        form.addRow("Categoría:", inp_categoria)
        lay.addLayout(form)

        lbl_info = QLabel("")
        lbl_info.setStyleSheet(
            f"color: {styles.COLOR_TEXT_MUTED}; font-size: 11px;"
        )
        lay.addWidget(lbl_info)

        def buscar_producto():
            nombre = inp_nombre.text().strip()
            if not nombre:
                return
            p = self._prod_svc.buscar_por_nombre(nombre)
            if p:
                lbl_info.setText(
                    f"✓ Encontrado en inventario. Stock actual: {p.stock}"
                )
                lbl_info.setStyleSheet(
                    f"color: {styles.COLOR_SUCCESS}; font-size: 11px;"
                )
            else:
                lbl_info.setText("Producto nuevo — se agregará al inventario.")
                lbl_info.setStyleSheet(
                    f"color: {styles.COLOR_TEXT_MUTED}; font-size: 11px;"
                )

        inp_nombre.textChanged.connect(buscar_producto)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Agregar")
        btn_ok.setStyleSheet(styles.btn_primary())
        btn_ok.clicked.connect(lambda: self._agregar_producto_a_factura(
            dlg, inp_nombre, inp_cantidad, inp_p_compra,
            inp_p_venta, inp_categoria
        ))

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)
        dlg.exec()

    def _agregar_producto_a_factura(self, dlg, inp_nombre, inp_cantidad,
                                     inp_p_compra, inp_p_venta, inp_categoria):
        nombre    = inp_nombre.text().strip()
        cantidad  = inp_cantidad.text().strip()
        p_compra  = inp_p_compra.text().strip()
        p_venta   = inp_p_venta.text().strip()
        categoria = inp_categoria.text().strip()

        for valor, validator, campo in [
            (nombre,   self._v_nombre,   "nombre"),
            (cantidad, self._v_cantidad, "cantidad"),
            (p_compra, self._v_precio,   "precio de compra"),
            (p_venta,  self._v_precio,   "precio de venta"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                styles.mostrar_mensaje(self, "Error", f"{campo}: {e}", "warning")
                return

        try:
            self._compra_svc.agregar_producto_a_factura(
                nombre, int(cantidad), float(p_compra),
                float(p_venta), categoria
            )
            self._actualizar_tabla_factura()
            dlg.accept()
        except AppError as e:
            styles.mostrar_mensaje(self, "Error", str(e), "warning")

    def _dlg_confirmar(self):
        if not self._factura_activa or not self._factura_activa.lista_detalles:
            styles.mostrar_mensaje(self, "Error", "La factura no tiene productos.", "warning")
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Confirmar compra — datos del proveedor")
        dlg.setFixedSize(380, 260)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        lay.addWidget(QLabel("Datos del proveedor"))

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre = self._inp("Nombre o empresa")
        inp_doc    = self._inp("NIT o cédula (8-10 dígitos)")
        inp_tel    = self._inp("Teléfono (10 dígitos)")

        form.addRow("Nombre:",    inp_nombre)
        form.addRow("Documento:", inp_doc)
        form.addRow("Teléfono:",  inp_tel)
        lay.addLayout(form)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Confirmar compra")
        btn_ok.setStyleSheet(styles.btn_success())
        btn_ok.clicked.connect(lambda: self._confirmar_compra(
            dlg, inp_nombre, inp_doc, inp_tel
        ))

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)
        dlg.exec()

    def _confirmar_compra(self, dlg, inp_nombre, inp_doc, inp_tel):
        nombre = inp_nombre.text().strip()
        doc    = inp_doc.text().strip()
        tel    = inp_tel.text().strip()

        v_doc = DocumentoValidator()
        v_tel = TelefonoValidator()

        for valor, validator, campo in [
            (nombre, NombreValidator(), "nombre"),
            (doc,    v_doc,            "documento"),
            (tel,    v_tel,            "teléfono"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                styles.mostrar_mensaje(self, "Error", f"{campo}: {e}", "warning")
                return

        proveedor = Proveedor(nombre, int(doc), int(tel))
        try:
            confirmada = self._compra_svc.confirmar_factura(proveedor, self._usuario.nombre)
            styles.mostrar_mensaje(
                self, "Compra confirmada",
                f"Factura #{confirmada.id_factura} confirmada.\n"
                f"Total: ${confirmada.total_factura:,.0f}", "info"
            )
            dlg.accept()
            self._resetear_factura()
            self._cargar_historial()
        except AppError as e:
            styles.mostrar_mensaje(self, "Error", str(e), "warning")
            
            
            
            
            
    def _ver_detalle_factura(self, index):
        """Abre ventana de detalle al hacer doble clic en una factura."""
        fila = index.row()
        id_item = self._tabla_historial.item(fila, 0)
        if id_item is None:
            return

        id_factura = int(id_item.text())
        compras = self._compra_svc.obtener_todas_las_compras()
        factura = next((c for c in compras if c.id_factura == id_factura), None)
        if factura is None:
            return

        self._mostrar_ventana_detalle(factura)
        
        
        
    def _mostrar_ventana_detalle(self, factura):
        """Muestra una ventana con el detalle completo de una factura."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Detalle — Factura #{factura.id_factura}")
        dlg.setMinimumSize(700, 450)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        # Encabezado de la factura
        lay.addWidget(self._lbl_detalle(
            f"Factura #{factura.id_factura}", grande=True
        ))

        info = QHBoxLayout()
        info.addWidget(self._lbl_detalle(
            f"Proveedor: {factura.proveedor.nombre_empresa if factura.proveedor else '-'}"
        ))
        info.addStretch()
        info.addWidget(self._lbl_detalle(
            f"Empleado: {factura.empleado_nombre or '-'}"
        ))
        info.addStretch()
        info.addWidget(self._lbl_detalle(
            f"Fecha: {factura.fecha_hora or '-'}"
        ))
        lay.addLayout(info)

        # Tabla de productos
        tabla = QTableWidget()
        tabla.setStyleSheet(styles.table_style())
        tabla.setColumnCount(6)
        tabla.setHorizontalHeaderLabels([
            "Cód.", "Producto", "Tipo",
            "Cantidad", "P. Compra", "Subtotal"
        ])

        _h = tabla.horizontalHeader()
        assert _h is not None
        _h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        _v = tabla.verticalHeader()
        assert _v is not None
        _v.setVisible(False)

        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.setRowCount(len(factura.lista_detalles))

        for i, d in enumerate(factura.lista_detalles):
            tipo = "Nuevo" if d.es_nuevo else "Inventario"
            tabla.setItem(i, 0, self._celda(str(d.id_detalle)))
            tabla.setItem(i, 1, self._celda(d.producto.nombre))
            tabla.setItem(i, 2, self._celda(tipo))
            tabla.setItem(i, 3, self._celda(str(d.cantidad_compra)))
            tabla.setItem(i, 4, self._celda(f"${d.precio_compra:,.0f}"))
            tabla.setItem(i, 5, self._celda(f"${d.subtotal:,.0f}"))
            tabla.setRowHeight(i, 44)

        lay.addWidget(tabla)

        # Total
        total_lbl = QLabel(f"Total: ${factura.total_factura:,.0f}")
        total_lbl.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        total_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        lay.addWidget(total_lbl)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet(styles.btn_secondary())
        btn_cerrar.setFixedHeight(38)
        btn_cerrar.clicked.connect(dlg.accept)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(btn_cerrar)
        lay.addLayout(btns)

        dlg.exec()
        
        
    def _lbl_detalle(self, texto: str, grande: bool = False) -> QLabel:
        lbl = QLabel(texto)
        if grande:
            lbl.setStyleSheet(
                f"font-size: 18px; font-weight: bold; color: {styles.COLOR_TEXT};"
            )
        else:
            lbl.setStyleSheet(
                f"font-size: 13px; color: {styles.COLOR_TEXT_MUTED};"
            )
        return lbl
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
    
    