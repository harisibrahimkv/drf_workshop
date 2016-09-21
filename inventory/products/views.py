from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from .models import Category, Stat

from .serializers import (
    UserSerializer,
    CategorySerializer,
    StatSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
