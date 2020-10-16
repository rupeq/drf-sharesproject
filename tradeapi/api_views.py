from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from tradeapi.models import Item, WatchList, Offer, Inventory, Trade, Currency
from tradeapi.serializers import (ItemSerializer,
                                  CurrencySerializer,
                                  FavoriteCreateSerializer,
                                  InventoryListSerializer,
                                  OfferCreateSerializer,
                                  OfferListSerializer,
                                  OfferUpdateSerializer,
                                  TradeSerializer)


class CurrencyView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemsView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FavoriteList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    default_serializer_class = FavoriteCreateSerializer

    permission_classes = (IsAuthenticated, )

    def get_serializer(self, *args, **kwargs):
        return self.default_serializer_class

    def perform_create(self, serializer):
        item = get_object_or_404(Item, id=self.request.data.get('item'))
        serializer.save(item=item, user=self.request.user)
        return serializer.data

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class InventoryList(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = InventoryListSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Inventory.objects.filter(user=user)


class OfferList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    default_serializer_class = OfferListSerializer

    permission_classes = (IsAuthenticated, )

    serializer_classes_by_action = {
        "list": OfferListSerializer,
        "create": OfferCreateSerializer,
        "update": OfferUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Offer.objects.filter(is_active=True)


class TradeList(mixins.ListModelMixin,
                viewsets.GenericViewSet):

    serializer_class = TradeSerializer
    queryset = Trade.objects.all()

    # filter_backends = (DjangoFilterBackend, )
    # filterset_fields = ('seller', 'buyer')

    permission_classes = (IsAuthenticated, )
