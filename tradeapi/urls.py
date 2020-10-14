from django.urls import path

from rest_framework.routers import DefaultRouter

from .api_views import ItemsView, FavoriteList


router = DefaultRouter()
router.register(r'items', ItemsView, basename="shares")
router.register(r'watchlist', FavoriteList, basename="favorite")

urlpatterns = [
]

urlpatterns += router.urls
