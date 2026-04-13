# =============================================================================
# repositories/base_repository.py
# =============================================================================
# ¿POR QUÉ UNA CLASE BASE ABSTRACTA?
#
# PRINCIPIOS APLICADOS:
#   - DIP (Dependency Inversion Principle): el resto del sistema (services,
#     UI) depende de ESTA abstracción, no de la implementación concreta.
#     Eso significa que si mañana cambias de listas en memoria a MySQL,
#     solo creas una nueva clase que herede de BaseRepository y el resto
#     del sistema no se entera del cambio.
#
#   - Polimorfismo: todos los repositories son intercambiables porque
#     comparten la misma interfaz. Un UsuarioRepository y un
#     ProductoRepository se usan igual desde afuera.
#
#   - OCP (Open/Closed): puedes agregar nuevos repositories sin modificar
#     los existentes ni la clase base.
#
# ANALOGÍA:
#   BaseRepository es como el contrato de un empleado de almacén.
#   El contrato dice: "debes saber guardar, buscar, listar y eliminar".
#   Cada almacén (memoria, base de datos, archivo) implementa esas
#   tareas a su manera, pero el jefe (service) siempre les habla igual.
# =============================================================================

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Contrato abstracto que todo repository del sistema debe cumplir.
    Define las 4 operaciones fundamentales de persistencia (CRUD).

    NOTA SOBRE *args y **kwargs:
    Pylance exige que los nombres de parámetros coincidan exactamente
    entre la clase base y cada subclase. Como cada repository usa nombres
    distintos (compra, usuario, producto...), usamos *args para que cada
    subclase pueda nombrar sus parámetros libremente sin conflicto.
    """

    @abstractmethod
    def guardar(self, *args, **kwargs) -> None:
        """
        Persiste una nueva entidad en el almacenamiento.
        Equivale al INSERT en bases de datos.
        Cada subclase define el tipo exacto de su parámetro.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, *args, **kwargs):
        """
        Busca y retorna una entidad por su identificador único.
        Equivale al SELECT WHERE id = ? en bases de datos.
        Retorna el objeto si existe, None si no.
        """
        pass

    @abstractmethod
    def obtener_todos(self) -> list:
        """
        Retorna todas las entidades almacenadas.
        Equivale al SELECT * en bases de datos.
        """
        pass

    @abstractmethod
    def eliminar(self, *args, **kwargs) -> bool:
        """
        Elimina una entidad por su identificador único.
        Equivale al DELETE WHERE id = ? en bases de datos.
        Retorna True si se eliminó, False si no existía.
        """
        pass