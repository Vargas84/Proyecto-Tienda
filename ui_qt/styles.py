# =============================================================================
# ui_qt/styles.py
# =============================================================================
# Colores y estilos compartidos entre todas las ventanas.
# Tener los estilos en un solo lugar significa que si quieres cambiar
# un color o fuente, lo cambias aquí y aplica en todo el sistema.
# =============================================================================

# Paleta de colores principal
COLOR_PRIMARY    = "#2563EB"   # azul principal — botones, encabezados
COLOR_PRIMARY_DARK = "#1D4ED8" # azul oscuro — hover de botones
COLOR_DANGER     = "#DC2626"   # rojo — botones de cancelar/eliminar
COLOR_DANGER_DARK = "#B91C1C"  # rojo oscuro — hover
COLOR_SUCCESS    = "#16A34A"   # verde — confirmaciones
COLOR_SUCCESS_DARK = "#15803D" # verde oscuro — hover
COLOR_BG         = "#F8FAFC"   # fondo general
COLOR_SURFACE    = "#FFFFFF"   # fondo de tarjetas y paneles
COLOR_BORDER     = "#E2E8F0"   # bordes
COLOR_TEXT       = "#1E293B"   # texto principal
COLOR_TEXT_MUTED = "#64748B"   # texto secundario
COLOR_SIDEBAR    = "#1E293B"   # fondo del menú lateral
COLOR_SIDEBAR_HOVER = "#334155"  # hover en sidebar
COLOR_SIDEBAR_ACTIVE = "#2563EB" # ítem activo en sidebar


def btn_primary() -> str:
    """Estilo para botones principales (azul)."""
    return f"""
        QPushButton {{
            background-color: {COLOR_PRIMARY};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_PRIMARY_DARK};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_PRIMARY_DARK};
        }}
        QPushButton:disabled {{
            background-color: #94A3B8;
        }}
    """


def btn_danger() -> str:
    """Estilo para botones de acción destructiva (rojo)."""
    return f"""
        QPushButton {{
            background-color: {COLOR_DANGER};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_DANGER_DARK};
        }}
        QPushButton:disabled {{
            background-color: #94A3B8;
        }}
    """


def btn_success() -> str:
    """Estilo para botones de confirmación (verde)."""
    return f"""
        QPushButton {{
            background-color: {COLOR_SUCCESS};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SUCCESS_DARK};
        }}
        QPushButton:disabled {{
            background-color: #94A3B8;
        }}
    """


def btn_secondary() -> str:
    """Estilo para botones secundarios (borde, sin relleno)."""
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {COLOR_PRIMARY};
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 6px;
            padding: 8px 20px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLOR_PRIMARY};
            color: white;
        }}
    """


def input_field() -> str:
    """Estilo para campos de texto (QLineEdit)."""
    return f"""
        QLineEdit {{
            border: 1.5px solid {COLOR_BORDER};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            color: {COLOR_TEXT};
            background-color: {COLOR_SURFACE};
        }}
        QLineEdit:focus {{
            border-color: {COLOR_PRIMARY};
        }}
        QLineEdit:disabled {{
            background-color: #F1F5F9;
            color: {COLOR_TEXT_MUTED};
        }}
    """


def table_style() -> str:
    """Estilo para tablas (QTableWidget)."""
    return f"""
        QTableWidget {{
            border: 1px solid {COLOR_BORDER};
            border-radius: 8px;
            gridline-color: {COLOR_BORDER};
            background-color: {COLOR_SURFACE};
            font-size: 13px;
        }}
        QTableWidget::item {{
            padding: 8px 12px;
            color: {COLOR_TEXT};
        }}
        QTableWidget::item:selected {{
            background-color: #EFF6FF;
            color: {COLOR_PRIMARY};
        }}
        QHeaderView::section {{
            background-color: #F1F5F9;
            color: {COLOR_TEXT};
            font-weight: bold;
            font-size: 12px;
            padding: 8px 12px;
            border: none;
            border-bottom: 1px solid {COLOR_BORDER};
        }}
    """


def label_title() -> str:
    """Estilo para títulos de sección."""
    return f"font-size: 20px; font-weight: bold; color: {COLOR_TEXT};"


def label_subtitle() -> str:
    """Estilo para subtítulos."""
    return f"font-size: 13px; color: {COLOR_TEXT_MUTED};"


def card_style() -> str:
    """Estilo para contenedores tipo tarjeta."""
    return f"""
        QFrame {{
            background-color: {COLOR_SURFACE};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
        }}
    """


def combo_style() -> str:
    """Estilo para QComboBox."""
    return f"""
        QComboBox {{
            border: 1.5px solid {COLOR_BORDER};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            color: {COLOR_TEXT};
            background-color: {COLOR_SURFACE};
        }}
        QComboBox:focus {{
            border-color: {COLOR_PRIMARY};
        }}
        QComboBox::drop-down {{
            border: none;
        }}
    """