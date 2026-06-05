from django.core.exceptions import ValidationError
import os
from PIL import Image
from io import BytesIO

def validate_image_extension(value):
    """Valida que la extensión del archivo sea permitida"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f'Extensión de archivo no permitida. Use: {", ".join(valid_extensions)}'
        )

def validate_image_size(value):
    """Valida que el tamaño del archivo no exceda 5MB"""
    filesize = value.size
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if filesize > max_size_bytes:
        raise ValidationError(
            f'El tamaño máximo permitido es {max_size_mb}MB. Tamaño actual: {filesize / (1024 * 1024):.2f}MB'
        )

def validate_image_dimensions(value):
    """Valida que las dimensiones de la imagen sean apropiadas"""
    try:
        img = Image.open(value)
        width, height = img.size
        
        # Dimensiones máximas: 2000x2000 píxeles
        max_width = 2000
        max_height = 2000
        # Dimensiones mínimas: 300x300 píxeles
        min_width = 300
        min_height = 300
        
        if width > max_width or height > max_height:
            raise ValidationError(
                f'Las dimensiones máximas permitidas son {max_width}x{max_height} píxeles. '
                f'Dimensiones actuales: {width}x{height} píxeles'
            )
        
        if width < min_width or height < min_height:
            raise ValidationError(
                f'Las dimensiones mínimas requeridas son {min_width}x{min_height} píxeles. '
                f'Dimensiones actuales: {width}x{height} píxeles'
            )
    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        raise ValidationError('Formato de imagen inválido o corrupto')
