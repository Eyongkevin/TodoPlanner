from django.db import models

from apps.core.models import AbstractDesModel, AbstractModel


class KeyResult(AbstractModel, AbstractDesModel):
    task = models.ForeignKey("apps_task.Task", on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}(task: {self.task.name}, Complete: {self.complete})"

    class Meta:
        unique_together = ["name", "task"]
