from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile

def validate_image_size(file: ImageFile):
    BYTES_IN_KB = 1024
    max_image_size = 50
    
    if file.size > max_image_size * BYTES_IN_KB:
        raise ValidationError(f'File cannot be bigger than {max_image_size}KB!')