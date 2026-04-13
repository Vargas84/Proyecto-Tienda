# =============================================================================
# repositories/producto_repository.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Centraliza toda la gestión de productos del inventario:
#   - Guardar productos nuevos
#   - Buscar por ID o por nombre
#   - Listar todo el inventario
#   - Verificar existencia de nombres duplicados
#   - Generar IDs automáticamente
#
# ANTES: la clase Inventario mezclaba generación de IDs, búsquedas,
# lógica de negocio (registrar_compra con input()) y presentación
# (mostrar_inventario con print()). Todo en un solo objeto.
#
# AHORA:
#   - ProductoRepository → gestiona el almacenamiento (este archivo)
#   - ProductoService    → lógica de negocio (Paso 4)
#   - UI                 → presentación (Paso 5)
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from models.producto import Producto
from exceptions.app_exceptions import (
    ProductoYaExisteError,
    ProductoNoEncontradoError,
)


class ProductoRepository(BaseRepository):
    """
    Implementación en memoria del repositorio de productos.
    
    Reemplaza la lista inventario.lista_productos y todos los métodos
    de búsqueda que estaban en la clase Inventario original.
    """

    def __init__(self):
        # Lista privada de productos
        self._productos: list[Producto] = []

        # Contador de IDs — equivale a inventario.productos_id del original.
        # Generamos IDs aquí porque el repository es quien "posee" los datos.
        self._siguiente_id: int = 1

    # -------------------------------------------------------------------------
    # GENERACIÓN DE ID
    # -------------------------------------------------------------------------

    def generar_id(self) -> int:
        """
        Genera y reserva el próximo ID disponible para un producto.
        
        ANTES: inventario.generar_id_productos() hacía esto mismo pero
        vivía en la clase Inventario junto con todo lo demás.
        
        AHORA: vive aquí porque el repository es el dueño del almacenamiento
        y por lo tanto el responsable de asignar identificadores.
        
        Retorna:
            int: el ID generado (autoincremental, empieza en 1).
        """
        id_generado = self._siguiente_id
        self._siguiente_id += 1
        return id_generado

    def liberar_ultimo_id(self) -> None:
        """
        Devuelve el último ID generado cuando una operación se cancela.
        
        ANTES: inventario.liberar_id_compra() y liberar_id_venta().
        Se llama cuando el usuario cancela antes de confirmar,
        para que el ID no quede "quemado" sin usarse.
        """
        if self._siguiente_id > 1:
            self._siguiente_id -= 1

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD
    # -------------------------------------------------------------------------

    def guardar(self, producto: Producto) -> None: # type: ignore[override]
        """
        Agrega un producto nuevo al inventario.
        
        Verifica que el nombre no esté duplicado (sin importar mayúsculas
        ni espacios) antes de guardar.
        
        Lanza:
            ProductoYaExisteError: si ya existe un producto con ese nombre.
        """
        nombre_normalizado = producto.nombre.lower().replace(" ", "")

        for p in self._productos:
            if p.nombre.lower().replace(" ", "") == nombre_normalizado:
                raise ProductoYaExisteError(
                    f"Ya existe un producto con el nombre '{producto.nombre}'"
                )

        self._productos.append(producto)

    def buscar_por_id(self, codigo: int) -> Optional[Producto]:# type: ignore[override]
        """
        Busca un producto por su código (ID).
        
        ANTES: inventario.buscar_producto_id(codigo_producto).
        Misma lógica, ahora en su lugar correcto.
        
        Retorna:
            Producto si existe, None si no.
        """
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_por_nombre(self, nombre: str) -> Optional[Producto]:
        """
        Busca un producto por nombre, ignorando mayúsculas y espacios.
        
        ANTES: inventario.buscar_producto() tenía un bug: el return None
        estaba dentro del for, así que nunca buscaba más allá del primer
        elemento. Aquí está correctamente afuera del bucle.
        
        Retorna:
            Producto si existe, None si no.
        """
        nombre_normalizado = nombre.lower().replace(" ", "")
        for producto in self._productos:
            if producto.nombre.lower().replace(" ", "") == nombre_normalizado:
                return producto
        # El return None está AFUERA del for — bug corregido respecto al original
        return None

    def obtener_todos(self) -> list[Producto]:
        """
        Retorna todos los productos del inventario.
        Retorna copia para proteger la lista interna.
        """
        return self._productos[:]

    def obtener_disponibles(self) -> list[Producto]:
        """
        Retorna solo los productos marcados como disponibles.
        Útil para el menú de ventas donde solo se puede vender
        lo que está disponible.
        """
        return [p for p in self._productos if p.esta_disponible()]

    def eliminar(self, codigo: int) -> bool:# type: ignore[override]
        """
        Elimina un producto por su código.
        Retorna True si se encontró y eliminó, False si no existía.
        """
        for producto in self._productos:
            if producto.codigo == codigo:
                self._productos.remove(producto)
                return True
        return False

    # -------------------------------------------------------------------------
    # VERIFICACIONES DE EXISTENCIA
    # -------------------------------------------------------------------------

    def nombre_existe(self, nombre: str) -> bool:
        """
        Verifica si ya existe un producto con ese nombre.
        Útil para validar antes de agregar sin necesitar el objeto.
        """
        return self.buscar_por_nombre(nombre) is not None

    def total_productos(self) -> int:
        """Retorna la cantidad de productos en el inventario."""
        return len(self._productos)

    def inventario_vacio(self) -> bool:
        """Retorna True si no hay productos registrados."""
        return len(self._productos) == 0