from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_manager(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Manager must have is_staff=True.")
        if extra_fields.get("is_superuser") is not False:
            raise ValueError("Manager must have is_superuser=False.")

        return self._create_user(email, password, **extra_fields)


class UserProfile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse_lazy("users:users-profile", kwargs={"pk": self.pk})


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name="Почта", unique=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class ConfirmationCode(models.Model):
    code = models.CharField(max_length=4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="confirmation_code")
