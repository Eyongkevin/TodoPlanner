from django.db import models

from apps.core.models import AbstractModel

# Create your models here.


class Link(AbstractModel):
    # TODO: Set user_id = ...
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.name}<url: {self.url}>"

    # TODO: Set unique_together = (user_id, url)
