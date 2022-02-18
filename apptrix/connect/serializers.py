import os

from rest_framework import serializers
from connect.models import User
from django.contrib.auth.password_validation import *
from PIL import Image, ImageEnhance


class UserRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'user_image', 'gender']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_image=self.validated_data['user_image'],
            gender=self.validated_data['gender'],
        )
        password = self.validated_data['password']
        try:
            validate_password(password)
        except ValidationError:
            raise serializers.ValidationError({password: "Password is too common"})
        user.set_password(password)

        user.save()

        watermark = os.path.join(settings.MEDIA_ROOT, 'watermark.png')
        image = os.path.join(settings.MEDIA_ROOT, str(user.user_image))
        print(image)
        wm_user_image = add_watermark(image, watermark)
        wm_user_image.save(image)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'user_image']


def add_watermark(image, watermark, opacity=1):
    image = Image.open(image)
    watermark = Image.open(watermark)

    assert 0 <= opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    x = (watermark.size[0])
    y = (watermark.size[1])
    layer.paste(watermark, (x, y))
    return Image.composite(layer, image, layer)