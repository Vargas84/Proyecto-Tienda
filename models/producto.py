# =============================================================================
# models/producto.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL: la clase Productos (plural) mezclaba la representación
# del dato con lógica de presentación. Los métodos aumentar_stock(),
# disminuir_stock() y actualizar_stock() hacían print() directamente,
# lo que significa que la entidad tomaba decisiones de UI.
#
# CORRECCIONES:
#   1. Nombre cambiado a Producto (singular) — cada objeto ES un producto,
#      no una colección. Convención estándar en Python y en diseño de dominio.
#   2. aumentar_stock() y disminuir_stock() ahora LANZAN excepciones en vez
#      de hacer print(). La UI decide cómo mostrar el error.
#   3. actualizar_stock() corregido: el atributo era self.disponible (con bug
#      de nombre) — ahora usa self.disponibilidad consistentemente.
#   4. mostrar_informacion() simplificado: el if/else era idéntico en ambas
#      ramas salvo un espacio extra, se unificó.
#   5. Se agrega __repr__ para facilitar depuración.
#
# PRINCIPIO APLICADO: SRP — la clase solo representa un producto y
# sus operaciones propias. No imprime, no valida input del usuario.
# =============================================================================

from exceptions.app_exceptions import StockInsuficienteError, ValorFueraDeRangoError


class Producto:
    """
    Representa un producto dentro del inventario.
    
    Atributos:
        codigo (int | None): identificador único. Es None cuando el producto
            es nuevo y aún no ha sido confirmado en una factura de compra.
        nombre (str): nombre del producto.
        precio (float): precio de venta al público.
        categoria (str): categoría a la que pertenece.
        stock (int): unidades disponibles en inventario.
        disponibilidad (str): 'Disponible' o 'No Disponible'.
    """

    # Constantes del dominio — si el negocio cambia los textos,
    # se modifica aquí y aplica en todo el sistema automáticamente.
    DISPONIBLE     = "Disponible"
    NO_DISPONIBLE  = "No Disponible"

    def __init__(self, codigo, nombre: str, precio: float,
                 categoria: str, stock: int):
        self.codigo       = codigo    # None hasta que se confirma en factura
        self.nombre       = nombre
        self.precio       = precio
        self.categoria    = categoria
        self.stock        = stock
        # Inicia como Disponible; cambia automáticamente si el stock llega a 0
        self.disponibilidad = self.DISPONIBLE

    # -------------------------------------------------------------------------
    # MÉTODOS DE DOMINIO
    # Operaciones que tienen sentido sobre el propio producto.
    # No hacen print(), no piden input(). Solo modifican estado y/o lanzan
    # excepciones cuando algo no es válido.
    # -------------------------------------------------------------------------

    def cambiar_disponibilidad(self):
        """
        Alterna la disponibilidad entre 'Disponible' y 'No Disponible'.
        Lo llama el usuario/trabajador cuando quiere activar o desactivar
        un producto manualmente.
        
        
        NOTA: el nombre cambió de cambiarDisponibilidad() (camelCase)
        a cambiar_disponibilidad() (snake_case) para seguir la convención
        estándar de Python (PEP 8).
        """
        if self.disponibilidad == self.DISPONIBLE:
            self.disponibilidad = self.NO_DISPONIBLE
        else:
            self.disponibilidad = self.DISPONIBLE

    def aumentar_stock(self, cantidad: int):
        """
        Suma 'cantidad' al stock actual del producto.
        Se llama cuando se confirma una factura de compra.
        
        CAMBIO RESPECTO AL ORIGINAL: en vez de print("La cantidad debe ser
        mayor a cero"), ahora lanza ValorFueraDeRangoError. La UI captura
        esa excepción y decide cómo mostrarla.
        
        Lanza:
            ValorFueraDeRangoError: si cantidad <= 0
        """
        if cantidad <= 0:
            raise ValorFueraDeRangoError(
                "La cantidad a aumentar debe ser mayor a 0"
            )
        self.stock += cantidad

        # Si el producto estaba marcado como No Disponible por falta de stock
        # y ahora llega mercancía, lo reactivamos automáticamente.
        if self.disponibilidad == self.NO_DISPONIBLE:
            self.disponibilidad = self.DISPONIBLE

    def disminuir_stock(self, cantidad: int):
        """
        Resta 'cantidad' del stock actual del producto.
        Se llama cuando se confirma una factura de venta.
        
        CAMBIO RESPECTO AL ORIGINAL: lanza excepciones en vez de print().
        Además marca automáticamente el producto como No Disponible
        si el stock llega a 0 (lógica que antes estaba dispersa en el
        controlador dentro del bloque de confirmar venta).
        
        Lanza:
            ValorFueraDeRangoError: si cantidad <= 0
            StockInsuficienteError: si cantidad > stock disponible
        """
        if cantidad <= 0:
            raise ValorFueraDeRangoError(
                "La cantidad a descontar debe ser mayor a 0"
            )
        if cantidad > self.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente. Solo hay {self.stock} "
                f"unidades de '{self.nombre}'"
            )

        self.stock -= cantidad

        # Si el stock llega exactamente a 0, marcamos como No Disponible.
        # Antes esta lógica estaba en el controlador (if p.stock == 0: ...).
        # Ahora vive donde corresponde: en la propia entidad.
        if self.stock == 0:
            self.disponibilidad = self.NO_DISPONIBLE

    def esta_disponible(self) -> bool:
        """
        Retorna True si el producto está disponible para vender.
        Método de conveniencia para no comparar strings en la UI.
        
        Uso:
            if producto.esta_disponible(): ...
        En vez de:
            if producto.disponibilidad == "Disponible": ...
        """
        return self.disponibilidad == self.DISPONIBLE

    # -------------------------------------------------------------------------
    # REPRESENTACIÓN
    # -------------------------------------------------------------------------

    def mostrar_informacion(self) -> str:
        """
        Retorna una línea formateada con los datos del producto,
        lista para imprimir en la tabla del inventario.
        
        CAMBIO: el if/else original era idéntico en ambas ramas
        (solo difería en un espacio extra). Se unificó en una sola línea.
        """
        return (
            f"{self.codigo:<10} | {self.nombre:<20} | {self.precio:<10} | "
            f"{self.stock:<10} | {self.categoria:<15} | {self.disponibilidad:<20}"
        )

    def __repr__(self) -> str:
        """
        Representación técnica del objeto. Útil para depuración.
        Cuando haces print(producto) o lo ves en el debugger, muestra esto.
        """
        return (
            f"Producto(codigo={self.codigo}, nombre='{self.nombre}', "
            f"precio={self.precio}, stock={self.stock})"
        )