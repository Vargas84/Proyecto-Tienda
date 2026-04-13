# =============================================================================
# repositories/compra_repository.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Gestiona el almacenamiento de facturas de compra confirmadas y
# la generación de IDs para facturas y detalles.
#
# ANTES: inventario.lista_compras, inventario.generar_id_compra(),
# inventario.liberar_id_compra() y inventario.generar_id_detalle()
# estaban todos en la clase Inventario mezclados con todo lo demás.
#
# AHORA: cada uno en su lugar correspondiente.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from models.compra import Compra


class CompraRepository(BaseRepository):
    """
    Implementación en memoria del repositorio de facturas de compra.
    
    Solo almacena facturas CONFIRMADAS. Las facturas en proceso
    viven temporalmente en el service hasta que se confirman.
    """

    def __init__(self):
        # Lista privada de facturas confirmadas
        self._compras: list[Compra] = []

        # Contadores de IDs — equivalen a los del Inventario original
        self._siguiente_id_factura: int = 1
        self._siguiente_id_detalle: int = 1

    # -------------------------------------------------------------------------
    # GENERACIÓN DE IDs
    # -------------------------------------------------------------------------

    def generar_id_factura(self) -> int:
        """
        Genera el próximo ID para una nueva factura de compra.
        ANTES: inventario.generar_id_compra()
        """
        id_generado = self._siguiente_id_factura
        self._siguiente_id_factura += 1
        return id_generado

    def liberar_id_factura(self) -> None:
        """
        Devuelve el último ID de factura cuando se cancela la compra.
        ANTES: inventario.liberar_id_compra()
        """
        if self._siguiente_id_factura > 1:
            self._siguiente_id_factura -= 1

    def generar_id_detalle(self) -> int:
        """
        Genera el próximo ID para un detalle dentro de una factura.
        ANTES: inventario.generar_id_detalle()
        
        NOTA: el contador de detalle se reinicia en cada factura nueva.
        Eso lo maneja el service al llamar a reiniciar_contador_detalle().
        """
        id_generado = self._siguiente_id_detalle
        self._siguiente_id_detalle += 1
        return id_generado

    def reiniciar_contador_detalle(self) -> None:
        """
        Reinicia el contador de detalles a 1.
        Se llama al iniciar una nueva factura, igual que hacía
        inventario.detalle_id = 1 en el controlador original.
        """
        self._siguiente_id_detalle = 1

    # -------------------------------------------------------------------------
    # OPERACIONES CRUD
    # -------------------------------------------------------------------------

    def guardar(self, compra: Compra) -> None:# type: ignore[override]
        """
        Guarda una factura de compra confirmada.
        ANTES: inventario.lista_compras.append(factura)
        """
        self._compras.append(compra)

    def buscar_por_id(self, id_factura: int) -> Optional[Compra]:# type: ignore[override]
        """
        Busca una factura de compra por su ID.
        Retorna None si no existe.
        """
        for compra in self._compras:
            if compra.id_factura == id_factura:
                return compra
        return None

    def obtener_todos(self) -> list[Compra]:
        """Retorna todas las facturas de compra confirmadas."""
        return self._compras[:]

    def eliminar(self, id_factura: int) -> bool:# type: ignore[override]
        """
        Las facturas confirmadas no se eliminan en este sistema
        (el controlador original tampoco lo permitía).
        Se incluye para cumplir el contrato de BaseRepository.
        Retorna False siempre.
        """
        return False

    # -------------------------------------------------------------------------
    # BÚSQUEDAS ESPECÍFICAS
    # -------------------------------------------------------------------------

    def buscar_por_mes_anio(self, mes: int, anio: int) -> list[Compra]:
        """
        Filtra facturas por mes y año de confirmación.
        
        ANTES: este filtrado estaba inline en el controlador con un bucle
        for que parseaba la fecha manualmente. Ahora vive aquí.
        
        La fecha tiene formato 'dd/mm/yyyy hh:mm:ss' — parseamos igual
        que el original para mantener compatibilidad.
        
        Retorna:
            Lista de facturas que corresponden al mes y año dados.
            Lista vacía si no hay ninguna.
        """
        resultados = []
        for compra in self._compras:
            if compra.fecha_hora is None:
                continue
            # 'dd/mm/yyyy hh:mm:ss' → split('/') → ['dd','mm','yyyy hh:mm:ss']
            partes = compra.fecha_hora.split('/')
            mes_factura  = int(partes[1])
            anio_factura = int(partes[2][:4])
            if mes_factura == mes and anio_factura == anio:
                resultados.append(compra)
        return resultados

    def total_facturas(self) -> int:
        """Retorna la cantidad de facturas de compra confirmadas."""
        return len(self._compras)

    def hay_facturas(self) -> bool:
        """Retorna True si hay al menos una factura guardada."""
        return len(self._compras) > 0