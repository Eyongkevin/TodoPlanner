from django.db import models

from apps.core.models import AbstractModel
from apps.core.validators import is_hex_color


class Category(AbstractModel):
    # TODO: Set user_id = ...
    color = models.CharField(
        max_length=7, null=True, blank=True, validators=[is_hex_color]
    )  # "#3737A48"

    def __str__(self) -> str:
        return f"{self.name}<{self.color}>"

    class Meta:
        verbose_name_plural = "Categories"
