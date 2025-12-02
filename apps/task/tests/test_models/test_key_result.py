import pytest
from django.db import models
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.models import AbstractDesModel
from apps.task.models import KeyResult, Task

fake = Faker()


class BaseTestKeyResult(BaseModelFieldTest):
    model = KeyResult


# TODO: Test model's instance
class TestModelKeyResult(BaseModelTest):
    model = KeyResult
    instance_kwargs = {
        "task__sub_project__project__user__phone_number": fake.phone_number()
    }

    # @pytest.mark.django_db
    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "task")
        assert hasattr(instance, "complete")
        assert hasattr(instance, "description")
        assert hasattr(instance, "short_des")

    def test_str_method(self, instance):
        assert (
            str(instance)
            == f"{instance.name}(task: {instance.task.name}, Complete: {instance.complete})"
        )

    def test_short_des(self, instance):
        assert (
            instance.short_des
            == f'{instance.description[:30] if instance.description else ""}...'
        )

    def test_issubclass_abstract_des_model(self) -> None:
        assert issubclass(self.model, AbstractDesModel)

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("name", "task")


# TODO: Test model's individual fields
class TestFieldTask(BaseTestKeyResult):
    field_name = "task"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == Task

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldComplete(BaseTestKeyResult):
    field_name = "complete"
    field_type = models.BooleanField
    default = False
