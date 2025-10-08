from django.db import models

from apps.core.models import AbstractModel
from apps.core.validators import is_hex_color


class Label(AbstractModel):
    # TODO: user_id =
    color = models.CharField(
        max_length=7, null=True, blank=True, validators=(is_hex_color,)
    )

    def __str__(self) -> str:
        return self.name

    # TODO: Add unique_together (user_id, name)
