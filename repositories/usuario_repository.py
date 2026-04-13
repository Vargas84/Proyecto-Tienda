# =============================================================================
# repositories/usuario_repository.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Centraliza TODA la gestión de usuarios en un solo lugar:
#   - Guardar usuarios nuevos
#   - Buscar por documento (para login)
#   - Buscar por correo o teléfono (para verificar duplicados)
#   - Listar todos los usuarios
#
# ANTES: estas búsquedas estaban dispersas en el controlador con bucles
# for repetidos en cada validación:
#
#   for usuario in inventario.usuarios_registrados:
#       if usuario.documento == documento: ...   ← en crear usuario
#
#   for usuario in inventario.usuarios_registrados:
#       if usuario.documento == doc_login: ...   ← en iniciar sesión
#
#   for usuario in inventario.usuarios_registrados:
#       if usuario.documento == documento_proveedor: ...  ← en compras
#
# AHORA: un solo método buscar_por_documento() que se reutiliza en los
# tres casos. Si el día de mañana usas una BD, solo cambias este archivo.
#
# IMPLEMENTACIÓN: en memoria (listas de Python).
# Si en el futuro quieres usar SQLite o MySQL, creas
# UsuarioRepositorioSQLite(BaseRepository) con la misma interfaz
# y el resto del sistema no cambia nada.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from models.usuario import Usuario
from exceptions.app_exceptions import UsuarioYaExisteError


class UsuarioRepository(BaseRepository):
    """
    Implementación en memoria del repositorio de usuarios.
    
    Gestiona el almacenamiento y búsqueda de objetos Usuario.
    Reemplaza el atributo inventario.usuarios_registrados y todos
    los bucles de búsqueda que estaban en el controlador.
    """

    def __init__(self):
        # Lista privada — nadie fuera de esta clase accede directamente.
        # El guión bajo (_) es la convención de Python para "uso interno".
        # Antes era inventario.usuarios_registrados (pública y accesible
        # desde cualquier parte del código).
        self._usuarios: list[Usuario] = []

        # Contador interno de IDs. Cada usuario recibe un ID único
        # autoincremental, igual que haría una base de datos.
        # NOTA: en tu sistema original los usuarios no tenían ID propio
        # (se identificaban solo por documento). Lo mantenemos así —
        # el documento sigue siendo el identificador de negocio.
        self._contador_id: int = 1

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD — implementan el contrato de BaseRepository
    # -------------------------------------------------------------------------

    def guardar(self, usuario: Usuario) -> None:# type: ignore[override]
        """
        Registra un nuevo usuario en el sistema.
        
        Verifica que no existan duplicados de documento, teléfono y correo
        antes de guardar. Si alguno ya existe, lanza UsuarioYaExisteError.
        
        ANTES: estas verificaciones estaban en el controlador con tres
        bucles for separados, uno para cada campo.
        
        AHORA: un solo método que encapsula toda la lógica de unicidad.
        
        Lanza:
            UsuarioYaExisteError: si documento, teléfono o correo
                                  ya están registrados.
        """
        # Verificamos los tres campos que deben ser únicos
        for u in self._usuarios:
            if u.documento == usuario.documento:
                raise UsuarioYaExisteError(
                    f"El documento {usuario.documento} ya está en uso"
                )
            if u.telefono == usuario.telefono:
                raise UsuarioYaExisteError(
                    f"El teléfono {usuario.telefono} ya está en uso"
                )
            if u.correo == usuario.correo:
                raise UsuarioYaExisteError(
                    f"El correo {usuario.correo} ya está en uso"
                )

        self._usuarios.append(usuario)

    def buscar_por_id(self, id_entidad: int) -> Optional[Usuario]:# type: ignore[override]
        """
        Busca un usuario por su posición en la lista (índice).
        No se usa frecuentemente — en este dominio se busca por documento.
        """
        for usuario in self._usuarios:
            if id(usuario) == id_entidad:
                return usuario
        return None

    def obtener_todos(self) -> list[Usuario]:
        """
        Retorna una copia de la lista de usuarios.
        
        Retornamos una copia ([:]) para que nadie pueda modificar
        la lista interna accidentalmente desde afuera.
        """
        return self._usuarios[:]

    def eliminar(self, id_entidad: int) -> bool:# type: ignore[override]
        """
        Elimina un usuario por documento.
        Retorna True si se eliminó, False si no se encontró.
        """
        for usuario in self._usuarios:
            if usuario.documento == id_entidad:
                self._usuarios.remove(usuario)
                return True
        return False

    # -------------------------------------------------------------------------
    # BÚSQUEDAS ESPECÍFICAS DEL DOMINIO DE USUARIOS
    # Métodos adicionales que el contrato base no define pero este
    # repository necesita para su dominio específico.
    # -------------------------------------------------------------------------

    def buscar_por_documento(self, documento: int) -> Optional[Usuario]:
        """
        Busca y retorna el usuario con ese número de documento.
        
        Es el método principal de búsqueda — se usa en:
          - Login (verificar que el documento existe)
          - Validación de proveedores y clientes (verificar que el
            documento NO sea de un empleado registrado)
        
        Retorna:
            El objeto Usuario si existe, None si no.
        """
        for usuario in self._usuarios:
            if usuario.documento == documento:
                return usuario
        return None

    def buscar_por_correo(self, correo: str) -> Optional[Usuario]:
        """
        Busca un usuario por su correo electrónico.
        Se usa para verificar duplicados al registrar.
        """
        for usuario in self._usuarios:
            if usuario.correo == correo:
                return usuario
        return None

    def buscar_por_telefono(self, telefono: int) -> Optional[Usuario]:
        """
        Busca un usuario por su número de teléfono.
        Se usa para verificar duplicados al registrar.
        """
        for usuario in self._usuarios:
            if usuario.telefono == telefono:
                return usuario
        return None

    def documento_existe(self, documento: int) -> bool:
        """
        Verifica rápidamente si un documento ya está registrado.
        Útil cuando solo necesitas saber si existe, sin obtener el objeto.
        """
        return self.buscar_por_documento(documento) is not None

    def telefono_existe(self, telefono: int) -> bool:
        """
        Verifica rápidamente si un teléfono ya está registrado.
        """
        return self.buscar_por_telefono(telefono) is not None

    def correo_existe(self, correo: str) -> bool:
        """
        Verifica rápidamente si un correo ya está registrado.
        """
        return self.buscar_por_correo(correo) is not None

    def total_usuarios(self) -> int:
        """Retorna la cantidad de usuarios registrados."""
        return len(self._usuarios)