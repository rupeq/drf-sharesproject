from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .api_views import ItemsView, FavoriteList, InventoryList, OfferList


router = DefaultRouter()
router.register(r'items', ItemsView, basename="shares")
router.register(r'watchlist', FavoriteList, basename="favorite")
router.register(r'offers', OfferList, basename="offers")
router.register(r'inventory', InventoryList, basename='inventory')

urlpatterns = [
    path(r'', include(router.urls, )),
]


