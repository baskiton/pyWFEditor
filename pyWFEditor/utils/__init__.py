from .logging import Logging

__all__ = (
    'Logging',
    'WC_IMAGES'
)

_x = (
    # display, filter
    ('BMP (*.bmp)', '*.bmp'),
    ('GIF (*.gif)', '*.gif'),
    ('PNG (*.png)', '*.png'),
    ('JPEG (*.jpg)', '*.jpg'),
    ('ICO (*.ico)', '*.ico'),
    ('PNM (*.pnm)', '*.pnm'),
    ('PCX (*.pcx)', '*.pcx'),
    ('TIFF (*.tif)', '*.tif'),
    ('All Files', '*.*'),
)
WC_IMAGES = f'All supported formats|{";".join(i[1] for i in _x[:-1])}|{"|".join("|".join(i) for i in _x)}'
