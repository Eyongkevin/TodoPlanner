from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractDesModel, AbstractModel
from apps.core.validators import is_hex_color


class Task(AbstractModel, AbstractDesModel):
    # ?: Would a finite state machine work better to manage mood?
    class Status(models.TextChoices):
        TASK = "task", _("Task")
        DO_TODAY = "do_today", _("Do Today")
        IN_PROGRESS = "in_progress", _("In Progress")
        TESTING = "testing", _("Testing")
        DONE = "done", _("Done")
        STUCK = "stuck", _("STUCK")
        SUSPENDED = "suspended", _("Suspended")

    sub_project = models.ForeignKey("apps_project.SubProject", on_delete=models.CASCADE)
    # The lesser, the higher the priority
    priority = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.TASK
    )
    due_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    color = models.CharField(
        max_length=7, null=True, blank=True, validators=(is_hex_color,)
    )
    labels = models.ManyToManyField("apps_task.Label")
    links = models.ManyToManyField("apps_link.Link")

    def __str__(self) -> str:
        return f"{self.name}(sub-project: {self.sub_project.name})"

    class Meta:
        # TODO: Build a vscode extension that will auto-complete when typing a meta property
        # by auto-completing the property name and suggesting base on the class attributes above.
        unique_together = ["name", "sub_project"]
        ordering = ("-priority",)
        default_related_name = "tasks"  # '%(app_label)s_%(model_name)s_tasks'
