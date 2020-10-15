from django.contrib.auth import get_user_model
from django.core import exceptions

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
        fields = ('id', 'username', 'email')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'is_active']


class ItemSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Item
        fields = ['code', 'name', 'actual_price', 'currency', 'details', 'logo', 'is_active']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    item = serializers.IntegerField(required=True)

    class Meta:
        model = WatchList
        fields = ['item', 'user']
        extra_kwargs = {'user': {'read_only': True}}


class OfferListSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    user = ListUserSerializer()

    class Meta:
        model = Offer
        fields = '__all__'


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['item', 'quantity', 'entry_quantity', 'order_type', 'transaction_type', 'price']

    def create(self, validated_data):
        user = self.context['request'].user
        item = user.inventory.get(item=validated_data.get('item'))
        order = validated_data.get('order_type')
        entry_quantity = validated_data.get('entry_quantity')

        if order in (1, 2):
            if order == 2:
                if item.quantity - item.reserved_quantity < entry_quantity:
                    return
                item.reserved_quantity += entry_quantity
        else:
            return

        offer = Offer(**validated_data)
        offer.save()
        item.save()
        return offer


class InventoryListSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"
