from uuid import uuid4

from django.db import models

from apps.core.helpertest import BaseModelFieldTest
from apps.core.models import AbstractDesModel


class BaseCoreDesModelTest(BaseModelFieldTest):
    model = AbstractDesModel


def test_model_is_abstract():
    assert AbstractDesModel._meta.abstract


class TestFieldDescription(BaseCoreDesModelTest):
    field_name = "description"
    field_type = models.TextField
    null = True
    blank = True
