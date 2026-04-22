# =============================================================================
# ui_qt/inventario_window.py
# =============================================================================
# Módulo de gestión del inventario de productos.
# Muestra todos los productos en una tabla y permite agregar,
# editar disponibilidad y modificar atributos.
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QDialog, QFormLayout, QLineEdit, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

from services.producto_service import ProductoService
from validators.campo_validator import (
    NombreValidator, PrecioValidator, StockValidator, CategoriaValidator
)
from exceptions.app_exceptions import AppError, ProductoYaExisteError
from ui_qt import styles


class InventarioWindow(QWidget):
    """Módulo de gestión del inventario."""

    def __init__(self, prod_svc: ProductoService):
        super().__init__()
        self._prod_svc    = prod_svc
        self._v_nombre    = NombreValidator()
        self._v_precio    = PrecioValidator()
        self._v_stock     = StockValidator()
        self._v_categoria = CategoriaValidator()
        self._construir_ui()
        self._cargar_productos()

    def _construir_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        # Encabezado
        header = QHBoxLayout()
        titulo = QLabel("Inventario de productos")
        titulo.setStyleSheet(styles.label_title())
        header.addWidget(titulo)
        header.addStretch()

        btn_agregar = QPushButton("+ Agregar producto")
        btn_agregar.setStyleSheet(styles.btn_primary())
        btn_agregar.setFixedHeight(38)
        btn_agregar.clicked.connect(self._dlg_agregar)
        header.addWidget(btn_agregar)
        lay.addLayout(header)

        subtitulo = QLabel("Gestiona el stock, precios y disponibilidad de tus productos")
        subtitulo.setStyleSheet(styles.label_subtitle())
        lay.addWidget(subtitulo)

        # Tabla
        self._tabla = QTableWidget()
        self._tabla.setStyleSheet(styles.table_style())
        self._tabla.setColumnCount(7)
        self._tabla.setHorizontalHeaderLabels([
            "Código", "Nombre", "Precio", "Stock",
            "Categoría", "Disponibilidad", "Acciones"
        ])
        self._tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._tabla.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self._tabla.horizontalHeader().setSectionResizeMode(
            6, QHeaderView.ResizeMode.ResizeToContents
        )
        self._tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self._tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self._tabla.verticalHeader().setVisible(False)
        self._tabla.setAlternatingRowColors(True)
        lay.addWidget(self._tabla)

    def _cargar_productos(self):
        """Recarga la tabla con los productos actuales del repository."""
        productos = self._prod_svc.obtener_todos()
        self._tabla.setRowCount(len(productos))

        for fila, p in enumerate(productos):
            self._tabla.setItem(fila, 0, self._celda(str(p.codigo)))
            self._tabla.setItem(fila, 1, self._celda(p.nombre))
            self._tabla.setItem(fila, 2, self._celda(f"${p.precio:,.0f}"))
            self._tabla.setItem(fila, 3, self._celda(str(p.stock)))
            self._tabla.setItem(fila, 4, self._celda(p.categoria))

            # Disponibilidad con color
            disp_item = QTableWidgetItem(p.disponibilidad)
            disp_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if p.disponibilidad == "Disponible":
                disp_item.setForeground(QColor("#16A34A"))
            else:
                disp_item.setForeground(QColor("#DC2626"))
            self._tabla.setItem(fila, 5, disp_item)

            # Botones de acción en la columna Acciones
            self._tabla.setCellWidget(fila, 6, self._acciones(p))
            self._tabla.setRowHeight(fila, 48)

    def _acciones(self, producto) -> QWidget:
        """Crea los botones de acción para cada fila."""
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(6)

        btn_editar = QPushButton("Editar")
        btn_editar.setStyleSheet(styles.btn_secondary())
        btn_editar.setFixedHeight(30)
        btn_editar.clicked.connect(
            lambda _, p=producto: self._dlg_editar(p)
        )

        texto_disp = ("Desactivar" if producto.disponibilidad == "Disponible"
                      else "Activar")
        btn_disp = QPushButton(texto_disp)
        btn_disp.setStyleSheet(
            styles.btn_danger() if producto.disponibilidad == "Disponible"
            else styles.btn_success()
        )
        btn_disp.setFixedHeight(30)
        btn_disp.clicked.connect(
            lambda _, p=producto: self._cambiar_disponibilidad(p)
        )

        lay.addWidget(btn_editar)
        lay.addWidget(btn_disp)
        return w

    # -------------------------------------------------------------------------
    # DIÁLOGOS
    # -------------------------------------------------------------------------

    def _dlg_agregar(self):
        """Diálogo para agregar un nuevo producto."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Agregar producto")
        dlg.setFixedSize(380, 320)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        titulo = QLabel("Nuevo producto")
        titulo.setStyleSheet(styles.label_title())
        lay.addWidget(titulo)

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre    = self._inp("Ej: Jabón líquido")
        inp_precio    = self._inp("Ej: 5000")
        inp_categoria = self._inp("Ej: Aseo")
        inp_stock     = self._inp("Ej: 50")

        form.addRow("Nombre:",    inp_nombre)
        form.addRow("Precio:",    inp_precio)
        form.addRow("Categoría:", inp_categoria)
        form.addRow("Stock:",     inp_stock)
        lay.addLayout(form)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Agregar")
        btn_ok.setStyleSheet(styles.btn_primary())
        btn_ok.clicked.connect(lambda: self._guardar_producto(
            dlg, inp_nombre, inp_precio, inp_categoria, inp_stock
        ))

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)

        dlg.exec()

    def _guardar_producto(self, dlg, inp_nombre, inp_precio,
                          inp_categoria, inp_stock):
        nombre    = inp_nombre.text().strip()
        precio    = inp_precio.text().strip()
        categoria = inp_categoria.text().strip()
        stock     = inp_stock.text().strip()

        for valor, validator, campo in [
            (nombre,    self._v_nombre,    "nombre"),
            (precio,    self._v_precio,    "precio"),
            (categoria, self._v_categoria, "categoría"),
            (stock,     self._v_stock,     "stock"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                QMessageBox.warning(self, "Error", f"{campo}: {e}")
                return

        if not self._prod_svc.nombre_disponible(nombre):
            QMessageBox.warning(self, "Error",
                                f"'{nombre}' ya está registrado.")
            return

        try:
            p = self._prod_svc.agregar_producto(
                nombre, float(precio), categoria, int(stock)
            )
            QMessageBox.information(
                self, "Éxito",
                f"Producto '{p.nombre}' agregado con código {p.codigo}."
            )
            dlg.accept()
            self._cargar_productos()
        except AppError as e:
            QMessageBox.warning(self, "Error", str(e))

    def _dlg_editar(self, producto):
        """Diálogo para editar atributos de un producto."""
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Editar: {producto.nombre}")
        dlg.setFixedSize(380, 320)
        dlg.setStyleSheet(f"background-color: {styles.COLOR_SURFACE};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(12)

        titulo = QLabel(f"Editando: {producto.nombre}")
        titulo.setStyleSheet(styles.label_title())
        lay.addWidget(titulo)

        sub = QLabel("Deja vacío el campo que no quieras cambiar")
        sub.setStyleSheet(styles.label_subtitle())
        lay.addWidget(sub)

        form = QFormLayout()
        form.setSpacing(10)

        inp_nombre    = self._inp(producto.nombre)
        inp_precio    = self._inp(str(producto.precio))
        inp_categoria = self._inp(producto.categoria)
        inp_stock     = self._inp(str(producto.stock))

        form.addRow("Nombre:",    inp_nombre)
        form.addRow("Precio:",    inp_precio)
        form.addRow("Categoría:", inp_categoria)
        form.addRow("Stock:",     inp_stock)
        lay.addLayout(form)

        btns = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(styles.btn_secondary())
        btn_cancel.clicked.connect(dlg.reject)

        btn_ok = QPushButton("Guardar cambios")
        btn_ok.setStyleSheet(styles.btn_primary())
        btn_ok.clicked.connect(lambda: self._guardar_edicion(
            dlg, producto, inp_nombre, inp_precio, inp_categoria, inp_stock
        ))

        btns.addWidget(btn_cancel)
        btns.addWidget(btn_ok)
        lay.addLayout(btns)

        dlg.exec()

    def _guardar_edicion(self, dlg, producto, inp_nombre, inp_precio,
                         inp_categoria, inp_stock):
        cambios = 0
        try:
            if inp_nombre.text().strip():
                self._prod_svc.editar_nombre(
                    producto.codigo, inp_nombre.text().strip()
                )
                cambios += 1
            if inp_precio.text().strip():
                self._v_precio.validar(inp_precio.text().strip())
                self._prod_svc.editar_precio(
                    producto.codigo, float(inp_precio.text().strip())
                )
                cambios += 1
            if inp_categoria.text().strip():
                self._v_categoria.validar(inp_categoria.text().strip())
                self._prod_svc.editar_categoria(
                    producto.codigo, inp_categoria.text().strip()
                )
                cambios += 1
            if inp_stock.text().strip():
                self._v_stock.validar(inp_stock.text().strip())
                self._prod_svc.editar_stock(
                    producto.codigo, int(inp_stock.text().strip())
                )
                cambios += 1
        except AppError as e:
            QMessageBox.warning(self, "Error", str(e))
            return

        if cambios == 0:
            QMessageBox.information(self, "Sin cambios",
                                    "No se modificó ningún campo.")
        else:
            QMessageBox.information(self, "Éxito",
                                    "Producto actualizado correctamente.")
        dlg.accept()
        self._cargar_productos()

    def _cambiar_disponibilidad(self, producto):
        nuevo = ("No Disponible" if producto.disponibilidad == "Disponible"
                 else "Disponible")
        resp = QMessageBox.question(
            self, "Confirmar",
            f"¿Cambiar '{producto.nombre}' a {nuevo}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resp == QMessageBox.StandardButton.Yes:
            self._prod_svc.cambiar_disponibilidad(producto.codigo)
            self._cargar_productos()

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