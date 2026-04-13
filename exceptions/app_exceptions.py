# =============================================================================
# exceptions/app_exceptions.py
# =============================================================================
# ¿POR QUÉ ESTE ARCHIVO?
# Antes, cuando algo salía mal, el código hacía print("Error: ...") directo
# en el medio del menú. Eso mezcla la UI con la lógica de errores.
#
# Con excepciones propias del dominio, cualquier capa del sistema puede
# LANZAR un error con nombre claro, y la UI simplemente lo CAPTURA y
# muestra el mensaje. Cada capa hace solo su trabajo.
#
# PRINCIPIO APLICADO: SRP — cada clase tiene una sola razón de existir.
#
# CÓMO SE USA (ejemplo):
#   # En un validator o service:
#   raise DocumentoInvalidoError("El documento debe tener entre 8 y 10 dígitos")
#
#   # En la UI (menú):
#   try:
#       validar_documento(doc)
#   except DocumentoInvalidoError as e:
#       print(f"Error: {e}")
# =============================================================================


# -----------------------------------------------------------------------------
# CLASE BASE — todas las excepciones del sistema heredan de esta
# -----------------------------------------------------------------------------
class AppError(Exception):#Heredan Exception--->todos los errores de python vienen de qui 
    """
    Excepción base del sistema de inventarios.
    
    Heredar de Exception es el estándar de Python para crear errores propios.
    Al tener una clase base común, puedes capturar TODOS los errores del sistema
    con un solo 'except AppError' si lo necesitas.
    """
    def __init__(self, mensaje: str):#recibe le mensaje que queremos mostrar
        # Llamamos al __init__ de Exception para que Python
        # registre el mensaje correctamente (visible en traceback y en str(e))
        super().__init__(mensaje)#llama la constructor de Exception y esto hace que python
        #reconozca bien el error
        self.mensaje = mensaje  # guardamos el mensaje como atributo propio también

    def __str__(self):
        # Controla cómo se imprime el error: print(e) o str(e)
        return self.mensaje


# =============================================================================
# EXCEPCIONES DE VALIDACIÓN DE CAMPOS
# Se lanzan cuando un dato ingresado no cumple las reglas del dominio.
# =============================================================================

class CampoVacioError(AppError):
    """
    Se lanza cuando un campo obligatorio llega vacío.
    
    Ejemplo de uso:
        if not nombre:
            raise CampoVacioError("El nombre no puede estar vacío")
    """
    pass  # 'pass' porque toda la lógica viene de AppError


class FormatoInvalidoError(AppError):
    """
    Se lanza cuando un campo tiene caracteres que no corresponden.
    Por ejemplo: un nombre con números, o un precio con letras.
    
    Ejemplo de uso:
        if not nombre.isalpha():
            raise FormatoInvalidoError("El nombre solo puede contener letras")
    """
    pass


class LongitudInvalidaError(AppError):
    """
    Se lanza cuando un campo no cumple la longitud requerida.
    Por ejemplo: documento con menos de 8 dígitos o más de 10.
    
    Ejemplo de uso:
        if not (8 <= len(doc) <= 10):
            raise LongitudInvalidaError("El documento debe tener entre 8 y 10 dígitos")
    """
    pass


class ValorFueraDeRangoError(AppError):
    """
    Se lanza cuando un número no está dentro del rango permitido.
    Por ejemplo: precio <= 0, stock negativo, opción de menú fuera de rango.
    
    Ejemplo de uso:
        if precio <= 0:
            raise ValorFueraDeRangoError("El precio debe ser mayor a 0")
    """
    pass


class ContrasenaInseguraError(AppError):
    """
    Se lanza cuando la contraseña no cumple los criterios de seguridad:
    mínimo 8 caracteres, al menos una mayúscula y al menos un número.
    
    Ejemplo de uso:
        if len(contrasena) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
    """
    pass


class CorreoInvalidoError(AppError):
    """
    Se lanza cuando el correo no tiene el formato mínimo esperado (@, .com).
    
    Ejemplo de uso:
        if "@" not in correo:
            raise CorreoInvalidoError("El correo debe contener '@'")
    """
    pass


# =============================================================================
# EXCEPCIONES DE NEGOCIO — USUARIOS
# Se lanzan cuando una regla del negocio es violada al registrar usuarios.
# =============================================================================

class UsuarioYaExisteError(AppError):
    """
    Se lanza cuando se intenta registrar un usuario con un documento,
    teléfono o correo que ya está en uso.
    
    Ejemplo de uso:
        if documento_duplicado:
            raise UsuarioYaExisteError(f"El documento {doc} ya está registrado")
    """
    pass


class UsuarioNoEncontradoError(AppError):
    """
    Se lanza cuando se busca un usuario por documento y no existe.
    
    Ejemplo de uso:
        if usuario is None:
            raise UsuarioNoEncontradoError("No existe un usuario con ese documento")
    """
    pass


class CredencialesInvalidasError(AppError):
    """
    Se lanza cuando la contraseña ingresada no coincide con la registrada.
    Usamos un mensaje genérico a propósito (no revelar si el error es en
    el documento o en la contraseña — buena práctica de seguridad).
    
    Ejemplo de uso:
        if usuario.contrasena != contrasena_ingresada:
            raise CredencialesInvalidasError("Documento o contraseña incorrectos")
    """
    pass


# =============================================================================
# EXCEPCIONES DE NEGOCIO — PRODUCTOS
# =============================================================================

class ProductoYaExisteError(AppError):
    """
    Se lanza cuando se intenta agregar un producto con un nombre
    que ya está registrado en el inventario.
    """
    pass


class ProductoNoEncontradoError(AppError):
    """
    Se lanza cuando se busca un producto por ID o nombre y no se encuentra.
    """
    pass


class StockInsuficienteError(AppError):
    """
    Se lanza cuando se intenta vender más unidades de las disponibles en stock.
    
    Ejemplo de uso:
        if cantidad_vender > producto.stock:
            raise StockInsuficienteError(
                f"Solo hay {producto.stock} unidades de {producto.nombre}"
            )
    """
    pass


class ProductoNoDisponibleError(AppError):
    """
    Se lanza cuando se intenta agregar a una venta un producto
    marcado como 'No Disponible'.
    """
    pass


# =============================================================================
# EXCEPCIONES DE NEGOCIO — FACTURAS (COMPRAS Y VENTAS)
# =============================================================================

class FacturaVaciaError(AppError):
    """
    Se lanza cuando se intenta confirmar una factura sin productos.
    
    Ejemplo de uso:
        if len(factura.lista_detalles) == 0:
            raise FacturaVaciaError("No puedes confirmar una compra sin productos")
    """
    pass


class ProductoDuplicadoEnFacturaError(AppError):
    """
    Se lanza cuando se intenta agregar a una factura un producto
    que ya fue agregado en esa misma factura.
    """
    pass


class FacturaYaConfirmadaError(AppError):
    """
    Se lanza cuando se intenta editar o cancelar una factura
    que ya fue confirmada (y por lo tanto no puede modificarse).
    """
    pass