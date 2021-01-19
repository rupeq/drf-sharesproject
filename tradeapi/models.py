from django.contrib.auth.models import User
from django.db import models


OrderType = {
    1: "OP_BUY",
    2: "OP_SELL",
}


class StockBase(models.Model):
    code = models.CharField("Code", max_length=8, unique=True)
    name = models.CharField("Name", max_length=128, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Currency(StockBase):
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Item(StockBase):

    cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.TextField("Details", blank=True, null=True, max_length=512)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.cost}{self.currency}"


class WatchList(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user} - {self.item}"


class Price(models.Model):

    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)

    price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(unique=True, blank=True, null=True)


class Offer(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name='offer')

    entry_quantity = models.IntegerField("Requested quantity")
    quantity = models.IntegerField("Current quantity")

    order_type = models.PositiveSmallIntegerField(choices=OrderType.items())
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Offer from {self.user}, item - {self.item}, {self.entry_quantity}"


class Trade(models.Model):

    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )
    buyer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )

    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    buyer_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buyer_trade',
        related_query_name='buyer_trade',
    )
    seller_offer = models.ForeignKey(
        Offer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='seller_trade',
        related_query_name='seller_trade',
    )

    def __str__(self):
        return f"Trade item {self.item}"


class Inventory(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='inventory')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)

    quantity = models.IntegerField()

    class Meta:
        db_table = 'inventory'
        unique_together = ('user', 'item')

    def __str__(self):
        return f"User - {self.user}, Item {self.item} - {self.quantity}"


class Wallet(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="wallet")
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)

    money = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.money}{self.currency}"