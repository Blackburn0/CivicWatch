from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        CITIZEN = "citizen", "Citizen"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CITIZEN)

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN or self.is_staff
