import os
import uuid

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def avatar_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{uuid.uuid4()}{extension}"

    return os.path.join("uploads/avatar/image", filename)


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        UNKNOWN = "unknown"
        MALE = "male"
        FEMALE = "female"
        GENDERLESS = "genderless"

    username = None
    email = models.EmailField(_("email address"), unique=True)
    sex = models.CharField(
        max_length=10, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN
    )
    subscribe = models.ManyToManyField(
        to="self", blank=True, related_name="followers", symmetrical=False
    )
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_image_file_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
