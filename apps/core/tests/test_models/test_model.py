from uuid import uuid4

import pytest
from django.db import models

from apps.core.helpertest import BaseModelFieldTest
from apps.core.models import AbstractModel


class BaseCoreModelTest(BaseModelFieldTest):
    model = AbstractModel


def test_model_is_abstract():
    assert AbstractModel._meta.abstract


class TestFieldUrl(BaseCoreModelTest):
    field_name = "public_id"
    field_type = models.UUIDField
    unique = True
    editable = False

    def test_has_max_length(self):
        pytest.skip("UUIDField has no max_length attribute")

    def test_default_value(self):
        assert self.field.default == uuid4

    def test_editable(self):
        assert self.field.editable == self.editable


class TestFieldName(BaseCoreModelTest):
    field_name = "name"
    field_type = models.CharField
    max_length = 200


class TestFieldCreatedAt(BaseCoreModelTest):
    field_name = "created_at"
    field_type = models.DateTimeField
    auto_now_add = True
    blank = True


class TestFieldModifiedAt(BaseCoreModelTest):
    field_name = "modified_at"
    field_type = models.DateTimeField
    auto_now = True
    blank = True
