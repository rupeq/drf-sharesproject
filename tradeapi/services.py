from django.shortcuts import get_object_or_404

from .models import Inventory, Wallet, Trade, Offer


def trade(buyer_offer: Offer, seller_offer: Offer):
    seller = seller_offer.user
    buyer = buyer_offer.user
    item = buyer_offer.item

    quantity = 10

    if seller_offer.entry_quantity < buyer_offer.entry_quantity:
        quantity = seller_offer.entry_quantity
    elif seller_offer.entry_quantity >= buyer_offer.entry_quantity:
        quantity = buyer_offer.entry_quantity

    Trade.objects.create(
        item=seller_offer.item,
        seller=seller,
        buyer=buyer,
        quantity=quantity,
        unit_price=buyer_offer.price,
        description="Trade",
        buyer_offer=buyer_offer,
        seller_offer=seller_offer
    )

    seller_offer.entry_quantity -= quantity
    buyer_offer.entry_quantity -= quantity

    buyer_inventory = get_object_or_404(Inventory, user=buyer, item=item)
    seller_inventory = get_object_or_404(Inventory, user=seller, item=item)

    seller_wallet = get_object_or_404(Wallet, user=seller)
    buyer_wallet = get_object_or_404(Wallet, user=buyer)

    seller_wallet.money += seller_offer.price * quantity
    buyer_wallet.money -= seller_offer.price * quantity

    buyer_inventory.quantity += quantity
    seller_inventory.quantity -= quantity

    buyer_offer.save(update_fields=('entry_quantity', ))
    seller_offer.save(update_fields=('entry_quantity',))

    if buyer_offer.entry_quantity == 0:
        buyer_offer.is_active = False
        buyer_offer.save(update_fields=('is_active', ))

    if seller_offer.entry_quantity == 0:
        seller_offer.is_active = False
        seller_offer.save(update_fields=('is_active',))

    seller_wallet.save(update_fields=('money', ))
    buyer_wallet.save(update_fields=('money', ))
    buyer_inventory.save(update_fields=('quantity', ))
    seller_inventory.save(update_fields=('quantity', ))
