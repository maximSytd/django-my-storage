from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from imagekit import models as imagekitmodels
from django_measurement.models import MeasurementField
from imagekit.processors import ResizeToFill, Transpose
from measurement.measures import Weight

from apps.core.models import BaseModel
from .. import querysets

class Product(BaseModel):
    """Represent Product in db."""

    name = models.CharField(
        unique=True,
        max_length=120,
        verbose_name=_("Name")
    )
    description = models.TextField(
        null=True,
        max_length=500,
        verbose_name=_("Description")
    )
    min_quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000000)],
        default=15,
        verbose_name=_("Minimal quantity"),
        null=True,
        blank=True,
    )
    to_notify = models.BooleanField(
        default=False,
        verbose_name=_("To notify"),
        help_text=_(
            (
                "Indicates the need for notification when the quantity on "
                "storage beyond than minimal"
            ),
        ),
    )
    sku = models.CharField(
        max_length=120,
        verbose_name=_("Sku"),
        unique=True,
    )
    weight = MeasurementField(
        measurement=Weight,
        unit_choices=(
            ("kg", _("Kilograms")),
        ),
        verbose_name=_("Weight"),
        help_text=_("Weight of one unit of product in packaging"),
        null=True,
    )
    category = models.ForeignKey(
        to="products.Category",
        related_name="products",
        on_delete=models.RESTRICT,
        verbose_name=_("Category"),
    )
    picture = imagekitmodels.ProcessedImageField(
        verbose_name=_("Picture"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    picture_thumbnail = imagekitmodels.ImageSpecField(
        source="picture",
        processors=[
            ResizeToFill(50, 50),
        ],
    )
    supplier = models.ForeignKey(
        to="products.Supplier",
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name=_("Supplier"),
    )
    objects = querysets.ProductQueryset.as_manager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return f"{self.name}"
