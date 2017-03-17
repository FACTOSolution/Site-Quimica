import os, magic
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


def validate_article_type(upload):
    # Whitelist for the article types
    ARTICLE_TYPES = [
        'application/pdf',
    ]
    file_type = magic.from_buffer(upload.file.read(1024), mime=True)
    if file_type not in ARTICLE_TYPES:
        raise ValidationError('Envie apenas arquivos PFD.')
