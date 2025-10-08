from uuid import uuid4

from django.db import models


# Create your models here.
class AbstractModel(models.Model):
    public_id = models.UUIDField(unique=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractDesModel(models.Model):
    description = models.TextField(null=True, blank=True)

    @property
    def short_des(self):
        return f"{self.description[:30] if self.description else ''}..."

    class Meta:
        abstract = True
