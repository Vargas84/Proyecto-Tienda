# =============================================================================
# services/auth_service.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Contiene toda la lógica de negocio relacionada con usuarios:
#   - Registrar un nuevo usuario (con todas sus reglas)
#   - Iniciar sesión (verificar documento y contraseña)
#   - Buscar un usuario por documento
#
# ANTES: esta lógica estaba dentro de los bloques if op_inicio == 1 y
# op_inicio == 2 del controlador, mezclada con los input() y print().
# Había bucles while True para cada campo, validaciones inline y
# la creación del objeto Usuarios todo en el mismo lugar.
#
# AHORA:
#   - AuthService  → decide las reglas (este archivo)
#   - UI           → pide los datos y muestra resultados (Paso 5)
#   - Repository   → guarda y busca usuarios (Paso 3)
#
# PRINCIPIO APLICADO:
#   DIP — AuthService depende de UsuarioRepository (abstracción),
#   no de listas concretas. Si cambias el almacenamiento, el service
#   no cambia nada.
#
# CÓMO SE INYECTA LA DEPENDENCIA:
#   El service recibe el repository en su __init__, no lo crea él mismo.
#   Esto se llama "inyección de dependencias" — quien construye el service
#   decide qué repository usar. En main.py conectaremos todo.
#
#   auth_service = AuthService(usuario_repository)
#   ← el service no sabe si el repo usa listas, archivos o base de datos
# =============================================================================

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from exceptions.app_exceptions import (
    UsuarioYaExisteError,
    UsuarioNoEncontradoError,
    CredencialesInvalidasError,
)


class AuthService:
    """
    Servicio de autenticación y gestión de usuarios.

    Coordina las operaciones de registro e inicio de sesión,
    aplicando las reglas de negocio del sistema.
    """

    def __init__(self, usuario_repo: UsuarioRepository):
        # Guardamos la referencia al repository como atributo privado.
        # El service NUNCA accede directamente a listas — siempre pasa
        # por el repository. Así cumplimos el DIP.
        self._usuario_repo = usuario_repo

    # -------------------------------------------------------------------------
    # REGISTRO DE USUARIO
    # -------------------------------------------------------------------------

    def registrar_usuario(self, nombre: str, documento: int,
                          telefono: int, correo: str,
                          contrasena: str) -> Usuario:
        """
        Registra un nuevo usuario en el sistema.

        Recibe los datos ya validados (la UI se encargó de validarlos
        con los validators antes de llamar a este método).

        Este método aplica las reglas de negocio:
          - Verifica que documento, teléfono y correo no estén en uso
          - Crea el objeto Usuario
          - Lo guarda en el repository

        ANTES: toda esta lógica estaba en el bloque if op_inicio == 1,
        con tres bucles while True separados chequeando duplicados.

        Parámetros:
            nombre (str): nombre completo del usuario
            documento (int): número de documento ya convertido a int
            telefono (int): teléfono ya convertido a int
            correo (str): correo electrónico
            contrasena (str): contraseña que cumple los criterios

        Retorna:
            Usuario: el objeto creado y guardado

        Lanza:
            UsuarioYaExisteError: si documento, teléfono o correo
                                  ya están registrados
        """
        # El repository ya verifica duplicados internamente y lanza
        # UsuarioYaExisteError si encuentra alguno. No necesitamos
        # repetir esa lógica aquí.
        nuevo_usuario = Usuario(nombre, documento, telefono, correo, contrasena)

        # guardar() lanza UsuarioYaExisteError si hay duplicado.
        # La UI capturará esa excepción y mostrará el mensaje.
        self._usuario_repo.guardar(nuevo_usuario)

        return nuevo_usuario

    # -------------------------------------------------------------------------
    # INICIO DE SESIÓN
    # -------------------------------------------------------------------------

    def iniciar_sesion(self, documento: int,
                       contrasena: str) -> Usuario:
        """
        Verifica las credenciales e inicia sesión.

        ANTES: este flujo estaba en if op_inicio == 2, con un for para
        buscar el documento y luego un if para comparar la contraseña,
        todo mezclado con print() y continue.

        Parámetros:
            documento (int): documento ingresado por el usuario
            contrasena (str): contraseña ingresada

        Retorna:
            Usuario: el objeto del usuario autenticado

        Lanza:
            UsuarioNoEncontradoError: si el documento no existe
            CredencialesInvalidasError: si la contraseña no coincide
        """
        # Paso 1: buscar el usuario por documento
        usuario = self._usuario_repo.buscar_por_documento(documento)

        if usuario is None:
            # Usamos un mensaje genérico a propósito — buena práctica
            # de seguridad: no revelar si el error es en el documento
            # o en la contraseña.
            raise UsuarioNoEncontradoError(
                "Documento o contraseña incorrectos"
            )

        # Paso 2: verificar la contraseña usando el método del modelo
        # (la comparación es responsabilidad del propio Usuario)
        if not usuario.verificar_contrasena(contrasena):
            raise CredencialesInvalidasError(
                "Documento o contraseña incorrectos"
            )

        # Si llegamos aquí, las credenciales son correctas
        return usuario

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def buscar_usuario(self, documento: int) -> Usuario:
        """
        Busca un usuario por documento y lo retorna.
        Se usa para verificar si un documento ya existe antes de
        registrar proveedores o clientes.

        Lanza:
            UsuarioNoEncontradoError: si no existe
        """
        usuario = self._usuario_repo.buscar_por_documento(documento)
        if usuario is None:
            raise UsuarioNoEncontradoError(
                f"No existe un usuario con el documento {documento}"
            )
        return usuario

    def documento_de_empleado_existe(self, documento: int) -> bool:
        """
        Verifica si un documento pertenece a un empleado registrado.

        ANTES: en el controlador, al registrar proveedores y clientes,
        se chequeaba que el documento no fuera de un empleado con un
        bucle for sobre inventario.usuarios_registrados.

        AHORA: un método claro con nombre descriptivo.

        Retorna:
            True si el documento pertenece a un empleado registrado.
        """
        return self._usuario_repo.documento_existe(documento)

    def telefono_de_empleado_existe(self, telefono: int) -> bool:
        """
        Verifica si un teléfono pertenece a un empleado registrado.
        Misma lógica que documento_de_empleado_existe para teléfono.
        """
        return self._usuario_repo.telefono_existe(telefono)

    def obtener_todos_los_usuarios(self) -> list:
        """Retorna la lista de todos los usuarios registrados."""
        return self._usuario_repo.obtener_todos()