# =============================================================================
# ui_qt/login_window.py
# =============================================================================
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
    QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from services.auth_service import AuthService
from validators.campo_validator import (
    NombreValidator, DocumentoValidator, TelefonoValidator,
    CorreoValidator, ContrasenaValidator
)
from exceptions.app_exceptions import (
    AppError, UsuarioYaExisteError,
    UsuarioNoEncontradoError, CredencialesInvalidasError
)
from ui_qt import styles


class LoginWindow(QMainWindow):
    """
    Ventana principal de autenticación.
    Tiene dos vistas: login y registro, alternadas con QStackedWidget.
    Emite la señal login_exitoso(usuario) cuando el login es correcto.
    """

    login_exitoso = pyqtSignal(object)

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self._auth = auth_service
        self._v_nombre     = NombreValidator()
        self._v_documento  = DocumentoValidator()
        self._v_telefono   = TelefonoValidator()
        self._v_correo     = CorreoValidator()
        self._v_contrasena = ContrasenaValidator()

        # Declaramos los atributos aquí para que Pylance los reconozca.
        # Si se declaran dentro de _vista_registro() con setattr(),
        # Pylance no puede inferir su tipo y los marca como desconocidos.
        self._inp_nombre:    QLineEdit = QLineEdit()
        self._inp_doc_reg:   QLineEdit = QLineEdit()
        self._inp_tel:       QLineEdit = QLineEdit()
        self._inp_correo:    QLineEdit = QLineEdit()
        self._inp_pass_reg:  QLineEdit = QLineEdit()

        self._construir_ui()

    def _construir_ui(self):
        self.setWindowTitle("Sistema de Inventarios — Acceso")
        self.setFixedSize(460, 720)
        self.setStyleSheet(f"background-color: {styles.COLOR_BG};")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        titulo = QLabel(" Sistema de Inventarios")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet(
            f"font-size: 22px; font-weight: bold; color: {styles.COLOR_TEXT};"
            f"margin-bottom: 8px;"
        )
        layout.addWidget(titulo)

        subtitulo = QLabel("Gestión de productos, compras y ventas")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet(styles.label_subtitle())
        layout.addWidget(subtitulo)
        layout.addSpacing(24)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {styles.COLOR_SURFACE};
                border: 1px solid {styles.COLOR_BORDER};
                border-radius: 12px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(12)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._vista_login())
        self._stack.addWidget(self._vista_registro())
        card_layout.addWidget(self._stack)

        layout.addWidget(card)

    # -------------------------------------------------------------------------
    # VISTA LOGIN
    # -------------------------------------------------------------------------

    def _vista_login(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        titulo = QLabel("Iniciar sesión")
        titulo.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        lay.addWidget(titulo)
        lay.addSpacing(4)

        lay.addWidget(self._label("Número de documento"))
        self._inp_doc_login = QLineEdit()
        self._inp_doc_login.setPlaceholderText("Ej: 12345678")
        self._inp_doc_login.setStyleSheet(styles.input_field())
        self._inp_doc_login.setFixedHeight(40)
        lay.addWidget(self._inp_doc_login)

        lay.addWidget(self._label("Contraseña"))
        self._inp_pass_login = QLineEdit()
        self._inp_pass_login.setPlaceholderText("Tu contraseña")
        self._inp_pass_login.setEchoMode(QLineEdit.EchoMode.Password)
        self._inp_pass_login.setStyleSheet(styles.input_field())
        self._inp_pass_login.setFixedHeight(40)
        self._inp_pass_login.returnPressed.connect(self._hacer_login)
        lay.addWidget(self._inp_pass_login)

        lay.addSpacing(8)

        btn_login = QPushButton("Iniciar sesión")
        btn_login.setStyleSheet(styles.btn_primary())
        btn_login.setFixedHeight(42)
        btn_login.clicked.connect(self._hacer_login)
        lay.addWidget(btn_login)

        lay.addSpacing(4)
        link = QPushButton("¿No tienes cuenta? Crear usuario")
        link.setStyleSheet(
            f"color: {styles.COLOR_PRIMARY}; border: none; "
            f"background: transparent; font-size: 12px;"
        )
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.clicked.connect(lambda: self._stack.setCurrentIndex(1))
        lay.addWidget(link, alignment=Qt.AlignmentFlag.AlignCenter)

        return w

    # -------------------------------------------------------------------------
    # VISTA REGISTRO
    # -------------------------------------------------------------------------

    def _vista_registro(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(6)
        lay.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("Crear usuario")
        titulo.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        lay.addWidget(titulo)

        # Campos declarados explícitamente (no con setattr en bucle)
        # para que Pylance reconozca el tipo de cada atributo.
        lay.addWidget(self._label("Nombre completo"))
        self._inp_nombre = QLineEdit()
        self._inp_nombre.setPlaceholderText("Ana García")
        self._inp_nombre.setStyleSheet(styles.input_field())
        self._inp_nombre.setFixedHeight(36)
        lay.addWidget(self._inp_nombre)

        lay.addWidget(self._label("Documento"))
        self._inp_doc_reg = QLineEdit()
        self._inp_doc_reg.setPlaceholderText("12345678")
        self._inp_doc_reg.setStyleSheet(styles.input_field())
        self._inp_doc_reg.setFixedHeight(36)
        lay.addWidget(self._inp_doc_reg)

        lay.addWidget(self._label("Teléfono"))
        self._inp_tel = QLineEdit()
        self._inp_tel.setPlaceholderText("3001234567")
        self._inp_tel.setStyleSheet(styles.input_field())
        self._inp_tel.setFixedHeight(36)
        lay.addWidget(self._inp_tel)

        lay.addWidget(self._label("Correo electrónico"))
        self._inp_correo = QLineEdit()
        self._inp_correo.setPlaceholderText("ana@gmail.com")
        self._inp_correo.setStyleSheet(styles.input_field())
        self._inp_correo.setFixedHeight(36)
        lay.addWidget(self._inp_correo)

        lay.addWidget(self._label("Contraseña"))
        self._inp_pass_reg = QLineEdit()
        self._inp_pass_reg.setPlaceholderText("Mínimo 8 chars")
        self._inp_pass_reg.setStyleSheet(styles.input_field())
        self._inp_pass_reg.setFixedHeight(36)
        self._inp_pass_reg.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self._inp_pass_reg)

        lay.addSpacing(6)

        btn_reg = QPushButton("Crear usuario")
        btn_reg.setStyleSheet(styles.btn_primary())
        btn_reg.setFixedHeight(42)
        btn_reg.clicked.connect(self._hacer_registro)
        lay.addWidget(btn_reg)

        link = QPushButton("¿Ya tienes cuenta? Iniciar sesión")
        link.setStyleSheet(
            f"color: {styles.COLOR_PRIMARY}; border: none; "
            f"background: transparent; font-size: 12px;"
        )
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        lay.addWidget(link, alignment=Qt.AlignmentFlag.AlignCenter)

        return w

    # -------------------------------------------------------------------------
    # LÓGICA
    # -------------------------------------------------------------------------

    def _hacer_login(self):
        doc_str  = self._inp_doc_login.text().strip()
        password = self._inp_pass_login.text()

        if not doc_str:
            self._error("Ingresa tu número de documento.")
            return

        try:
            doc = int(doc_str)
        except ValueError:
            self._error("El documento debe ser un número.")
            return

        try:
            usuario = self._auth.iniciar_sesion(doc, password)
            self._inp_doc_login.clear()
            self._inp_pass_login.clear()
            self.login_exitoso.emit(usuario)
        except (UsuarioNoEncontradoError, CredencialesInvalidasError) as e:
            self._error(str(e))

    def _hacer_registro(self):
        nombre   = self._inp_nombre.text().strip()
        doc_str  = self._inp_doc_reg.text().strip()
        tel_str  = self._inp_tel.text().strip()
        correo   = self._inp_correo.text().strip()
        password = self._inp_pass_reg.text()

        for valor, validator, campo in [
            (nombre,   self._v_nombre,     "nombre"),
            (doc_str,  self._v_documento,  "documento"),
            (tel_str,  self._v_telefono,   "teléfono"),
            (correo,   self._v_correo,     "correo"),
            (password, self._v_contrasena, "contraseña"),
        ]:
            try:
                validator.validar(valor)
            except AppError as e:
                self._error(f"Error en {campo}: {e}")
                return

        try:
            self._auth.registrar_usuario(
                nombre, int(doc_str), int(tel_str), correo, password
            )
            self._exito("Usuario creado correctamente. Ya puedes iniciar sesión.")
            self._inp_nombre.clear()
            self._inp_doc_reg.clear()
            self._inp_tel.clear()
            self._inp_correo.clear()
            self._inp_pass_reg.clear()
            self._stack.setCurrentIndex(0)
        except UsuarioYaExisteError as e:
            self._error(str(e))

    # -------------------------------------------------------------------------
    # UTILIDADES
    # -------------------------------------------------------------------------

    def _label(self, texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        return lbl


    def _error(self, msg: str):
        styles.mostrar_mensaje(self, "Error", msg, "warning")

    def _exito(self, msg: str):
        styles.mostrar_mensaje(self, "Éxito", msg, "info")
        
    """def _error(self, msg: str):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle("Error")
        box.setText(msg)
        box.setStyleSheet(styles.msgbox_style())
        box.exec()

    def _exito(self, msg: str):
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Éxito")
        box.setText(msg)
        box.setStyleSheet(styles.msgbox_style())
        box.exec()"""
    