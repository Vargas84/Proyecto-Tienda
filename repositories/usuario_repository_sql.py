# =============================================================================
# repositories/usuario_repository_sql.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Es la versión SQLite de UsuarioRepository. Implementa exactamente
# la misma interfaz (BaseRepository) que la versión en memoria, pero
# en vez de guardar en listas, guarda en la tabla 'usuarios' de la BD.
#
# PRINCIPIO DIP EN ACCIÓN:
# AuthService recibe un UsuarioRepository en su __init__ y no sabe
# si es en memoria o SQL — solo llama a guardar(), buscar_por_documento(),
# etc. Al cambiar de UsuarioRepository a UsuarioRepositorySQL en main.py,
# el service no cambia ni una línea.
#
# OPERACIONES SQL QUE SE USAN:
#   INSERT INTO  → guardar()
#   SELECT       → buscar_por_documento(), obtener_todos()
#   DELETE       → eliminar()
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from repositories.db.conexion import obtener
from models.usuario import Usuario
from exceptions.app_exceptions import UsuarioYaExisteError


class UsuarioRepositorySQL(BaseRepository):
    """
    Implementación SQLite del repositorio de usuarios.
    Reemplaza a UsuarioRepository (listas en memoria) en producción.
    """

    def __init__(self):
        # Obtenemos la conexión compartida — no creamos una nueva.
        # El singleton de conexion.py garantiza que es siempre la misma.
        self._con = obtener()

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD
    # -------------------------------------------------------------------------

    def guardar(self, usuario: Usuario) -> None:
        """
        Inserta un nuevo usuario en la tabla 'usuarios'.

        Verifica duplicados de documento, teléfono y correo antes
        de insertar — igual que hacía la versión en memoria.

        Lanza:
            UsuarioYaExisteError: si documento, teléfono o correo
                                  ya están registrados.
        """
        # Verificamos duplicados antes del INSERT para dar mensajes claros.
        # La BD tiene UNIQUE en esos campos y lanzaría IntegrityError,
        # pero ese error es genérico — con esta verificación previa
        # podemos decir exactamente qué campo está duplicado.
        if self.documento_existe(usuario.documento):
            raise UsuarioYaExisteError(
                f"El documento {usuario.documento} ya está en uso"
            )
        if self.telefono_existe(usuario.telefono):
            raise UsuarioYaExisteError(
                f"El teléfono {usuario.telefono} ya está en uso"
            )
        if self.correo_existe(usuario.correo):
            raise UsuarioYaExisteError(
                f"El correo {usuario.correo} ya está en uso"
            )

        # INSERT con parámetros posicionales (?).
        # NUNCA usar f-strings para valores SQL — eso abre la puerta
        # a inyección SQL. Los ? hacen que SQLite escape los valores
        # automáticamente.
        self._con.execute(
            """
            INSERT INTO usuarios (nombre, documento, telefono, correo, contrasena)
            VALUES (?, ?, ?, ?, ?)
            """,
            (usuario.nombre, usuario.documento, usuario.telefono,
             usuario.correo, usuario.contrasena)
        )
        self._con.commit()
        # commit() escribe los cambios en disco permanentemente.
        # Sin commit(), los cambios existen en memoria pero se pierden
        # si el programa se cierra antes de que SQLite los flush.

    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:  # type: ignore[override]
        """
        Busca un usuario por su ID interno de base de datos.
        En este sistema se usa poco — la búsqueda principal es por documento.
        """
        fila = self._con.execute(
            "SELECT * FROM usuarios WHERE id = ?",
            (id_usuario,)
        ).fetchone()
        # fetchone() retorna la primera fila o None si no hay resultados.
        return self._fila_a_usuario(fila) if fila else None

    def obtener_todos(self) -> list[Usuario]:
        """
        Retorna todos los usuarios registrados.
        SELECT * FROM usuarios ordena por ID para consistencia.
        """
        filas = self._con.execute(
            "SELECT * FROM usuarios ORDER BY id"
        ).fetchall()
        # fetchall() retorna todas las filas como lista.
        # Si no hay filas retorna lista vacía [].
        return [self._fila_a_usuario(f) for f in filas]

    def eliminar(self, documento: int) -> bool:
        """
        Elimina un usuario por su documento.
        Retorna True si se eliminó, False si no existía.
        """
        cursor = self._con.execute(
            "DELETE FROM usuarios WHERE documento = ?",
            (documento,)
        )
        self._con.commit()
        # rowcount indica cuántas filas fueron afectadas.
        # Si es 0, el documento no existía.
        return cursor.rowcount > 0

    # -------------------------------------------------------------------------
    # BÚSQUEDAS ESPECÍFICAS DEL DOMINIO
    # -------------------------------------------------------------------------

    def buscar_por_documento(self, documento: int) -> Optional[Usuario]:
        """
        Busca un usuario por documento. Es la búsqueda principal del sistema.
        Se usa en login y en validación de proveedores/clientes.

        Usa el índice idx_usuarios_documento definido en schema.sql
        para que la búsqueda sea O(log n) en vez de O(n).
        """
        fila = self._con.execute(
            "SELECT * FROM usuarios WHERE documento = ?",
            (documento,)
        ).fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def buscar_por_correo(self, correo: str) -> Optional[Usuario]:
        """Busca un usuario por correo electrónico."""
        fila = self._con.execute(
            "SELECT * FROM usuarios WHERE correo = ?",
            (correo,)
        ).fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def buscar_por_telefono(self, telefono: int) -> Optional[Usuario]:
        """Busca un usuario por teléfono."""
        fila = self._con.execute(
            "SELECT * FROM usuarios WHERE telefono = ?",
            (telefono,)
        ).fetchone()
        return self._fila_a_usuario(fila) if fila else None

    def documento_existe(self, documento: int) -> bool:
        """Verifica si un documento ya está registrado."""
        fila = self._con.execute(
            "SELECT 1 FROM usuarios WHERE documento = ?",
            (documento,)
        ).fetchone()
        # "SELECT 1" es más eficiente que "SELECT *" cuando solo
        # necesitamos saber si existe — no trae todos los campos,
        # solo un 1 si encuentra algo o None si no.
        return fila is not None

    def telefono_existe(self, telefono: int) -> bool:
        """Verifica si un teléfono ya está registrado."""
        fila = self._con.execute(
            "SELECT 1 FROM usuarios WHERE telefono = ?",
            (telefono,)
        ).fetchone()
        return fila is not None

    def correo_existe(self, correo: str) -> bool:
        """Verifica si un correo ya está registrado."""
        fila = self._con.execute(
            "SELECT 1 FROM usuarios WHERE correo = ?",
            (correo,)
        ).fetchone()
        return fila is not None

    def total_usuarios(self) -> int:
        """Retorna la cantidad de usuarios registrados."""
        fila = self._con.execute(
            "SELECT COUNT(*) FROM usuarios"
        ).fetchone()
        return fila[0]

    # -------------------------------------------------------------------------
    # MÉTODO PRIVADO DE CONVERSIÓN
    # -------------------------------------------------------------------------

    def _fila_a_usuario(self, fila) -> Usuario:
        """
        Convierte una fila de SQLite en un objeto Usuario.

        Gracias a row_factory = sqlite3.Row en conexion.py,
        podemos acceder a los campos por nombre: fila["nombre"]
        en vez de fila[0]. Mucho más claro y seguro.

        Este patrón (fila → objeto del dominio) se repite en todos
        los repositories SQL — es el equivalente al ORM manual.
        """
        return Usuario(
            nombre    = fila["nombre"],
            documento = fila["documento"],
            telefono  = fila["telefono"],
            correo    = fila["correo"],
            contrasena = fila["contrasena"]
        )