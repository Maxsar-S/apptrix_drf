from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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
    user_image = models.ImageField(upload_to='users_images')

    width = models.FloatField(default=55.75583)
    longitude = models.FloatField(default=37.6173)


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    like = models.ManyToManyField(User)
