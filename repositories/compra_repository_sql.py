# =============================================================================
# repositories/compra_repository_sql.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Versión SQLite de CompraRepository. Gestiona tres tablas relacionadas:
#   - proveedores     → datos del proveedor de cada factura
#   - facturas_compra → cabecera de cada factura confirmada
#   - detalles_compra → productos dentro de cada factura
#
# LA DIFERENCIA CON LA VERSIÓN EN MEMORIA:
# Antes, guardar una factura era un simple .append() a una lista.
# Ahora son tres INSERTs coordinados: primero el proveedor, luego
# la factura (que necesita el ID del proveedor), luego cada detalle
# (que necesita el ID de la factura).
#
# TRANSACCIONES:
# Los tres INSERTs deben ejecutarse como una unidad atómica.
# Si falla el tercero, los dos primeros deben deshacerse.
# SQLite maneja esto con BEGIN / COMMIT / ROLLBACK.
# Usamos "with self._con:" que activa ese mecanismo automáticamente.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from repositories.db.conexion import obtener
from models.compra import Compra
from models.detalle_compra import DetalleCompra
from models.proveedor import Proveedor
from models.producto import Producto


class CompraRepositorySQL(BaseRepository):
    """
    Implementación SQLite del repositorio de facturas de compra.
    Solo almacena facturas CONFIRMADAS.
    """

    def __init__(self):
        self._con = obtener()

    # -------------------------------------------------------------------------
    # GENERACIÓN DE IDs — con SQLite AUTOINCREMENT los maneja la BD
    # -------------------------------------------------------------------------

    def generar_id_factura(self) -> int:
        """
        Con SQLite el ID lo genera AUTOINCREMENT al hacer el INSERT.
        Retornamos -1 como placeholder — el ID real se obtiene con lastrowid.
        El service llama a este método pero con SQL no lo usamos realmente.
        """
        return -1

    def liberar_id_factura(self) -> None:
        """
        Con SQLite no es necesario liberar IDs — AUTOINCREMENT se salta
        los IDs cancelados y eso es comportamiento normal.
        Se mantiene para compatibilidad con el service.
        """
        pass

    def generar_id_detalle(self) -> int:
        """Mismo caso — AUTOINCREMENT maneja los IDs de detalles."""
        return -1

    def reiniciar_contador_detalle(self) -> None:
        """Con SQLite no hay contador que reiniciar."""
        pass

    # -------------------------------------------------------------------------
    # GUARDAR FACTURA CONFIRMADA (operación más importante)
    # -------------------------------------------------------------------------

    def guardar(self, compra: Compra) -> None:
        """
        Persiste una factura de compra confirmada en tres tablas:
          1. proveedores       → INSERT del proveedor
          2. facturas_compra   → INSERT de la cabecera
          3. detalles_compra   → INSERT de cada producto

        Usa una transacción para garantizar que los tres pasos
        se completan juntos o ninguno se guarda.

        TRANSACCIÓN:
            "with self._con:" activa BEGIN automáticamente al entrar
            y COMMIT al salir sin errores, o ROLLBACK si hay excepción.
            Así no quedan datos a medias en la BD.
        """
        with self._con:
            assert compra.proveedor is not None

            # PASO 1: Insertar el proveedor
            # Cada factura guarda su propio registro de proveedor.
            # Así el historial es inmutable aunque el proveedor cambie.
            cursor_prov = self._con.execute(
                """
                INSERT INTO proveedores (nombre_empresa, documento, telefono)
                VALUES (?, ?, ?)
                """,
                (compra.proveedor.nombre_empresa,
                 compra.proveedor.documento,
                 compra.proveedor.telefono)
            )
            id_proveedor = cursor_prov.lastrowid
            # lastrowid: el ID que SQLite asignó al proveedor recién insertado.
            # Lo necesitamos para la clave foránea de facturas_compra.

            # PASO 2: Insertar la cabecera de la factura
            cursor_factura = self._con.execute(
                """
                INSERT INTO facturas_compra
                    (proveedor_id, empleado_nombre, fecha_hora, total)
                VALUES (?, ?, ?, ?)
                """,
                (id_proveedor,
                 compra.proveedor.nombre_empresa,  # guardamos el nombre como texto
                 compra.fecha_hora,
                 compra.total_factura)
            )
            id_factura = cursor_factura.lastrowid
            assert id_factura is not None
            # Este ID lo necesitamos para los detalles (clave foránea).
            # También lo guardamos en el objeto para que el sistema
            # pueda referenciarlo después.
            compra.id_factura = id_factura

            # PASO 3: Insertar cada detalle (producto de la factura)
            for detalle in compra.lista_detalles:

                # producto_id puede ser None si el producto fue borrado,
                # pero siempre guardamos el nombre como registro histórico.
                producto_id = (detalle.producto.codigo
                               if detalle.producto.codigo is not None
                               else None)

                self._con.execute(
                    """
                    INSERT INTO detalles_compra
                        (factura_id, producto_id, producto_nombre,
                         cantidad, precio_compra, precio_venta,
                         subtotal, es_nuevo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (id_factura,
                     producto_id,
                     detalle.producto.nombre,   # instantánea histórica
                     detalle.cantidad_compra,
                     detalle.precio_compra,
                     detalle.precio_venta_nuevo,
                     detalle.subtotal,
                     1 if detalle.es_nuevo else 0)
                     # SQLite no tiene BOOLEAN — guardamos 1/0
                )

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def buscar_por_id(self, id_factura: int) -> Optional[Compra]:  # type: ignore[override]
        """
        Carga una factura completa (cabecera + proveedor + detalles)
        desde la BD y la reconstruye como objeto Compra.
        """
        # Primero cargamos la cabecera con JOIN al proveedor
        fila = self._con.execute(
            """
            SELECT fc.*, p.nombre_empresa, p.documento, p.telefono
            FROM   facturas_compra fc
            JOIN   proveedores p ON fc.proveedor_id = p.id
            WHERE  fc.id = ?
            """,
            (id_factura,)
        ).fetchone()

        if fila is None:
            return None

        return self._fila_a_compra(fila)

    def obtener_todos(self) -> list[Compra]:
        """
        Retorna todas las facturas de compra con sus detalles.
        Ordena por ID descendente — las más recientes primero.
        """
        filas = self._con.execute(
            """
            SELECT fc.*, p.nombre_empresa, p.documento, p.telefono
            FROM   facturas_compra fc
            JOIN   proveedores p ON fc.proveedor_id = p.id
            ORDER  BY fc.id DESC
            """
        ).fetchall()
        return [self._fila_a_compra(f) for f in filas]

    def eliminar(self, id_factura: int) -> bool:
        """Las facturas confirmadas no se eliminan. Retorna False siempre."""
        return False

    def buscar_por_mes_anio(self, mes: int, anio: int) -> list[Compra]:
        """
        Filtra facturas por mes y año usando SUBSTR en SQL.

        La fecha tiene formato 'dd/mm/yyyy hh:mm:ss'.
        SUBSTR(fecha_hora, 4, 2) extrae los caracteres 4 y 5 → el mes.
        SUBSTR(fecha_hora, 7, 4) extrae los caracteres 7 al 10 → el año.
        Convertimos a INTEGER para comparar con los parámetros.

        Esto reemplaza el filtrado manual que estaba en el repository
        en memoria y también en el controlador original.
        """
        filas = self._con.execute(
            """
            SELECT fc.*, p.nombre_empresa, p.documento, p.telefono
            FROM   facturas_compra fc
            JOIN   proveedores p ON fc.proveedor_id = p.id
            WHERE  CAST(SUBSTR(fc.fecha_hora, 4, 2) AS INTEGER) = ?
            AND    CAST(SUBSTR(fc.fecha_hora, 7, 4) AS INTEGER) = ?
            ORDER  BY fc.id DESC
            """,
            (mes, anio)
        ).fetchall()
        return [self._fila_a_compra(f) for f in filas]

    def total_facturas(self) -> int:
        """Retorna la cantidad de facturas de compra confirmadas."""
        fila = self._con.execute(
            "SELECT COUNT(*) FROM facturas_compra"
        ).fetchone()
        return fila[0]

    def hay_facturas(self) -> bool:
        """Retorna True si hay al menos una factura guardada."""
        return self.total_facturas() > 0

    # -------------------------------------------------------------------------
    # CONVERSIÓN FILAS → OBJETOS
    # -------------------------------------------------------------------------

    def _fila_a_compra(self, fila) -> Compra:
        """
        Reconstruye un objeto Compra completo desde la BD:
          1. Crea el objeto Compra con su ID
          2. Crea el objeto Proveedor
          3. Carga los detalles desde detalles_compra
          4. Reconstruye cada DetalleCompra con su Producto

        Este proceso se llama "hidratación" — tomamos datos planos
        de la BD y los convertimos en objetos del dominio con relaciones.
        """
        # Reconstruimos el objeto Compra
        compra = Compra(fila["id"])
        compra.fecha_hora       = fila["fecha_hora"]
        compra.total_factura    = fila["total"]
        compra.factura_confirmada = True

        # Reconstruimos el Proveedor
        compra.proveedor = Proveedor(
            nombre_empresa = fila["nombre_empresa"],
            documento      = fila["documento"],
            telefono       = fila["telefono"]
        )

        # Cargamos todos los detalles de esta factura
        detalles = self._con.execute(
            """
            SELECT * FROM detalles_compra
            WHERE  factura_id = ?
            ORDER  BY id
            """,
            (fila["id"],)
        ).fetchall()

        for d in detalles:
            # Reconstruimos el producto con los datos históricos del detalle.
            # Usamos producto_nombre (el nombre guardado al momento de la compra)
            # no el nombre actual del producto en inventario — puede haber cambiado.
            producto = Producto(
                codigo    = d["producto_id"],
                nombre    = d["producto_nombre"],
                precio    = d["precio_venta"],
                categoria = "",   # no se guarda en el detalle, no es relevante
                stock     = 0     # ídem
            )

            detalle = DetalleCompra(
                id_detalle        = d["id"],
                producto          = producto,
                cantidad_compra   = d["cantidad"],
                precio_compra     = d["precio_compra"],
                precio_venta_nuevo = d["precio_venta"],
                es_nuevo          = bool(d["es_nuevo"])
                # bool(1) = True, bool(0) = False
            )
            detalle.subtotal = d["subtotal"]
            compra.lista_detalles.append(detalle)

        return compra