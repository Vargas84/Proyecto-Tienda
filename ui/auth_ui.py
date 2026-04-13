# =============================================================================
# ui/auth_ui.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Maneja toda la interacción con el usuario para autenticación:
#   - Mostrar el menú de inicio de sesión
#   - Recoger y validar datos de registro
#   - Recoger datos de login
#   - Llamar a AuthService y mostrar el resultado
#
# RESPONSABILIDAD ÚNICA: solo interactúa con el usuario y llama
# al service. No decide si el usuario existe o si la contraseña
# es correcta — eso lo hace AuthService.
#
# ANTES: todo esto estaba dentro de inventarioSistema() mezclado
# con la lógica de inventario, compras y ventas.
# =============================================================================

from services.auth_service import AuthService
from validators.campo_validator import (
    NombreValidator,
    DocumentoValidator,
    TelefonoValidator,
    CorreoValidator,
    ContrasenaValidator,
)
from exceptions.app_exceptions import (
    AppError,
    UsuarioYaExisteError,
    UsuarioNoEncontradoError,
    CredencialesInvalidasError,
)
from ui.ui_utils import pedir_dato, pedir_opcion, titulo


class AuthUI:
    """
    Interfaz de usuario para autenticación.
    Recibe AuthService por inyección de dependencia.
    """

    def __init__(self, auth_service: AuthService):
        self._auth_svc = auth_service

        # Instanciamos los validators una sola vez al crear la UI.
        # ANTES: la validación estaba inline en cada while True.
        # AHORA: reutilizamos los mismos objetos en cada llamada.
        self._v_nombre    = NombreValidator()
        self._v_documento = DocumentoValidator()
        self._v_telefono  = TelefonoValidator()
        self._v_correo    = CorreoValidator()
        self._v_contrasena = ContrasenaValidator()

    # -------------------------------------------------------------------------
    # MENÚ PRINCIPAL DE AUTENTICACIÓN
    # -------------------------------------------------------------------------

    def ejecutar(self):
        """
        Muestra el menú de inicio de sesión en bucle.
        Retorna el objeto Usuario cuando el login es exitoso,
        o None si el usuario elige salir.

        ANTES: este era el while True más externo de inventarioSistema(),
        con if op_inicio == 1, 2, 3 dentro.
        """
        while True:
            print("\n======== INICIO DE SESIÓN ========")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Salir del sistema")

            opcion = pedir_opcion("Seleccione una opción: ", 1, 3)

            if opcion == 1:
                self._registrar_usuario()

            elif opcion == 2:
                usuario = self._iniciar_sesion()
                if usuario is not None:
                    # Login exitoso — retornamos el usuario al menú principal
                    return usuario

            elif opcion == 3:
                print("Gracias por usar el sistema.")
                return None

    # -------------------------------------------------------------------------
    # REGISTRO DE USUARIO
    # -------------------------------------------------------------------------

    def _registrar_usuario(self) -> None:
        """
        Recopila los datos del nuevo usuario, los valida y llama
        al service para registrarlo.

        ANTES: bloque if op_inicio == 1 con cinco bucles while True
        anidados, uno por cada campo. ~70 líneas.
        AHORA: cinco llamadas a pedir_dato() + una llamada al service.
        """
        print("\n======== CREAR USUARIO ========")

        # pedir_dato() maneja el bucle y la validación internamente.
        # Solo recibimos el valor cuando ya es correcto.
        nombre    = pedir_dato("Nombre: ", self._v_nombre)
        documento = pedir_dato(f"Documento de {nombre}: ",
                               self._v_documento)
        telefono  = pedir_dato(f"Teléfono de {nombre}: ",
                               self._v_telefono)
        correo    = pedir_dato(f"Correo de {nombre}: ",
                               self._v_correo)
        contrasena = pedir_dato(f"Contraseña de {nombre}: ",
                                self._v_contrasena)

        try:
            usuario = self._auth_svc.registrar_usuario(
                nombre,
                int(documento),
                int(telefono),
                correo,
                contrasena
            )
            print(f"\nUsuario '{usuario.nombre}' creado exitosamente.")

        except UsuarioYaExisteError as e:
            # El service detectó un duplicado de documento, teléfono o correo
            print(f"\nError: {e}")

    # -------------------------------------------------------------------------
    # INICIO DE SESIÓN
    # -------------------------------------------------------------------------

    def _iniciar_sesion(self):
        """
        Pide documento y contraseña, llama al service y retorna
        el usuario autenticado o None si falla.

        ANTES: bloque if op_inicio == 2 con try/except para el documento,
        búsqueda manual en la lista y comparación de contraseña inline.
        """
        print("\n======== INICIAR SESIÓN ========")

        try:
            doc_str = input("Número de documento: ")
            doc_int = int(doc_str)
        except ValueError:
            print("  Error: El documento debe ser un número.")
            return None

        contrasena = input("Contraseña: ")

        try:
            usuario = self._auth_svc.iniciar_sesion(doc_int, contrasena)
            print(f"\n¡Acceso concedido! Bienvenido/a, {usuario.nombre}.")
            return usuario

        except (UsuarioNoEncontradoError, CredencialesInvalidasError) as e:
            print(f"\nError: {e}")
            return None


    # -------------------------------------------------------------------------
    # RECOGER DATOS DE PERSONAS (proveedor / cliente)
    # Reutilizados en CompraUI y VentaUI para no duplicar la lógica
    # -------------------------------------------------------------------------

    def recoger_datos_persona(self, tipo: str) -> dict:
        """
        Recopila y valida nombre, documento y teléfono de una persona.
        Verifica que el documento y teléfono no pertenezcan a un empleado.

        ANTES: el mismo bloque de tres while True para proveedor y para
        cliente aparecía dos veces en el controlador (duplicado exacto).

        Parámetros:
            tipo (str): 'proveedor' o 'cliente' — solo para los mensajes

        Retorna:
            dict con claves 'nombre', 'documento' (int), 'telefono' (int)
        """
        print(f"\n--- Datos del {tipo} ---")

        nombre = pedir_dato(f"Nombre del {tipo}: ", self._v_nombre)

        # Documento — validamos formato Y que no sea de un empleado
        while True:
            doc_str = pedir_dato(
                f"Documento del {tipo} {nombre}: ",
                self._v_documento
            )
            doc_int = int(doc_str)
            if self._auth_svc.documento_de_empleado_existe(doc_int):
                print(f"  Error: ese documento pertenece a un empleado "
                      f"registrado. Ingrese otro.")
            else:
                break

        # Teléfono — validamos formato Y que no sea de un empleado
        while True:
            tel_str = pedir_dato(
                f"Teléfono del {tipo} {nombre}: ",
                self._v_telefono
            )
            tel_int = int(tel_str)
            if self._auth_svc.telefono_de_empleado_existe(tel_int):
                print(f"  Error: ese teléfono pertenece a un empleado "
                      f"registrado. Ingrese otro.")
            else:
                break

        return {
            "nombre":    nombre,
            "documento": doc_int,
            "telefono":  tel_int,
        }