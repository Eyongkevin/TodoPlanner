from django.db import models

from apps.core.models import AbstractModel
from apps.core.validators import is_hex_color


class SubTask(AbstractModel):
    task = models.ForeignKey("apps_task.Task", on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7, null=True, blank=True, validators=(is_hex_color,)
    )

    def __str__(self) -> str:
        return f"{self.name}(task: {self.task.name})"

    class Meta:
        unique_together = ["name", "task"]
