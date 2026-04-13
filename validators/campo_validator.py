# =============================================================================
# validators/campo_validator.py
# =============================================================================
# ¿POR QUÉ ESTE ARCHIVO?
#
# En el controlador original, el mismo código de validación aparecía
# repetido para usuarios, proveedores y clientes:
#
#   # Para usuario:
#   elif not documento.isdigit(): print('Ingrese únicamente números')
#   elif len(documento) >= 8 and len(documento) <= 10: ...
#
#   # Para proveedor (idéntico):
#   elif not documento_proveedor.isdigit(): print('Ingrese únicamente números')
#   elif len(documento_proveedor) >= 8 and len(documento_proveedor) <= 10: ...
#
#   # Para cliente (idéntico de nuevo):
#   elif not documento_cliente.isdigit(): print('Ingrese únicamente números')
#   ...
#
# Ahora esa lógica vive en UN solo lugar. Si cambia la regla (ej: documentos
# de 6 a 12 dígitos), solo se modifica aquí y aplica en todo el sistema.
#
# PRINCIPIOS APLICADOS:
#   - SRP: cada clase valida un solo tipo de campo
#   - DRY (Don't Repeat Yourself): eliminamos la duplicación
#   - Polimorfismo: todas heredan de BaseValidator, son intercambiables
# =============================================================================

import re  # módulo de expresiones regulares de Python (para validar correo)
from validators.base_validator import BaseValidator
from exceptions.app_exceptions import (
    CampoVacioError,
    FormatoInvalidoError,
    LongitudInvalidaError,
    ValorFueraDeRangoError,
    ContrasenaInseguraError,
    CorreoInvalidoError,
)


# =============================================================================
# VALIDATOR DE NOMBRE
# Reglas: no vacío, solo letras y espacios
# Usado en: registro de usuario, proveedor, cliente, nombre de producto
# =============================================================================

class NombreValidator(BaseValidator):
    """
    Valida que un nombre contenga solo letras y espacios y no esté vacío.
    Reemplaza todas las llamadas a es_letras_y_espacios() + check de vacío
    que aparecían dispersas por el controlador.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si el valor está vacío.
        Lanza FormatoInvalidoError si contiene números o caracteres especiales.
        Retorna True si pasa ambas validaciones.
        """
        # Primero limpiamos espacios al inicio y al final (strip)
        valor = valor.strip()

        # Validación 1: campo vacío
        if not valor:
            raise CampoVacioError("El nombre no puede estar vacío")

        # Validación 2: solo letras y espacios
        # all() retorna True si TODOS los caracteres cumplen la condición
        # c.isalpha() es True para letras, c == ' ' es True para espacios
        if not all(c.isalpha() or c == ' ' for c in valor):
            raise FormatoInvalidoError(
                "El nombre solo puede contener letras y espacios"
            )

        return True


# =============================================================================
# VALIDATOR DE DOCUMENTO
# Reglas: no vacío, solo dígitos, entre 8 y 10 caracteres
# Usado en: registro de usuario, proveedor, cliente
# =============================================================================

class DocumentoValidator(BaseValidator):
    """
    Valida que un documento sea numérico y tenga entre 8 y 10 dígitos.
    Antes este bloque se repetía 3 veces en el controlador (usuario,
    proveedor, cliente) con variables de distinto nombre pero lógica idéntica.
    """

    # Estas constantes definen las reglas del dominio en un solo lugar.
    # Si el negocio cambia los límites, se modifica aquí y aplica en todo.
    LONGITUD_MIN = 8
    LONGITUD_MAX = 10

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si contiene letras o caracteres especiales.
        Lanza LongitudInvalidaError si no está entre 8 y 10 dígitos.
        Retorna True si pasa todas las validaciones.
        """
        valor = valor.strip()

        # Validación 1: campo vacío
        if not valor:
            raise CampoVacioError(
                "El documento es obligatorio para el registro"
            )

        # Validación 2: solo dígitos
        # isdigit() retorna True si TODOS los caracteres son números (0-9)
        if not valor.isdigit():
            raise FormatoInvalidoError(
                "El documento debe contener únicamente números, "
                "sin espacios ni puntos"
            )

        # Validación 3: longitud correcta
        if not (self.LONGITUD_MIN <= len(valor) <= self.LONGITUD_MAX):
            raise LongitudInvalidaError(
                f"El documento debe tener entre {self.LONGITUD_MIN} "
                f"y {self.LONGITUD_MAX} dígitos"
            )

        return True


# =============================================================================
# VALIDATOR DE TELÉFONO
# Reglas: no vacío, solo dígitos, exactamente 10 caracteres
# Usado en: registro de usuario, proveedor, cliente
# =============================================================================

class TelefonoValidator(BaseValidator):
    """
    Valida que un teléfono colombiano sea numérico y tenga exactamente 10 dígitos.
    Antes se repetía 3 veces en el controlador con el mismo bloque while/elif.
    """

    LONGITUD_EXACTA = 10

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si contiene letras.
        Lanza LongitudInvalidaError si no tiene exactamente 10 dígitos.
        Retorna True si pasa todas las validaciones.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError(
                "El teléfono es obligatorio para el registro"
            )

        if not valor.isdigit():
            raise FormatoInvalidoError(
                "El teléfono debe contener únicamente números, "
                "sin espacios ni guiones"
            )

        if len(valor) != self.LONGITUD_EXACTA:
            raise LongitudInvalidaError(
                f"El teléfono debe tener exactamente {self.LONGITUD_EXACTA} dígitos"
            )

        return True


# =============================================================================
# VALIDATOR DE CORREO
# Reglas: no vacío, debe contener '@' y '.com'
# Usado en: registro de usuario
# =============================================================================

class CorreoValidator(BaseValidator):
    """
    Valida que un correo electrónico tenga formato básico aceptable.
    Mantiene las mismas reglas del controlador original (@ y .com),
    sin agregar complejidad extra que el negocio no pidió.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza CorreoInvalidoError si no contiene '@' y '.com'.
        Retorna True si pasa las validaciones.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError(
                "El correo es obligatorio para el registro"
            )

        # Verificación básica: el controlador original solo chequeaba @ y .com
        # Mantenemos la misma regla para no cambiar el comportamiento del sistema
        if "@" not in valor or ".com" not in valor:
            raise CorreoInvalidoError(
                'El correo debe contener "@" y ".com". '
                'Ejemplo: usuario@gmail.com'
            )

        return True


# =============================================================================
# VALIDATOR DE CONTRASEÑA
# Reglas: mínimo 8 caracteres, al menos una mayúscula, al menos un número
# Usado en: registro de usuario
# =============================================================================

class ContrasenaValidator(BaseValidator):
    """
    Valida que la contraseña cumpla los criterios de seguridad definidos
    en el controlador original.
    """

    LONGITUD_MIN = 8

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza ContrasenaInseguraError si no cumple los criterios de seguridad.
        Retorna True si la contraseña es segura.
        
        NOTA: para contraseña NO hacemos strip() porque los espacios
        al inicio/final son caracteres válidos y parte de la seguridad.
        """
        if not valor:
            raise CampoVacioError("La contraseña no puede estar vacía")

        # Verificamos cada criterio por separado para dar mensajes precisos
        errores = []

        if len(valor) < self.LONGITUD_MIN:
            errores.append(f"al menos {self.LONGITUD_MIN} caracteres")

        # any() recorre los caracteres y retorna True si alguno es mayúscula
        if not any(c.isupper() for c in valor):
            errores.append("al menos una letra mayúscula")

        # any() recorre los caracteres y retorna True si alguno es dígito
        if not any(c.isdigit() for c in valor):
            errores.append("al menos un número")

        # Si hay errores, los unimos en un mensaje claro
        if errores:
            raise ContrasenaInseguraError(
                "Contraseña insegura. Debe tener: " + ", ".join(errores)
            )

        return True


# =============================================================================
# VALIDATOR DE PRECIO
# Reglas: no vacío, numérico, mayor a 0
# Usado en: agregar producto, registrar compra (precio_compra, precio_venta)
# =============================================================================

class PrecioValidator(BaseValidator):
    """
    Valida que un precio sea un número positivo mayor a cero.
    Antes este bloque se repetía para precio de producto, precio de compra
    y precio de venta con el mismo while/if/continue.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si no es numérico.
        Lanza ValorFueraDeRangoError si es <= 0.
        Retorna True si el precio es válido.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError("El precio es obligatorio")

        # isdigit() en el string antes de convertir, para evitar crash en float()
        if not valor.isdigit():
            raise FormatoInvalidoError(
                "El precio debe ser un número sin espacios, puntos ni comas"
            )

        # Convertimos a float solo después de validar que es numérico
        precio = float(valor)

        if precio <= 0:
            raise ValorFueraDeRangoError("El precio debe ser mayor a 0")

        return True


# =============================================================================
# VALIDATOR DE STOCK
# Reglas: no vacío, entero, mayor a 0
# Usado en: agregar producto
# =============================================================================

class StockValidator(BaseValidator):
    """
    Valida que el stock sea un número entero positivo mayor a cero.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si no es entero.
        Lanza ValorFueraDeRangoError si es <= 0.
        Retorna True si el stock es válido.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError("El stock es obligatorio")

        # isnumeric() acepta solo enteros positivos (no puntos ni comas)
        if not valor.isnumeric():
            raise FormatoInvalidoError(
                "El stock debe ser un número entero sin decimales"
            )

        stock = int(valor)

        if stock <= 0:
            raise ValorFueraDeRangoError("El stock debe ser mayor a 0")

        return True


# =============================================================================
# VALIDATOR DE CANTIDAD (para compras y ventas)
# Reglas: no vacío, entero, mayor a 0
# Nota: es igual a StockValidator pero semánticamente distinto.
#       Una "cantidad" a comprar/vender no es lo mismo que "stock" del producto.
# =============================================================================

class CantidadValidator(BaseValidator):
    """
    Valida la cantidad de unidades a comprar o vender en una factura.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si no es entero.
        Lanza ValorFueraDeRangoError si es <= 0.
        Retorna True si la cantidad es válida.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError("La cantidad es obligatoria")

        if not valor.isnumeric():
            raise FormatoInvalidoError(
                "La cantidad debe ser un número entero"
            )

        cantidad = int(valor)

        if cantidad <= 0:
            raise ValorFueraDeRangoError("La cantidad debe ser mayor a 0")

        return True


# =============================================================================
# VALIDATOR DE OPCIÓN DE MENÚ
# Reglas: debe ser un entero dentro de un rango dado
# Usado en: todos los menús del sistema
# =============================================================================

class OpcionMenuValidator(BaseValidator):
    """
    Valida que una opción de menú sea un entero dentro del rango permitido.
    
    Este validator es especial: recibe el rango como parámetro en __init__
    porque el rango varía según el menú (1-3, 1-4, 1-6, etc.).
    
    Ejemplo de uso:
        validator = OpcionMenuValidator(1, 4)
        validator.validar("2")   # → True
        validator.validar("5")   # → lanza ValorFueraDeRangoError
        validator.validar("abc") # → lanza FormatoInvalidoError
    """

    def __init__(self, minimo: int, maximo: int):
        """
        Parámetros:
            minimo (int): opción mínima válida del menú (normalmente 1)
            maximo (int): opción máxima válida del menú
        """
        # Guardamos el rango como atributos de instancia
        # para usarlos en validar()
        self.minimo = minimo
        self.maximo = maximo

    def validar(self, valor: str) -> bool:
        """
        Lanza FormatoInvalidoError si no es un entero.
        Lanza ValorFueraDeRangoError si está fuera del rango minimo-maximo.
        Retorna True si la opción es válida.
        """
        valor = valor.strip()

        # Intentamos convertir a entero — si falla, no es una opción válida
        try:
            opcion = int(valor)
        except ValueError:
            raise FormatoInvalidoError(
                "Ingrese un número válido"
            )

        if not (self.minimo <= opcion <= self.maximo):
            raise ValorFueraDeRangoError(
                f"Opción fuera de rango. Ingrese un número entre "
                f"{self.minimo} y {self.maximo}"
            )

        return True


# =============================================================================
# VALIDATOR DE CATEGORÍA
# Reglas: no vacío, solo letras y espacios (igual que nombre)
# Usado en: agregar producto
# =============================================================================

class CategoriaValidator(BaseValidator):
    """
    Valida que una categoría de producto contenga solo letras y espacios.
    Reutiliza la misma lógica de NombreValidator pero con mensajes distintos,
    porque semánticamente una categoría es distinta de un nombre de persona.
    """

    def validar(self, valor: str) -> bool:
        """
        Lanza CampoVacioError si está vacío.
        Lanza FormatoInvalidoError si contiene números o caracteres especiales.
        Retorna True si es válida.
        """
        valor = valor.strip()

        if not valor:
            raise CampoVacioError("La categoría es obligatoria")

        if not all(c.isalpha() or c == ' ' for c in valor):
            raise FormatoInvalidoError(
                "La categoría solo puede contener letras y espacios"
            )

        return True