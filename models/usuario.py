# =============================================================================
# models/usuario.py
# =============================================================================
# ¿QUÉ CAMBIÓ RESPECTO A LA CLASE ORIGINAL?
#
# PROBLEMA ORIGINAL: la clase Usuarios (plural) tenía métodos que NO
# pertenecen a un usuario como entidad del dominio:
#   - ver_inventario(inventario)         → le pertenece a la UI
#   - agregar_productos(inventario, p)   → le pertenece al InventarioService
#   - cambiar_disponibilidad_producto()  → le pertenece al ProductoService
#   - editar_productos()                 → le pertenece al ProductoService
#
# Un usuario del sistema es simplemente una persona con credenciales.
# No "sabe" cómo funciona el inventario — eso lo coordina el service.
#
# CORRECCIONES:
#   1. Nombre cambiado a Usuario (singular).
#   2. Se eliminaron todos los métodos de inventario — irán al service.
#   3. Se agrega verificar_contrasena() como método propio del usuario,
#      porque la comparación de contraseña SÍ le pertenece a esta entidad.
#   4. Se agrega __repr__ para facilitar depuración.
#
# PRINCIPIO APLICADO:
#   SRP — Usuario solo representa a un trabajador del sistema con sus
#   credenciales. No coordina operaciones de inventario.
# =============================================================================


class Usuario:
    """
    Representa a un trabajador registrado en el sistema.
    
    Atributos:
        nombre (str): nombre completo del trabajador.
        documento (int): número de documento de identidad (8-10 dígitos).
        telefono (int): número de teléfono (10 dígitos).
        correo (str): correo electrónico.
        contrasena (str): contraseña de acceso al sistema.
    """

    def __init__(self, nombre: str, documento: int, telefono: int,
                 correo: str, contrasena: str):
        self.nombre    = nombre
        self.documento = documento
        self.telefono  = telefono
        self.correo    = correo
        self.contrasena = contrasena

    # -------------------------------------------------------------------------
    # MÉTODOS DE DOMINIO PROPIOS DEL USUARIO
    # Solo operaciones que tienen sentido sobre las credenciales del usuario.
    # -------------------------------------------------------------------------

    def verificar_contrasena(self, contrasena_ingresada: str) -> bool:
        """
        Verifica si la contraseña ingresada coincide con la registrada.
        
        ¿POR QUÉ AQUÍ Y NO EN EL SERVICE?
        La comparación de contraseña es una operación que involucra
        únicamente datos del propio usuario — es parte de su dominio.
        El service llamará a este método y decidirá qué hacer si falla.
        
        Retorna:
            True si la contraseña es correcta, False si no.
        """
        return self.contrasena == contrasena_ingresada

    # -------------------------------------------------------------------------
    # REPRESENTACIÓN
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Representación técnica. Nunca mostramos la contraseña en el repr
        por seguridad básica (no aparece en logs ni en el debugger).
        """
        return (
            f"Usuario(nombre='{self.nombre}', "
            f"documento={self.documento}, "
            f"correo='{self.correo}')"
        )