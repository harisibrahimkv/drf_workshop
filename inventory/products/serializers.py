from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Category, Stat, Product

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Category.objects.all(),
        source='category'
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category_id', 'category')

    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     category = Category.objects.get(**category_data)
    #     product = Product.objects.create(category=category, **validated_data)
    #     return product


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
