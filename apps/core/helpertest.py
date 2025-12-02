from typing import Any

import pytest
from django.db import models
from model_bakery import baker

from apps.core.models import AbstractModel

DATETIME_FIELDS = [models.DateTimeField, models.DateField, models.TimeField]


class BaseModelTest:
    model: models.Model | None = None
    instance_kwargs: dict[str, Any] = {}

    @pytest.fixture
    def instance(self) -> models.Model:
        return baker.make(self.model, **self.instance_kwargs)

    def test_issubclass_model(self):
        assert issubclass(self.model, models.Model)

    def test_issubclass_abstract_model(self):
        assert issubclass(self.model, AbstractModel)

    def test_has_common_attributes(self, instance):
        assert hasattr(instance, "name")
        assert hasattr(instance, "public_id")
        assert hasattr(instance, "created_at")
        assert hasattr(instance, "modified_at")


class BaseModelFieldTest:
    model: models.Model | None = None
    field_name: str | None = None
    field_type: models.Field | None = None

    null: bool = False
    blank: bool = False
    default: Any = models.fields.NOT_PROVIDED
    unique: bool = False
    db_index: bool = False
    auto_now: bool = False
    auto_now_add: bool = False
    primary_key: bool = False
    max_length: int | None = None

    @property
    def field(self):
        return self.model._meta.get_field(self.field_name)

    def test_field_type(self):
        assert isinstance(self.field, self.field_type)

    def test_is_null(self):
        assert self.field.null == self.null

    def test_is_unique(self):
        assert self.field.unique == self.unique

    def test_is_indexed(self):
        assert self.field.db_index == self.db_index

    def test_is_blank(self):
        assert self.field.blank == self.blank

    def test_default_value(self):
        assert self.field.default == self.default

    def test_is_primary_key(self):
        assert self.field.primary_key == self.primary_key

    def test_has_max_length(self):
        assert self.field.max_length == self.max_length

    def test_auto_now(self):
        if self.field.__class__ not in DATETIME_FIELDS:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name} is not a date/time model type"
            )
        assert self.field.auto_now == self.auto_now

    def test_auto_now_add(self):
        if self.field.__class__ not in DATETIME_FIELDS:
            pytest.skip(
                f"{self.model.__name__}->{self.field_name} is not a date/time model type"
            )
        assert self.field.auto_now_add == self.auto_now_add
