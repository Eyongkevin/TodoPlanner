from datetime import date

import pytest
from django.db import models
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.models import AbstractDesModel
from apps.link.models import Link
from apps.project.models import Project
from apps.user.models import UserPlanner

fake = Faker()


# TODO: Test model's instance
class TestModelProject(BaseModelTest):
    model = Project
    instance_kwargs = {"user__phone_number": fake.phone_number()}

    def test_has_common_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "user")
        assert hasattr(instance, "start_date")
        assert hasattr(instance, "end_date")
        assert hasattr(instance, "links")
        assert hasattr(instance, "description")
        assert hasattr(instance, "short_des")

    def test_short_des(self, instance):
        assert (
            instance.short_des
            == f'{instance.description[:30] if instance.description else ""}...'
        )

    def test_str_method(self, instance):
        assert (
            str(instance)
            == f"{instance.name}(start: {instance.start_date}, end: {instance.end_date})"
        )

    def test_issubclass_abstract_des_model(self) -> None:
        assert issubclass(self.model, AbstractDesModel)

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("user", "name")

    def test_meta_ordering(self):
        assert self.model._meta.ordering == ("modified_at",)

    def test_constraint_start_and_end_dates_both_null(self, instance):
        instance.end_date = None
        instance.start_date = None
        instance.save()

    @pytest.mark.xfail
    def test_constraint_start_date_is_null_but_end_date_is_not_null(self, instance):
        instance.start_date = None
        instance.end_date = date.today()
        instance.save()

    def test_constraint_start_date_is_not_null_but_end_date_is_null(self, instance):
        instance.start_date = date.today()
        instance.end_date = None
        instance.save()

    def test_constraint_start_and_end_dates_both_not_null(self, instance):
        instance.start_date = date.today()
        instance.end_date = date.today()
        instance.save()

    @pytest.mark.xfail
    def test_constraint_start_date_is_lesser_than_end_date(self, instance):
        instance.start_date = date.fromisoformat("2021-02-01")
        instance.end_date = date.fromisoformat("2021-01-01")
        instance.save()


# TODO: Test model's individual fields


class BaseProjectFieldTest(BaseModelFieldTest):
    model = Project


class TestFieldUser(BaseProjectFieldTest):
    field_name = "user"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == UserPlanner

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldStartDate(BaseProjectFieldTest):
    field_name = "start_date"
    field_type = models.DateField
    null = True
    blank = True


class TestFieldEndDate(BaseProjectFieldTest):
    field_name = "end_date"
    field_type = models.DateField
    null = True
    blank = True


class TestFieldLink(BaseProjectFieldTest):
    field_name = "links"
    field_type = models.ManyToManyField

    def test_has_correct_related_model(self):
        assert self.field.related_model == Link

    def test_has_correct_related_name(self):
        assert self.field.related_query_name() == "projects"
