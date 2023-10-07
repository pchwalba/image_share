import os

from django.core.exceptions import ValidationError


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = {".jpg", ".png"}
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File. Please select jpg or png file.")

    if value.size > 10 * 1024 * 1024:
        raise ValidationError('File size exceeds the limit. Max 10MB is allowed.')


def validate_expiration_time(value):
    if 30000 < value < 300:
        raise ValidationError('Expiration time should be between 300 and 30000 sec')