from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    """Valida que la extensión del archivo sea permitida"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f'Extensión de archivo no permitida. Use: {", ".join(valid_extensions)}'
        )

def validate_image_size(value):
    """Valida que el tamaño del archivo no exceda 20MB"""
    filesize = value.size
    max_size_mb = 20
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if filesize > max_size_bytes:
        raise ValidationError(
            f'El tamaño máximo permitido es {max_size_mb}MB. Tamaño actual: {filesize / (1024 * 1024):.2f}MB'
        )
