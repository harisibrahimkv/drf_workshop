from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Stat, Product

from .serializers import (
    UserSerializer,
    CategorySerializer,
    ProductSerializer,
    StatSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(status=1)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if Stat.objects.exists():
            s = Stat.objects.get()
            s.category_count += 1
            s.save()
        else:
            Stat.objects.create(category_count=1)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        s = Stat.objects.get()
        s.category_count -= 1
        # This should never happen. The idea here is to just demonstrate overriding destroy().
        if s.category_count < 1:
            s.category_count = 0
        s.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category_id = self.kwargs.get('categories_pk', None)
        product_id = self.kwargs.get('pk', None)

        if category_id:
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(category=category)

        if product_id:
            queryset = queryset.filter(id=product_id)

        return queryset


class StatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
