from .models import Trade


def trade(boffer, soffer):

    quantity = min(boffer.quantity, soffer.quanity)

    Trade.objects.create(
        buyer_offer=boffer,
        seller_offer=soffer,
        item=boffer.item,
        seller=soffer.user,
        buyer=boffer.user,
        quantity=quantity,
        unit_price=boffer.price,
        trade_type=boffer.order_type,
    )

    buyer_inventory = boffer.user.inventory
    seller_inventory = soffer.user.inventory

    buyer_inventory.money -= boffer.price * quantity
    seller_inventory.money += boffer.price * quantity

    buyer_inventory.quantity += quantity
    seller_inventory.quantity -= quantity
    seller_inventory.reserved_quantity -= quantity

    boffer.quantity -= quantity
    soffer.quanity -= quantity

    if not boffer.quantity:
        boffer.is_active = False
    if not soffer.quanity:
        soffer.is_active = False

    boffer.save()
    soffer.save()

    buyer_inventory.save()
    seller_inventory.save()


