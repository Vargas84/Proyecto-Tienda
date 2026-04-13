# =============================================================================
# models/cliente.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# La clase original era mínima y correcta en estructura.
# Se añaden tipos, docstring y __repr__.
#
# NOTA SOBRE nombre_cliente:
# Mantenemos el atributo como 'nombre_cliente' (igual que el original)
# para no romper el controlador que ya usa cliente.nombre_cliente.
# =============================================================================


class Cliente:
    """
    Representa a un cliente que compra productos del negocio.
    
    Atributos:
        nombre_cliente (str): nombre completo del cliente.
        documento (int): número de documento (8-10 dígitos).
        telefono (int): número de contacto (10 dígitos).
    """

    def __init__(self, nombre_cliente: str, documento: int, telefono: int):
        self.nombre_cliente = nombre_cliente
        self.documento      = documento
        self.telefono       = telefono

    def __repr__(self) -> str:
        return (
            f"Cliente(nombre='{self.nombre_cliente}', "
            f"documento={self.documento})"
        )