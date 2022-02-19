import os
from abc import ABC

from rest_framework import serializers
from connect.models import User, Match
from django.contrib.auth.password_validation import *
from PIL import Image, ImageEnhance


class UserRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name',
                  'user_image', 'gender', 'width', 'longitude']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            user_image=self.validated_data['user_image'],
            gender=self.validated_data['gender'],
            width=self.validated_data['width'],
            longitude=self.validated_data['longitude'],
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
        fields = ['username', 'first_name', 'last_name', 'gender', 'user_image', 'width', 'longitude']


class UserMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = []

    def like(self, *args, **kwargs):
        username = self.initial_data['username']
        user = User.objects.get(username=username)
        print(user)
        if Match.objects.filter(user=self.initial_data['user_like']):
            likes = Match.objects.get(user=self.initial_data['user_like'])
            if self.initial_data['username'] in likes.like.all():
                username = self.initial_data['username']
                user = User.objects.get(username=username)
                likes.like.add(user)
                likes.save()
                return "Match"
            else:
                username = self.initial_data['username']
                user = User.objects.get(username=username)
                likes.like.add(user)
                likes.save()
                print(likes)
                return "Not match"
        else:
            like = Match(
                user=self.initial_data['user_like'],
            )

            print(User.objects.get(username=self.initial_data['username']))
            like.save()

            username = self.initial_data['username']
            user = User.objects.get(username=username)
            like.like.add(user)

            return "Not match"


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
