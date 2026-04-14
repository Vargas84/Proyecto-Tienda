-- =============================================================================
-- schema.sql
-- =============================================================================
-- Define la estructura completa de la base de datos del sistema de inventarios.
-- Este archivo se ejecuta una sola vez al iniciar el sistema por primera vez.
-- "CREATE TABLE IF NOT EXISTS" garantiza que si las tablas ya existen
-- no se borran ni se vuelven a crear — los datos se conservan.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- TABLA: usuarios
-- Almacena los trabajadores registrados en el sistema.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    -- AUTOINCREMENT: SQLite asigna el ID automáticamente, igual que
    -- hacía el contador self._siguiente_id en UsuarioRepository.
    nombre      TEXT    NOT NULL,
    documento   INTEGER NOT NULL UNIQUE,
    -- UNIQUE: garantiza que no haya dos usuarios con el mismo documento.
    -- Antes esto lo verificaba el repository en Python con un bucle for.
    -- Ahora la BD lo garantiza a nivel de almacenamiento.
    telefono    INTEGER NOT NULL UNIQUE,
    correo      TEXT    NOT NULL UNIQUE,
    contrasena  TEXT    NOT NULL
);


-- -----------------------------------------------------------------------------
-- TABLA: productos
-- Almacena el inventario de productos.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL UNIQUE,
    precio          REAL    NOT NULL,
    -- REAL: tipo de SQLite para números con decimales (equivale a float).
    categoria       TEXT    NOT NULL,
    stock           INTEGER NOT NULL DEFAULT 0,
    disponibilidad  TEXT    NOT NULL DEFAULT 'Disponible'
    -- DEFAULT: valor por defecto si no se especifica al insertar.
    -- Equivale a self.disponibilidad = "Disponible" en el modelo Producto.
);


-- -----------------------------------------------------------------------------
-- TABLA: proveedores
-- Almacena los proveedores de las facturas de compra.
-- No tiene UNIQUE en documento porque el mismo proveedor puede aparecer
-- en múltiples facturas y cada vez se guarda como registro independiente.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_empresa  TEXT    NOT NULL,
    documento       INTEGER NOT NULL,
    telefono        INTEGER NOT NULL
);


-- -----------------------------------------------------------------------------
-- TABLA: clientes
-- Almacena los clientes de las facturas de venta.
-- Misma lógica que proveedores — sin UNIQUE en documento.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cliente  TEXT    NOT NULL,
    documento       INTEGER NOT NULL,
    telefono        INTEGER NOT NULL
);


-- -----------------------------------------------------------------------------
-- TABLA: facturas_compra
-- Cabecera de cada factura de compra confirmada.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas_compra (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor_id    INTEGER NOT NULL,
    empleado_nombre TEXT    NOT NULL,
    fecha_hora      TEXT    NOT NULL,
    total           REAL    NOT NULL DEFAULT 0,

    -- FOREIGN KEY: le dice a SQLite que proveedor_id debe existir en
    -- la tabla proveedores. Si se intenta insertar un proveedor_id que
    -- no existe, SQLite lanza un error automáticamente.
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);


-- -----------------------------------------------------------------------------
-- TABLA: detalles_compra
-- Una fila por cada producto dentro de una factura de compra.
-- Relación: muchos detalles → una factura, muchos detalles → un producto.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalles_compra (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id      INTEGER NOT NULL,
    producto_id     INTEGER,
    -- producto_id puede ser NULL si el producto fue eliminado después.
    -- Pero producto_nombre siempre queda guardado como registro histórico.

    producto_nombre TEXT    NOT NULL,
    -- ¿Por qué guardar el nombre si ya tenemos producto_id?
    -- Porque las facturas son registros históricos inmutables.
    -- Si mañana cambias el nombre de "Jabón" a "Jabón líquido",
    -- las facturas antiguas deben seguir mostrando "Jabón".
    -- El nombre en el detalle es una "foto" del momento de la compra.

    cantidad        INTEGER NOT NULL,
    precio_compra   REAL    NOT NULL,
    precio_venta    REAL    NOT NULL,
    subtotal        REAL    NOT NULL,
    es_nuevo        INTEGER NOT NULL DEFAULT 0,
    -- SQLite no tiene tipo BOOLEAN. Usamos INTEGER: 0 = False, 1 = True.
    -- Al leer, convertimos: bool(es_nuevo) en Python.

    FOREIGN KEY (factura_id)  REFERENCES facturas_compra(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);


-- -----------------------------------------------------------------------------
-- TABLA: facturas_venta
-- Cabecera de cada factura de venta confirmada.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facturas_venta (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL,
    empleado_nombre TEXT    NOT NULL,
    fecha           TEXT    NOT NULL,
    total           REAL    NOT NULL DEFAULT 0,

    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


-- -----------------------------------------------------------------------------
-- TABLA: detalles_venta
-- Una fila por cada producto dentro de una factura de venta.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS detalles_venta (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id      INTEGER NOT NULL,
    producto_id     INTEGER,
    -- También puede ser NULL si el producto fue eliminado del inventario.

    producto_nombre TEXT    NOT NULL,
    -- Misma razón que en detalles_compra: registro histórico del nombre.

    cantidad        INTEGER NOT NULL,
    precio_venta    REAL    NOT NULL,
    subtotal        REAL    NOT NULL,

    FOREIGN KEY (factura_id)  REFERENCES facturas_venta(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);


-- -----------------------------------------------------------------------------
-- ÍNDICES
-- Aceleran las búsquedas más frecuentes del sistema.
-- Sin índice, SQLite recorre toda la tabla fila por fila (lento con muchos datos).
-- Con índice, va directo al resultado (como el índice de un libro).
-- -----------------------------------------------------------------------------

-- Búsqueda de usuario por documento (login y validaciones)
CREATE INDEX IF NOT EXISTS idx_usuarios_documento
    ON usuarios(documento);

-- Búsqueda de producto por nombre (al agregar a facturas)
CREATE INDEX IF NOT EXISTS idx_productos_nombre
    ON productos(nombre);

-- Búsqueda de detalles por factura (al cargar una factura completa)
CREATE INDEX IF NOT EXISTS idx_detalles_compra_factura
    ON detalles_compra(factura_id);

CREATE INDEX IF NOT EXISTS idx_detalles_venta_factura
    ON detalles_venta(factura_id);

-- Búsqueda de facturas por fecha (filtro por mes y año)
CREATE INDEX IF NOT EXISTS idx_facturas_compra_fecha
    ON facturas_compra(fecha_hora);

CREATE INDEX IF NOT EXISTS idx_facturas_venta_fecha
    ON facturas_venta(fecha);