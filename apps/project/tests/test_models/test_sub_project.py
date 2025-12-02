from datetime import date

import pytest
from django.db import models
from faker import Faker

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.core.models import AbstractDesModel
from apps.link.models import Link
from apps.project.models import Category, Project, SubProject

fake = Faker()


class BaseTestSubProject(BaseModelFieldTest):
    model = SubProject


# TODO: Test model's instance
class TestModelSubProject(BaseModelTest):
    model = SubProject
    instance_kwargs = {"project__user__phone_number": fake.phone_number()}

    def test_has_all_attributes(self, instance):
        # TODO: Test that all attributes and methods are present
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "project")
        assert hasattr(instance, "categories")
        assert hasattr(instance, "start_date")
        assert hasattr(instance, "end_date")
        assert hasattr(instance, "links")
        assert hasattr(instance, "description")
        assert hasattr(instance, "short_des")

    def test_str_method(self, instance):
        assert (
            str(instance)
            == f"{instance.name}(start: {instance.start_date}, end: {instance.end_date})"
        )

    def test_issubclass_abstract_des_model(self) -> None:
        assert issubclass(self.model, AbstractDesModel)

    # TODO: Test meta properties and constraints
    def test_meta_unique_together(self):
        assert self.model._meta.unique_together[0] == ("project", "name")

    def test_meta_ordering(self):
        assert self.model._meta.ordering == ("modified_at",)

    def test_meta_default_related_name(self):
        assert self.model._meta.default_related_name == "sub_projects"

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


class TestFieldProject(BaseTestSubProject):
    field_name = "project"
    field_type = models.ForeignKey
    db_index = True

    def test_has_correct_related_model(self):
        assert self.field.related_model == Project

    def test_on_delete(self):
        assert self.field.remote_field.on_delete == models.CASCADE


class TestFieldSubProject(BaseTestSubProject):
    field_name = "categories"
    field_type = models.ManyToManyField

    def test_has_correct_related_model(self):
        assert self.field.related_model == Category


class TestFieldStartDate(BaseTestSubProject):
    field_name = "start_date"
    field_type = models.DateField
    null = True
    blank = True


class TestFieldEndDate(BaseTestSubProject):
    field_name = "end_date"
    field_type = models.DateField
    null = True
    blank = True


class TestFieldLink(BaseTestSubProject):
    field_name = "links"
    field_type = models.ManyToManyField

    def test_has_correct_related_model(self):
        assert self.field.related_model == Link

    def test_has_correct_related_name(self):
        assert self.field.related_query_name() == "sub_projects"
