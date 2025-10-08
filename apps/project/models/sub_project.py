from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import AbstractDesModel, AbstractModel
from apps.project.utils import START_DATE_END_DATE_CHECK, END_DATE_gte_START_DATE_CHECK


class SubProject(AbstractModel, AbstractDesModel):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey("apps_project.Project", on_delete=models.CASCADE)
    categories = models.ManyToManyField("apps_project.Category")
    links = models.ManyToManyField("apps_link.Link")

    # ? The clean() is useful for admin/forms validation
    # ? To validate in ORM, we need to use either serializer or signal. .add(). .set()
    def clean(self) -> None:
        super().clean()
        if self.categories.count() > 5:
            raise ValidationError("A project cannot have more than 5 categories!")

    def __str__(self) -> str:
        return f"{self.name}(start: {self.start_date}, end: {self.end_date})"

    class Meta:
        unique_together = ("project", "name")
        ordering = ("modified_at",)
        default_related_name = "sub_projects"
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
