from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.validators import is_hex_color
from apps.task.models import SubTask, Task

fake = Faker()


class BaseTestSubTask(BaseModelFieldTest):
    model = SubTask


# TODO: Test model's instance
class TestModelSubTask(BaseModelTest):
    model = SubTask
    instance_kwargs = {
        "task__sub_project__project__user__phone_number": fake.phone_number()
    }

    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "task")
        assert hasattr(instance, "done")
        assert hasattr(instance, "color")

    def test_str_method(self, instance):
        assert str(instance) == f"{instance.name}(task: {instance.task.name})"

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("name", "task")


# # TODO: Test model's individual fields
class TestFieldPriority(BaseTestSubTask):
    field_name = "done"
    field_type = models.BooleanField
    default = False


class TestFieldColor(BaseTestSubTask):
    field_name = "color"
    field_type = models.CharField
    max_length = 7
    null = True
    blank = True

    def test_validators(self):
        assert is_hex_color in self.field.validators


class TestFieldTask(BaseTestSubTask):
    field_name = "task"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == Task

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE
