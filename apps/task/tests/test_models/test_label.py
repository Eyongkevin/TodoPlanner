from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.validators import is_hex_color
from apps.task.models import Label
from apps.user.models import UserPlanner

fake = Faker()


class BaseTestLabel(BaseModelFieldTest):
    model = Label


# TODO: Test model's instance
class TestModelLabel(BaseModelTest):
    model = Label
    instance_kwargs = {"user__phone_number": fake.phone_number()}

    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "user")
        assert hasattr(instance, "color")

    def test_str_method(self, instance):
        assert str(instance) == instance.name

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("user", "name")


# TODO: Test model's individual fields
class TestFieldUser(BaseTestLabel):
    field_name = "user"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == UserPlanner

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldColor(BaseTestLabel):
    field_name = "color"
    field_type = models.CharField
    max_length = 7
    null = True
    blank = True

    def test_validators(self):
        assert is_hex_color in self.field.validators
