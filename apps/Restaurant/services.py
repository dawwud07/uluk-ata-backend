from django.shortcuts import get_object_or_404

from .models import Cart, CartItem, Dish


def get_or_create_user_cart(user):
    """Return the user's cart, creating it if it does not exist."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_dish_to_cart(user, dish_id, quantity=1):
    """Add a dish to the user's cart (or increase its quantity). Return the CartItem."""
    cart = get_or_create_user_cart(user)
    dish = get_object_or_404(Dish, id=dish_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()
    return cart_item


def set_cart_item_quantity(user, cart_item_id, quantity):
    """
    Set the quantity of a cart item belonging to the user.

    Returns:
        - CartItem instance if updated successfully.
        - 'deleted' if quantity <= 0 (item removed).
        - None if the cart item does not exist.
    """
    cart_item = CartItem.objects.filter(cart__user=user, id=cart_item_id).first()
    if not cart_item:
        return None

    if quantity <= 0:
        cart_item.delete()
        return "deleted"

    cart_item.quantity = quantity
    cart_item.save()
    return cart_item


def clear_user_cart(user):
    """Remove all items from the user's cart."""
    cart = Cart.objects.filter(user=user).first()
    if cart:
        cart.items.all().delete()
