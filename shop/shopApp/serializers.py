from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'title', 'slug', 'images', 'description', 'specifications', 'price')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CustomerProductRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProductRelation
        fields = ('customer', 'product', 'in_bookmarks')
