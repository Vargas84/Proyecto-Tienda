# =============================================================================
# ui/ui_utils.py
# =============================================================================
# Funciones de apoyo reutilizables en todos los menús de la UI.
#
# ANTES: estas funciones de apoyo estaban duplicadas o inline en el
# controlador. Por ejemplo, el patrón de pedir un dato y validarlo
# con while True se repetía decenas de veces.
#
# AHORA: dos funciones genéricas que encapsulan ese patrón.
# Cada menú las usa sin repetir la lógica de bucle y captura.
# =============================================================================

from exceptions.app_exceptions import AppError


def pedir_dato(prompt: str, validator) -> str:
    """
    Pide un dato al usuario en bucle hasta que sea válido.

    Reemplaza el patrón que se repetía ~20 veces en el controlador:

        while True:
            valor = input("Ingrese X: ")
            if not valor:
                print("Error...")
                continue
            if not valor.isdigit():
                print("Error...")
                continue
            break

    AHORA:
        valor = pedir_dato("Ingrese X: ", MiValidator())

    Parámetros:
        prompt (str): texto que ve el usuario al pedir el dato
        validator: cualquier instancia de BaseValidator con método validar()

    Retorna:
        str: el valor ingresado que pasó la validación
    """
    while True:
        valor = input(prompt)
        try:
            validator.validar(valor)
            return valor
        except AppError as e:
            # Mostramos el mensaje de la excepción específica
            # (CampoVacioError, FormatoInvalidoError, etc.)
            print(f"  Error: {e}")


def pedir_opcion(prompt: str, minimo: int, maximo: int) -> int:
    """
    Pide una opción de menú en bucle hasta que sea un entero válido
    dentro del rango [minimo, maximo].

    Reemplaza el patrón:
        try:
            op = int(input("Seleccione: "))
        except ValueError:
            print("ERROR: Ingrese un número válido.")
            continue
        if op < 1 or op > N:
            print("Opción fuera de rango.")
            continue

    Parámetros:
        prompt (str): texto que ve el usuario
        minimo (int): opción mínima válida
        maximo (int): opción máxima válida

    Retorna:
        int: la opción seleccionada ya convertida a entero
    """
    from validators.campo_validator import OpcionMenuValidator
    validator = OpcionMenuValidator(minimo, maximo)
    while True:
        valor = input(prompt)
        try:
            validator.validar(valor)
            return int(valor)
        except AppError as e:
            print(f"  Error: {e}")


def separador(longitud: int = 100) -> None:
    """Imprime una línea separadora. Evita repetir print('-'*100)."""
    print("-" * longitud)


def titulo(texto: str, longitud: int = 100) -> None:
    """Imprime un título centrado con separadores."""
    separador(longitud)
    print(texto.center(longitud))
    separador(longitud)