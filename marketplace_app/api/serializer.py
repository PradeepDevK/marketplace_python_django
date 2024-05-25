from rest_framework import serializers
from marketplace_app.models import (
    Category,
    Product
)


"""
Product Serializer
"""
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = '__all__'


"""
Category Serializer
"""
class CategorySerializer(serializers.ModelSerializer):
    productlist = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'