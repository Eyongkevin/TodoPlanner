from django.db import models

from apps.core.models import AbstractDesModel, AbstractModel
from apps.project.utils import START_DATE_END_DATE_CHECK, END_DATE_gte_START_DATE_CHECK


class Project(AbstractModel, AbstractDesModel):
    # TODO: set user_id = ...
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    links = models.ManyToManyField("apps_link.Link", related_name="projects")

    def __str__(self) -> str:
        return f"{self.name}(start: {self.start_date}, end: {self.end_date})"

    class Meta:
        # TODO: Set unique_together = (user_id, name)
        ordering = ("modified_at",)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_end_date_check",
                check=START_DATE_END_DATE_CHECK,
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_end_date_start_date_check",
                check=END_DATE_gte_START_DATE_CHECK,
            ),
        ]
