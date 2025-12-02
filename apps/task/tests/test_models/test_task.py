from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.models import AbstractDesModel
from apps.core.validators import is_hex_color
from apps.link.models import Link
from apps.project.models import SubProject
from apps.task.models import Label, Task

fake = Faker()


class BaseTestTask(BaseModelFieldTest):
    model = Task


# TODO: Test model's instance
class TestModelTask(BaseModelTest):
    model = Task
    instance_kwargs = {"sub_project__project__user__phone_number": fake.phone_number()}

    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "sub_project")
        assert hasattr(instance, "priority")
        assert hasattr(instance, "status")
        assert hasattr(instance, "due_date")
        assert hasattr(instance, "color")
        assert hasattr(instance, "labels")
        assert hasattr(instance, "links")
        assert hasattr(instance, "description")
        assert hasattr(instance, "short_des")

    def test_str_method(self, instance):
        assert (
            str(instance)
            == f"{instance.name}(sub-project: {instance.sub_project.name})"
        )

    def test_issubclass_abstract_des_model(self) -> None:
        assert issubclass(self.model, AbstractDesModel)

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("name", "sub_project")

    def test_meta_ordering(self):
        assert self.model._meta.ordering == ("-priority",)

    def test_meta_default_related_name(self):
        assert self.model._meta.default_related_name == "tasks"


# # TODO: Test model's individual fields
class TestFieldPriority(BaseTestTask):
    field_name = "priority"
    field_type = models.PositiveIntegerField
    default = 1


class TestFieldColor(BaseTestTask):
    field_name = "color"
    field_type = models.CharField
    max_length = 7
    null = True
    blank = True

    def test_validators(self):
        assert is_hex_color in self.field.validators


class TestFieldUserStatus(BaseTestTask):
    class Status(models.TextChoices):
        TASK = "task", _("Task")
        DO_TODAY = "do_today", _("Do Today")
        IN_PROGRESS = "in_progress", _("In Progress")
        TESTING = "testing", _("Testing")
        DONE = "done", _("Done")
        STUCK = "stuck", _("STUCK")
        SUSPENDED = "suspended", _("Suspended")

    field_name = "status"
    field_type = models.CharField
    max_length = 50
    choices = Status.choices
    default = Status.TASK

    def test_choices(self):
        assert self.field.choices == self.choices


class TestFieldLink(BaseTestTask):
    field_name = "links"
    field_type = models.ManyToManyField

    def test_has_correct_related_model(self):
        assert self.field.related_model == Link


class TestFieldSubProject(BaseTestTask):
    field_name = "sub_project"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == SubProject

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldLabels(BaseTestTask):
    field_name = "labels"
    field_type = models.ManyToManyField

    def test_has_correct_related_model(self):
        assert self.field.related_model == Label
