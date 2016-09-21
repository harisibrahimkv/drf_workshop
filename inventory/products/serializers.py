from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Category, Stat

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
