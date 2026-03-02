def es_letras_y_espacios(texto):
    """Verifica si una cadena contiene solo letras y espacios, y no está vacía."""
    # 1. Elimina espacios en blanco iniciales/finales y verifica si la cadena resultante está vacía
    if not texto.strip():
        return False
        
    # 2. Quita todos los espacios internos para verificar si el resto son solo letras
    texto_sin_espacios = texto.replace(" ", "")
    
    # 3. Retorna True si lo restante son solo letras
    return texto_sin_espacios.isalpha()
