# =============================================================================
# repositories/venta_repository_sql.py
# =============================================================================
# ¿QUÉ HACE ESTE ARCHIVO?
#
# Versión SQLite de VentaRepository. Gestiona tres tablas:
#   - clientes       → datos del cliente de cada factura
#   - facturas_venta → cabecera de cada factura confirmada
#   - detalles_venta → productos dentro de cada factura
#
# Mismo patrón que CompraRepositorySQL pero para ventas.
# =============================================================================

from typing import Optional
from repositories.base_repository import BaseRepository
from repositories.db.conexion import obtener
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.cliente import Cliente
from models.producto import Producto


class VentaRepositorySQL(BaseRepository):
    """
    Implementación SQLite del repositorio de facturas de venta.
    Solo almacena ventas CONFIRMADAS.
    """

    def __init__(self):
        self._con = obtener()

    # -------------------------------------------------------------------------
    # GENERACIÓN DE IDs — manejados por AUTOINCREMENT
    # -------------------------------------------------------------------------

    def generar_id_venta(self) -> int:
        """SQLite asigna el ID con AUTOINCREMENT al hacer INSERT."""
        return -1

    def liberar_id_venta(self) -> None:
        """No necesario con AUTOINCREMENT."""
        pass

    def generar_id_detalle(self) -> int:
        """SQLite asigna el ID con AUTOINCREMENT al hacer INSERT."""
        return -1

    def reiniciar_contador_detalle(self) -> None:
        """No hay contador que reiniciar con SQLite."""
        pass

    # -------------------------------------------------------------------------
    # GUARDAR VENTA CONFIRMADA
    # -------------------------------------------------------------------------

    def guardar(self, venta: Venta) -> None:
        """
        Persiste una factura de venta confirmada en tres tablas:
          1. clientes       → INSERT del cliente
          2. facturas_venta → INSERT de la cabecera
          3. detalles_venta → INSERT de cada producto vendido

        Usa transacción para garantizar atomicidad — los tres INSERTs
        se confirman juntos o ninguno se guarda.
        """
        with self._con:
            assert venta.cliente is not None

            # PASO 1: Insertar el cliente
            cursor_cli = self._con.execute(
                """
                INSERT INTO clientes (nombre_cliente, documento, telefono)
                VALUES (?, ?, ?)
                """,
                (venta.cliente.nombre_cliente,
                 venta.cliente.documento,
                 venta.cliente.telefono)
            )
            id_cliente = cursor_cli.lastrowid

            # PASO 2: Insertar la cabecera de la venta
            cursor_venta = self._con.execute(
                """
                INSERT INTO facturas_venta
                    (cliente_id, empleado_nombre, fecha, total)
                VALUES (?, ?, ?, ?)
                """,
                (id_cliente,
                 venta.cliente.nombre_cliente,  # nombre como texto
                 venta.fecha,
                 venta.total_venta)
            )
            id_venta = cursor_venta.lastrowid
            assert id_venta is not None
            # Asignamos el ID real generado por SQLite al objeto venta
            # para que el sistema pueda referenciarlo correctamente.
            venta.id_venta = id_venta

            # PASO 3: Insertar cada detalle de venta
            for detalle in venta.productos_vendidos:

                producto_id = (detalle.objeto_producto.codigo
                               if detalle.objeto_producto.codigo is not None
                               else None)

                self._con.execute(
                    """
                    INSERT INTO detalles_venta
                        (factura_id, producto_id, producto_nombre,
                         cantidad, precio_venta, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (id_venta,
                     producto_id,
                     detalle.objeto_producto.nombre,  # instantánea histórica
                     detalle.cantidad_vender,
                     detalle.precio_venta,
                     detalle.subtotal)
                )

    # -------------------------------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------------------------------

    def buscar_por_id(self, id_venta: int) -> Optional[Venta]:  # type: ignore[override]
        """
        Carga una venta completa (cabecera + cliente + detalles).
        """
        fila = self._con.execute(
            """
            SELECT fv.*, c.nombre_cliente, c.documento, c.telefono
            FROM   facturas_venta fv
            JOIN   clientes c ON fv.cliente_id = c.id
            WHERE  fv.id = ?
            """,
            (id_venta,)
        ).fetchone()

        if fila is None:
            return None

        return self._fila_a_venta(fila)

    def obtener_todos(self) -> list[Venta]:
        """
        Retorna todas las facturas de venta con sus detalles.
        Las más recientes primero.
        """
        filas = self._con.execute(
            """
            SELECT fv.*, c.nombre_cliente, c.documento, c.telefono
            FROM   facturas_venta fv
            JOIN   clientes c ON fv.cliente_id = c.id
            ORDER  BY fv.id DESC
            """
        ).fetchall()
        return [self._fila_a_venta(f) for f in filas]

    def eliminar(self, id_venta: int) -> bool:
        """Las ventas confirmadas no se eliminan. Retorna False siempre."""
        return False

    def buscar_por_mes_anio(self, mes: int, anio: int) -> list[Venta]:
        """
        Filtra ventas por mes y año.
        La fecha tiene formato 'dd/mm/yyyy hh:mm:ss'.
        SUBSTR extrae mes (posición 4, longitud 2) y año (posición 7, longitud 4).
        """
        filas = self._con.execute(
            """
            SELECT fv.*, c.nombre_cliente, c.documento, c.telefono
            FROM   facturas_venta fv
            JOIN   clientes c ON fv.cliente_id = c.id
            WHERE  CAST(SUBSTR(fv.fecha, 4, 2) AS INTEGER) = ?
            AND    CAST(SUBSTR(fv.fecha, 7, 4) AS INTEGER) = ?
            ORDER  BY fv.id DESC
            """,
            (mes, anio)
        ).fetchall()
        return [self._fila_a_venta(f) for f in filas]

    def total_ventas(self) -> int:
        """Retorna la cantidad de facturas de venta confirmadas."""
        fila = self._con.execute(
            "SELECT COUNT(*) FROM facturas_venta"
        ).fetchone()
        return fila[0]

    def hay_ventas(self) -> bool:
        """Retorna True si hay al menos una venta guardada."""
        return self.total_ventas() > 0

    # -------------------------------------------------------------------------
    # CONVERSIÓN FILAS → OBJETOS
    # -------------------------------------------------------------------------

    def _fila_a_venta(self, fila) -> Venta:
        """
        Reconstruye un objeto Venta completo desde la BD.
        Mismo proceso de hidratación que en CompraRepositorySQL:
          1. Objeto Venta con su ID
          2. Objeto Cliente
          3. Detalles con sus Productos (datos históricos)
        """
        # Reconstruimos el objeto Venta
        venta = Venta(fila["id"])
        venta.fecha           = fila["fecha"]
        venta.total_venta     = fila["total"]
        venta.venta_confirmada = True

        # Reconstruimos el Cliente
        venta.cliente = Cliente(
            nombre_cliente = fila["nombre_cliente"],
            documento      = fila["documento"],
            telefono       = fila["telefono"]
        )

        # Cargamos todos los detalles de esta venta
        detalles = self._con.execute(
            """
            SELECT * FROM detalles_venta
            WHERE  factura_id = ?
            ORDER  BY id
            """,
            (fila["id"],)
        ).fetchall()

        for d in detalles:
            # Reconstruimos el producto con los datos históricos.
            # precio viene de precio_venta del detalle — el precio
            # al momento de la venta, no el actual del inventario.
            producto = Producto(
                codigo    = d["producto_id"],
                nombre    = d["producto_nombre"],
                precio    = d["precio_venta"],
                categoria = "",
                stock     = 0
            )

            # DetalleVenta calcula el subtotal en __init__ como
            # cantidad * objeto_producto.precio, así que pasamos
            # el producto con el precio correcto y luego sobreescribimos
            # el subtotal con el valor histórico de la BD.
            detalle = DetalleVenta(
                id_detalle_ventas = d["id"],
                objeto_producto   = producto,
                cantidad_vender   = d["cantidad"]
            )
            # Sobreescribimos con el subtotal guardado en BD
            # (puede diferir si el precio se editó antes de confirmar)
            detalle.subtotal      = d["subtotal"]
            detalle.precio_venta  = d["precio_venta"]

            venta.productos_vendidos.append(detalle)

        return venta