# =============================================================================
# ui_qt/login_window.py
# =============================================================================
# Ventana de inicio de sesión y registro de usuarios.
# Reemplaza auth_ui.py de la consola.
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
    La ventana principal escucha esa señal para abrir el menú de gestión.
    """

    # Señal que lleva el objeto Usuario autenticado
    login_exitoso = pyqtSignal(object)

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self._auth = auth_service
        self._v_nombre    = NombreValidator()
        self._v_documento = DocumentoValidator()
        self._v_telefono  = TelefonoValidator()
        self._v_correo    = CorreoValidator()
        self._v_contrasena = ContrasenaValidator()

        self._construir_ui()

    def _construir_ui(self):
        self.setWindowTitle("Sistema de Inventarios — Acceso")
        self.setFixedSize(420, 580)
        self.setStyleSheet(f"background-color: {styles.COLOR_BG};")

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo / título
        titulo = QLabel("📦 Sistema de Inventarios")
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

        # Tarjeta contenedora
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

        # Stack: vista login / vista registro
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

        # Documento
        lay.addWidget(self._label("Número de documento"))
        self._inp_doc_login = QLineEdit()
        self._inp_doc_login.setPlaceholderText("Ej: 12345678")
        self._inp_doc_login.setStyleSheet(styles.input_field())
        self._inp_doc_login.setFixedHeight(40)
        lay.addWidget(self._inp_doc_login)

        # Contraseña
        lay.addWidget(self._label("Contraseña"))
        self._inp_pass_login = QLineEdit()
        self._inp_pass_login.setPlaceholderText("Tu contraseña")
        self._inp_pass_login.setEchoMode(QLineEdit.EchoMode.Password)
        self._inp_pass_login.setStyleSheet(styles.input_field())
        self._inp_pass_login.setFixedHeight(40)
        self._inp_pass_login.returnPressed.connect(self._hacer_login)
        lay.addWidget(self._inp_pass_login)

        lay.addSpacing(8)

        # Botón login
        btn_login = QPushButton("Iniciar sesión")
        btn_login.setStyleSheet(styles.btn_primary())
        btn_login.setFixedHeight(42)
        btn_login.clicked.connect(self._hacer_login)
        lay.addWidget(btn_login)

        # Link a registro
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
        lay.setSpacing(8)

        titulo = QLabel("Crear usuario")
        titulo.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {styles.COLOR_TEXT};"
        )
        lay.addWidget(titulo)

        campos = [
            ("Nombre completo",    "_inp_nombre",    "Ana García",     False),
            ("Documento",          "_inp_doc_reg",   "12345678",       False),
            ("Teléfono",           "_inp_tel",       "3001234567",     False),
            ("Correo electrónico", "_inp_correo",    "ana@gmail.com",  False),
            ("Contraseña",         "_inp_pass_reg",  "Mínimo 8 chars", True),
        ]

        for label_txt, attr, placeholder, es_pass in campos:
            lay.addWidget(self._label(label_txt))
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setStyleSheet(styles.input_field())
            inp.setFixedHeight(38)
            if es_pass:
                inp.setEchoMode(QLineEdit.EchoMode.Password)
            setattr(self, attr, inp)
            lay.addWidget(inp)

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

        # Validamos cada campo con los validators
        for valor, validator, campo in [
            (nombre,   self._v_nombre,    "nombre"),
            (doc_str,  self._v_documento, "documento"),
            (tel_str,  self._v_telefono,  "teléfono"),
            (correo,   self._v_correo,    "correo"),
            (password, self._v_contrasena,"contraseña"),
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
            # Limpiar campos y volver a login
            for attr in ['_inp_nombre','_inp_doc_reg','_inp_tel',
                         '_inp_correo','_inp_pass_reg']:
                getattr(self, attr).clear()
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
        QMessageBox.warning(self, "Error", msg)

    def _exito(self, msg: str):
        QMessageBox.information(self, "Éxito", msg)