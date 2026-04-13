# =============================================================================
# models/venta.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL (mismo bug de Python que en Compra):
# productos_vendidos se definía en __init__ correctamente como [],
# pero el controlador usaba DOS nombres distintos para el mismo objeto:
#   - factura_venta.productos_vendidos  (al agregar y ver productos)
#   - venta.codigo_venta               (al mostrar facturas guardadas)
#   - id_venta                         (al crear la factura)
# Esto generaba confusión. Se unifica en esta clase con atributos claros.
#
# CORRECCIONES:
#   1. Se elimina el import de datetime — la fecha se recibe ya formateada
#      desde el service, no se calcula aquí.
#   2. Se elimina el import de Cliente — Venta recibe el objeto ya construido.
#   3. id_venta y codigo_venta unifican: el atributo principal es id_venta,
#      y codigo_venta es una propiedad que apunta al mismo valor para
#      mantener compatibilidad con el código existente.
#   4. calcular_total() para recalcular después de editar detalles.
#   5. __repr__ para depuración.
#
# PRINCIPIO APLICADO: SRP — Venta representa una factura de venta.
# =============================================================================
from models.cliente import Cliente

class Venta:
    """
    Representa una factura de venta completa.
    
    Atributos:
        id_venta (int): identificador único de la factura.
        cliente: objeto Cliente asociado (None hasta confirmar).
        fecha (str | None): fecha/hora de confirmación.
        productos_vendidos (list): lista de objetos DetalleVenta.
        total_venta (float): suma de todos los subtotales.
        venta_confirmada (bool): True cuando la factura fue cerrada.
    """

    def __init__(self, id_venta: int):
        self.id_venta          = id_venta
        self.cliente: Cliente  | None  = None     # Se asigna al confirmar
        self.fecha:str         | None  = None     # Se asigna al confirmar
        # CORRECCIÓN: lista en __init__ para que cada Venta tenga la suya.
        self.productos_vendidos = []
        self.total_venta       = 0
        self.venta_confirmada  = False

    @property
    def codigo_venta(self):
        """
        Propiedad de compatibilidad.
        
        El controlador original usaba 'factura_venta.id_venta' al crear
        la factura y 'venta.codigo_venta' al leer las guardadas.
        Con esta propiedad, ambos nombres apuntan al mismo valor sin
        romper código existente.
        """
        return self.id_venta

    def agregar_detalle(self, detalle):
        """
        Agrega un objeto DetalleVenta a la factura y acumula su subtotal.
        
        Parámetros:
            detalle (DetalleVenta): el detalle a agregar.
        """
        self.productos_vendidos.append(detalle)
        self.total_venta += detalle.subtotal

    def calcular_total(self) -> float:
        """
        Recalcula el total desde cero.
        Necesario después de editar o eliminar productos de la factura.
        
        Retorna:
            float: suma de todos los subtotales.
        """
        self.total_venta = sum(d.subtotal for d in self.productos_vendidos)
        return self.total_venta

    def __repr__(self) -> str:
        return (
            f"Venta(id={self.id_venta}, "
            f"confirmada={self.venta_confirmada}, "
            f"total={self.total_venta}, "
            f"productos={len(self.productos_vendidos)})"
        )