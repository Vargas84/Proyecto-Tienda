# =============================================================================
# validators/base_validator.py
# =============================================================================
# ¿POR QUÉ UNA CLASE BASE?
#
# PRINCIPIOS APLICADOS:
#   - Abstracción: definimos un contrato que TODOS los validators deben cumplir
#   - OCP (Open/Closed): puedes crear nuevos validators sin tocar los existentes
#   - Polimorfismo: cualquier validator puede usarse donde se espere un Validator
#
# La clase base define el "contrato": todo validator debe tener un método
# 'validar()'. Si no lo implementa, Python lanzará un error en tiempo de
# ejecución, avisando al programador que olvidó implementarlo.
#
# ANALOGÍA: es como una plantilla de formulario. La empresa define qué campos
# debe tener, y cada departamento llena los suyos con sus propias reglas.
# =============================================================================

from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """
    Clase base abstracta para todos los validators del sistema.
    
    ABC = Abstract Base Class. Es una clase que NO puede instanciarse
    directamente — solo sirve para ser heredada.
    
    Al heredar de ABC y marcar 'validar' con @abstractmethod, Python
    garantiza que cualquier subclase DEBE implementar ese método.
    Si no lo hace, intentar crear un objeto de esa subclase lanzará:
        TypeError: Can't instantiate abstract class X with abstract method validar
    """

    @abstractmethod
    def validar(self, valor: str) -> bool:
        """
        Método que TODA subclase debe implementar.
        
        Recibe el valor a validar (siempre string, porque viene del input())
        y retorna True si es válido, False si no lo es.
        
        Las subclases lanzarán excepciones específicas en vez de retornar False,
        pero la firma base usa bool para mantener compatibilidad.
        
        Parámetros:
            valor (str): el dato ingresado por el usuario
            
        Retorna:
            bool: True si el valor pasa la validación
            
        Lanza:
            AppError (o subclase): si el valor no cumple las reglas
        """
        pass  # Las subclases reemplazan este 'pass' con su propia lógica