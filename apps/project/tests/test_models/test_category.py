from django.db import models
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.validators import is_hex_color
from apps.project.models import Category
from apps.user.models import UserPlanner

fake = Faker()


class BaseTestProject(BaseModelFieldTest):
    model = Category


# TODO: Test model's instance
class TestModelProject(BaseModelTest):
    model = Category
    instance_kwargs = {"user__phone_number": fake.phone_number()}

    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "color")

    def test_str_method(self, instance):
        assert str(instance) == f"{instance.name}<{instance.color}>"

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("user", "name")

    def test_meta_verbose_name_plural(self):
        assert self.model._meta.verbose_name_plural == "Categories"


# TODO: Test model's individual fields
class TestFieldUser(BaseTestProject):
    field_name = "user"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == UserPlanner

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldColor(BaseTestProject):
    field_name = "color"
    field_type = models.CharField
    max_length = 7
    null = True
    blank = True

    def test_validators(self):
        assert is_hex_color in self.field.validators
