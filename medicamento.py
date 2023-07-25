class Medicamento:
    def __init__(self, sku, nombre, laboratorio, principio_activo, accion_terapeutica, presentacion, dosis, bioequivalente, disponibilidad, precio, proveedor_nombre, proveedor_rut):
        self.sku = sku
        self.nombre = nombre
        self.laboratorio = laboratorio
        self.principio_activo = principio_activo
        self.accion_terapeutica = accion_terapeutica
        self.presentacion = presentacion
        self.dosis = dosis
        self.bioequivalente = bioequivalente
        self.disponibilidad = disponibilidad
        self.precio = precio
        self.proveedor_nombre = proveedor_nombre
        self.proveedor_rut = proveedor_rut

    def toDBCollection(self):
        return {
            "sku": self.sku,
            "nombre": self.nombre,
            "laboratorio": self.laboratorio,
            "principio_activo": self.principio_activo,
            "accion_terapeutica": self.accion_terapeutica,
            "presentacion": self.presentacion,
            "dosis": self.dosis,
            "bioequivalente": self.bioequivalente,
            "disponibilidad": self.disponibilidad,
            "precio": self.precio,
            "proveedor": [
                {"nombre": self.proveedor_nombre},
                {"rut": self.proveedor_rut}
            ]
        }

        
class Proveedor:
    def __init__(self, nombre, rut, ):
        self.nombre = nombre
        self.rut = rut
    

    def toDBCollection(self):
        return {
            "nombre": self.nombre,
            "rut": self.rut,
           
        }



