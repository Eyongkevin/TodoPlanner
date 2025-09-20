from uuid import uuid4

from django.db import models


# Create your models here.
class AbstractModel(models.Model):
    public_id = models.UUIDField(unique=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
