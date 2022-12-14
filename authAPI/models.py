from django.db import models
from django.contrib.auth.models import AbstractUser
from authAPI.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    profilePhoto = models.ImageField("Profile Photo", upload_to='users/', blank=True, null=True)
    # phone = models.CharField(_("Phone"), max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email