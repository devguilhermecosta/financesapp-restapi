from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from typing import Any


class UserManager(BaseUserManager):
    def create_user(self,
                    email: str,
                    first_name: str,
                    last_name: str,
                    password: str | None = None) -> Any:
        if not email:
            raise ValueError('Users must have an email adress')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email: str,
                         first_name: str,
                         last_name: str,
                         password: str | None = None) -> Any:
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def is_staff(self) -> bool:
        return self.is_admin
