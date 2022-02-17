from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISES = (
        (MALE, 'M'),
        (FEMALE, 'W'),
    )

    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER_CHOISES, max_length=1, verbose_name='gender')
    user_image = models.ImageField(upload_to='users_images', blank=True)
