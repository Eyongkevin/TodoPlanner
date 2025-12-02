from datetime import date

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.models import AbstractModel

# Create your models here.


class UserManager(BaseUserManager):
    # create_user
    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        date_of_birth: date,
        password: str,
        **kwargs,
    ) -> "UserPlanner":
        # Verify the fields above
        if username is None:
            raise TypeError("User must have a username")
        if email is None:
            raise TypeError("User must have an email")
        if first_name is None:
            raise TypeError("User must have a first name")
        if date_of_birth is None:
            raise TypeError("User must have a date of birth")
        if password is None:
            raise TypeError("User must have a password")

        user_planner: UserPlanner = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            date_of_birth=date_of_birth,
            **kwargs,
        )
        user_planner.set_password(password)
        user_planner.save(using=self._db)
        return user_planner

    # create_superuser
    def create_superuser(
        self,
        username: str,
        email: str,
        first_name: str,
        date_of_birth: date,
        password: str,
        **kwargs,
    ) -> "UserPlanner":
        user_planner: UserPlanner = self.create_user(
            username,
            email,
            first_name,
            date_of_birth,
            password,
            **kwargs,
        )

        user_planner.is_superuser = True
        user_planner.is_staff = True
        user_planner.save(using=self._db)
        return user_planner


class UserPlanner(AbstractBaseUser, AbstractModel, PermissionsMixin):
    name = None
    username = models.CharField(db_index=True, unique=True, max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, region=None)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    date_of_birth = models.DateField()
    # ? Check a library that can provide name of countries in a global space
    country = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "date_of_birth"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}<{self.email}>"

    @property
    def full_names(self):
        return f"{self.first_name} {self.last_name}"
