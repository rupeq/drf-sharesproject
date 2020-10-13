from django.contrib import admin
from .models import *


admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(Offer)
admin.site.register(Trade)
admin.site.register(Inventory)

