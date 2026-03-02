class Proveedor:
    def __init__(self, nombre_empresa, documento, telefono):
        # Datos de la entidad legal
        self.nombre_empresa = nombre_empresa  # Ej: "Distribuidora Global S.A."
        self.documento = documento            # Ej: NIT o RUT
        self.telefono = telefono              # Ej: +57 300...
        

    def __str__(self):
        return f" {self.nombre_empresa} | Doc: {self.documento} | Tel: {self.telefono}"