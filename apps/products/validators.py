from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_size(image) -> None:
    limit = 20 * 1024 * 1024
    if image.size > limit:
        raise ValidationError(_("File is too big, max size is 20 megabytes"))
