# =============================================================================
# models/proveedor.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# La clase original era correcta en estructura pero le faltaban:
#   1. __repr__ para depuración.
#   2. Tipos de datos explícitos en __init__.
#
# PRINCIPIO APLICADO: SRP — Proveedor solo representa los datos
# de quien nos vende mercancía. Sin lógica de negocio.
# =============================================================================


class Proveedor:
    """
    Representa a un proveedor al que le compramos mercancía.
    
    Atributos:
        nombre_empresa (str): nombre de la empresa o persona proveedora.
        documento (int): NIT o cédula del proveedor.
        telefono (int): número de contacto (10 dígitos).
    """

    def __init__(self, nombre_empresa: str, documento: int, telefono: int):
        # Mantenemos los mismos nombres de atributos que en la clase original
        # para no romper el código que ya los usa (nombre_empresa, documento, telefono)
        self.nombre_empresa = nombre_empresa
        self.documento      = documento
        self.telefono       = telefono

    def __repr__(self) -> str:
        return (
            f"Proveedor(nombre='{self.nombre_empresa}', "
            f"documento={self.documento})"
        )