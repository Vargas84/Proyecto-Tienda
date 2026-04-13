# =============================================================================
# repositories/venta_repository.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Gestiona el almacenamiento de facturas de venta confirmadas y
# la generación de IDs para ventas y detalles de venta.
#
# ANTES: inventario.lista_ventas, inventario.generar_id_venta(),
# inventario.liberar_id_venta() y inventario.generar_id_detalle_venta()
# estaban en la clase Inventario.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from models.venta import Venta


class VentaRepository(BaseRepository):
    """
    Implementación en memoria del repositorio de facturas de venta.
    Solo almacena ventas CONFIRMADAS.
    """

    def __init__(self):
        self._ventas: list[Venta] = []

        # Equivalen a inventario.ventas_id y inventario.detalle_venta_id
        self._siguiente_id_venta:   int = 1
        self._siguiente_id_detalle: int = 1

    # -------------------------------------------------------------------------
    # GENERACIÓN DE IDs
    # -------------------------------------------------------------------------

    def generar_id_venta(self) -> int:
        """
        Genera el próximo ID para una factura de venta.
        ANTES: inventario.generar_id_venta()
        """
        id_generado = self._siguiente_id_venta
        self._siguiente_id_venta += 1
        return id_generado

    def liberar_id_venta(self) -> None:
        """
        Devuelve el último ID cuando se cancela la venta.
        ANTES: inventario.liberar_id_venta()
        """
        if self._siguiente_id_venta > 1:
            self._siguiente_id_venta -= 1

    def generar_id_detalle(self) -> int:
        """
        Genera el próximo ID para un detalle dentro de una factura de venta.
        ANTES: inventario.generar_id_detalle_venta()
        """
        id_generado = self._siguiente_id_detalle
        self._siguiente_id_detalle += 1
        return id_generado

    def reiniciar_contador_detalle(self) -> None:
        """
        Reinicia el contador de detalles a 1 al comenzar una nueva venta.
        ANTES: inventario.detalle_venta_id = 1 en el controlador.
        """
        self._siguiente_id_detalle = 1

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD
    # -------------------------------------------------------------------------

    def guardar(self, venta: Venta) -> None:# type: ignore[override]
        """
        Guarda una factura de venta confirmada.
        ANTES: inventario.lista_ventas.append(factura_venta)
        """
        self._ventas.append(venta)

    def buscar_por_id(self, id_venta: int) -> Optional[Venta]:# type: ignore[override]
        """Busca una venta por su ID. Retorna None si no existe."""
        for venta in self._ventas:
            if venta.id_venta == id_venta:
                return venta
        return None

    def obtener_todos(self) -> list[Venta]:
        """Retorna todas las ventas confirmadas."""
        return self._ventas[:]

    def eliminar(self, id_venta: int) -> bool:# type: ignore[override]
        """
        Las ventas confirmadas no se eliminan (igual que en el original).
        Incluido para cumplir el contrato de BaseRepository.
        """
        return False

    # -------------------------------------------------------------------------
    # BÚSQUEDAS ESPECÍFICAS
    # -------------------------------------------------------------------------

    def buscar_por_mes_anio(self, mes: int, anio: int) -> list[Venta]:
        """
        Filtra ventas por mes y año de confirmación.
        
        ANTES: este bucle de filtrado estaba inline en el controlador.
        La fecha tiene formato 'dd/mm/yyyy hh:mm:ss'.
        
        Retorna:
            Lista de ventas del periodo. Lista vacía si no hay ninguna.
        """
        resultados = []
        for venta in self._ventas:
            if venta.fecha is None:
                continue
            partes = venta.fecha.split('/')
            mes_venta  = int(partes[1])
            anio_venta = int(partes[2][:4])
            if mes_venta == mes and anio_venta == anio:
                resultados.append(venta)
        return resultados

    def total_ventas(self) -> int:
        """Retorna la cantidad de facturas de venta confirmadas."""
        return len(self._ventas)

    def hay_ventas(self) -> bool:
        """Retorna True si hay al menos una venta guardada."""
        return len(self._ventas) > 0