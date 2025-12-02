import pytest
from django.db import models
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.helpertest import BaseModelFieldTest, BaseModelTest
from apps.user.models import UserManager, UserPlanner

fake = Faker()


# Test model isntance
class TestModelUserPlanner(BaseModelTest):
    model = UserPlanner
    instance_kwargs = {"phone_number": fake.phone_number()}

    def test_has_common_attributes(self, instance):
        super().test_has_common_attributes(instance)
        assert hasattr(instance, "username")
        assert hasattr(instance, "first_name")
        assert hasattr(instance, "last_name")
        assert hasattr(instance, "phone_number")
        assert hasattr(instance, "email")
        assert hasattr(instance, "date_of_birth")
        assert hasattr(instance, "country")
        assert hasattr(instance, "profession")
        assert hasattr(instance, "is_active")
        assert hasattr(instance, "is_staff")

        assert hasattr(instance, "USERNAME_FIELD")
        assert hasattr(instance, "REQUIRED_FIELDS")

        assert hasattr(instance, "full_names")

    def test_username_field(self, instance):
        assert instance.USERNAME_FIELD == "username"

    def test_required_field(self, instance):
        assert instance.REQUIRED_FIELDS == ["email", "first_name", "date_of_birth"]

    def test_name_set_to_none(self, instance):
        assert instance.name is None

    def test_full_names(self, instance):
        assert instance.full_names == f"{instance.first_name} {instance.last_name}"

    def test_str_method(self, instance):
        assert str(instance) == f"{instance.username}<{instance.email}>"


# Test model manager
class TestUserPlannerManager:
    def test_objects(self):
        assert isinstance(UserPlanner.objects, UserManager)

    def test_create_superuser(self):
        user = UserPlanner.objects.create_superuser(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            date_of_birth=fake.date_of_birth(),
            password=fake.password(),
        )
        assert isinstance(user, UserPlanner)
        assert user.is_superuser == True
        assert user.is_staff == True


# Test model fields
class BaseUserPlannerFieldTest(BaseModelFieldTest):
    model = UserPlanner


class TestFieldUserPlannerUsername(BaseUserPlannerFieldTest):
    field_name = "username"
    field_type = models.CharField
    unique = True
    db_index = True
    max_length = 50


class TestFieldUserPlannerFirstName(BaseUserPlannerFieldTest):
    field_name = "first_name"
    field_type = models.CharField
    max_length = 255


class TestFieldUserPlannerLastName(BaseUserPlannerFieldTest):
    field_name = "last_name"
    field_type = models.CharField
    null = True
    blank = True
    max_length = 255


class TestFieldUserPlannerPhoneNumber(BaseUserPlannerFieldTest):
    field_name = "phone_number"
    field_type = PhoneNumberField
    unique = True
    region = None

    def test_region_value(self):
        assert self.field.region == self.region

    def test_has_max_length(self):
        pytest.skip("PhoneNumberField has no max_length attribute")


class TestFieldUserPlannerEmail(BaseUserPlannerFieldTest):
    field_name = "email"
    field_type = models.EmailField
    db_index = True
    unique = True
    max_length = 254


class TestFieldUserPlannerDateOfBirth(BaseUserPlannerFieldTest):
    field_name = "date_of_birth"
    field_type = models.DateField


class TestFieldUserPlannerCountry(BaseUserPlannerFieldTest):
    field_name = "country"
    field_type = models.CharField
    max_length = 50
    blank = True
    null = True


class TestFieldUserPlannerProfession(BaseUserPlannerFieldTest):
    field_name = "profession"
    field_type = models.CharField
    null = True
    blank = True
    max_length = 200


class TestFieldUserPlannerIsActive(BaseUserPlannerFieldTest):
    field_name = "is_active"
    field_type = models.BooleanField
    default = True


class TestFieldUserPlannerIsStaff(BaseUserPlannerFieldTest):
    field_name = "is_staff"
    field_type = models.BooleanField
    default = False
