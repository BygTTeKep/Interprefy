from rest_framework import serializers
from django.utils.text import slugify
from .models import (
    CUser,
    Categories,
    Products,
    Posts,
)

class CUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    UserSlug = serializers.SlugField()
    MiddleName = serializers.CharField()
    TelephoneNumber = serializers.CharField()
    is_intermediary = serializers.BooleanField()
    Email = serializers.EmailField()
    Description = serializers.CharField()
    FromCountry = serializers.CharField()
    ImageIntermediares = serializers.ImageField(use_url=False)
    def create(self, validated_data):
        validated_data.UserSlug = slugify(self.username)
        return CUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.UserSlug = slugify(validated_data.get('UserSlug', instance.UserSlug))
        instance.MiddleName = validated_data.get('MiddleName', instance.MiddleName)
        instance.is_intermediary = validated_data.get('is_intermediary', instance.is_intermediary)
        instance.Email = validated_data.get('Email', instance.Email)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.FromCountry = validated_data.get('FromCountry', instance.FromCountry)
        instance.ImageIntermediares = validated_data.get('ImageIntermediares', instance.ImageIntermediares)
        instance.save()
        return instance
    
class CategorySerializer(serializers.Serializer):
    CategoryName = serializers.CharField(max_length=50)
    
    def create(self, validate_data):
        return Categories.objects.create(**validate_data)
    
    def update(self, instance, validate_data):
        instance.CategoryName = validate_data.get('CategoryName', instance.CategoryName)
        instance.save()
        return instance
    def delete(self, validate_data):
        return Categories.objects.delete(**validate_data)
    
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'