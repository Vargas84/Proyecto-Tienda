# =============================================================================
# models/compra.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL (bug importante de Python):
#
#   class Compra:
#       lista_detalles = []   ← ESTO ES UN ATRIBUTO DE CLASE, NO DE INSTANCIA
#
# Cuando se define una lista así (fuera del __init__), Python crea UNA SOLA
# lista compartida entre TODOS los objetos Compra. Eso significa que si
# creas factura1 y factura2, al agregar un detalle a factura1, ese detalle
# también aparece en factura2. Es uno de los bugs más frecuentes en Python.
#
# El código original los definía en __init__ (correctamente), pero la clase
# Ventas tenía este mismo bug con productos_vendidos. Se corrige en ambos.
#
# CORRECCIONES:
#   1. Se eliminan los imports innecesarios (Productos, Proveedor, datetime).
#   2. Se agrega id_venta como alias de id_factura en Ventas (el controlador
#      usaba ambos nombres inconsistentemente).
#   3. __repr__ para depuración.
#
# PRINCIPIO APLICADO: SRP — Compra representa una factura de compra.
# No importa nada que no use directamente.
# =============================================================================
from models.proveedor import Proveedor

class Compra:
    """
    Representa una factura de compra completa.
    
    Atributos:
        id_factura (int): identificador único de la factura.
        proveedor: objeto Proveedor asociado (None hasta confirmar).
        lista_detalles (list): lista de objetos DetalleCompra.
        total_factura (float): suma de todos los subtotales.
        factura_confirmada (bool): True cuando la factura fue cerrada.
        fecha_hora (str | None): fecha/hora de confirmación.
    """

    def __init__(self, id_factura: int):
        self.id_factura        = id_factura
        self.proveedor: Proveedor  | None = None       # Se asigna al confirmar
        # CORRECCIÓN: lista definida en __init__, no como atributo de clase.
        # Cada instancia de Compra tiene su PROPIA lista independiente.
        self.lista_detalles    = []
        self.total_factura     = 0
        self.factura_confirmada = False
        self.fecha_hora:str     | None  = None     # Se asigna al confirmar

    def agregar_detalle(self, detalle):
        """
        Agrega un objeto DetalleCompra a la factura y acumula su subtotal.
        
        Parámetros:
            detalle (DetalleCompra): el detalle a agregar.
        """
        self.lista_detalles.append(detalle)
        # Acumulamos el subtotal en tiempo real para tenerlo disponible
        # sin recorrer la lista cada vez.
        self.total_factura += detalle.subtotal

    def calcular_total(self) -> float:
        """
        Recalcula el total desde cero recorriendo todos los detalles.
        Útil después de editar o eliminar productos de la factura,
        ya que el acumulador en agregar_detalle() quedaría desfasado.
        
        Retorna:
            float: suma de todos los subtotales de la factura.
        """
        self.total_factura = sum(d.subtotal for d in self.lista_detalles)
        return self.total_factura

    def __repr__(self) -> str:
        return (
            f"Compra(id={self.id_factura}, "
            f"confirmada={self.factura_confirmada}, "
            f"total={self.total_factura}, "
            f"detalles={len(self.lista_detalles)})"
        )