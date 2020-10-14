from django.urls import path

from .api_views import CurrencyTable, CurrencyUpdateDelete


urlpatterns = [
    path('currency/', CurrencyTable.as_view()),
    path('currency/<int:id>/', CurrencyUpdateDelete.as_view()),
]
