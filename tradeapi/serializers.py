from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import *


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            password = validated_data.pop('password')
            user_obj = User(**validated_data)
            user_obj.set_password(password)
            user_obj.save()
            return user_obj


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'is_active']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['code', 'name', 'actual_price', 'currency', 'details', 'logo', 'is_active']