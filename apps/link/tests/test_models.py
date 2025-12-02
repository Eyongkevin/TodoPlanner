from django.db import models
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.link.models import Link
from apps.user.models import UserPlanner

fake = Faker()


class BaseTestLink(BaseModelFieldTest):
    model = Link


# TODO: Test model's instance
class TestModelLink(BaseModelTest):
    model = Link
    instance_kwargs = {"user__phone_number": fake.phone_number()}

    def test_has_all_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "user")
        assert hasattr(instance, "url")

    def test_str_method(self, instance):
        assert str(instance) == f"{instance.name}<url: {instance.url}>"

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("user", "url")


# TODO: Test model's individual fields
class TestFieldUser(BaseTestLink):
    field_name = "user"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == UserPlanner

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldUrl(BaseTestLink):
    field_name = "url"
    field_type = models.URLField
    max_length = 500
