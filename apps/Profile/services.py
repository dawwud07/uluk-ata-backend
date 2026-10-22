from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.utils import timezone

from apps.Restaurant.models import Cart

from .models import Address, Notification, Order, OrderItem
from .serializers import NotificationSerializer

DELIVERY_FEE = 100
FREE_DELIVERY_MIN_SUBTOTAL = 1500
FAMILY_SET_DISCOUNT_RATE = 0.20
FAMILY_SET_START_HOUR = 12
FAMILY_SET_END_HOUR = 16
VALID_PROMOS = ("", "free_delivery", "family_set")
VALID_FULFILLMENT = ("delivery", "pickup")


def create_order_from_cart(user, data):
    """
    Create an Order from the user's cart: validates promo/address/phone,
    creates Order + OrderItems, clears the cart and sends a notification.

    Returns (order, None) on success or (None, error_dict) on business error.
    """
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return None, {"detail": "Cart is empty."}

    cart_items = list(cart.items.select_related("dish"))
    if not cart_items:
        return None, {"detail": "Cart is empty."}

    fulfillment = data.get("fulfillment", "delivery")
    if fulfillment not in VALID_FULFILLMENT:
        return None, {"fulfillment": "Choose delivery or pickup."}

    address = None
    address_text = ""
    if fulfillment == "delivery":
        address = Address.objects.filter(user=user, id=data.get("address_id")).first()
        if not address:
            return None, {"address_id": "Provide a delivery address."}
        address_text = address.address

    phone = data.get("phone") or str(user.phone or "")
    if not phone:
        return None, {"phone": "Provide a phone number."}

    subtotal = sum(item.dish.price * item.quantity for item in cart_items)

    promo = data.get("promo", "")
    if promo not in VALID_PROMOS:
        return None, {"promo": "Unknown promo."}

    discount = 0
    delivery_fee = DELIVERY_FEE if fulfillment == "delivery" else 0
    if (
        promo == "free_delivery"
        and fulfillment == "delivery"
        and subtotal >= FREE_DELIVERY_MIN_SUBTOTAL
    ):
        delivery_fee = 0
    if promo == "family_set":
        hour = timezone.now().hour
        if hour < FAMILY_SET_START_HOUR or hour >= FAMILY_SET_END_HOUR:
            return None, {"promo": "Family set is active from 12:00 to 16:00."}
        discount = subtotal * FAMILY_SET_DISCOUNT_RATE

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            fulfillment=fulfillment,
            address=address,
            address_snapshot=address_text,
            phone=phone,
            comment=data.get("comment", ""),
            promo=promo,
            subtotal=subtotal,
            discount=discount,
            delivery_fee=delivery_fee,
            total=subtotal - discount + delivery_fee,
        )
        order.number = f"01-{order.id:04d}"
        order.save(update_fields=["number"])

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                name=item.dish.name,
                price=item.dish.price,
                quantity=item.quantity,
            )

        cart.items.all().delete()

        notification = Notification.objects.create(
            user=user,
            order=order,
            title="Order accepted",
            message=f"Order #{order.number} is being prepared.",
        )
        transaction.on_commit(
            lambda: async_to_sync(get_channel_layer().group_send)(
                f"user_{user.pk}_notifications",
                {
                    "type": "notification.created",
                    "data": dict(NotificationSerializer(notification).data),
                },
            )
        )

    return order, None


VALID_STATUSES = [status for status, _ in Order.STATUS_CHOICES]


def set_order_status(order, new_status):
    """Update order status and notify the customer via websocket."""
    if new_status not in VALID_STATUSES:
        raise ValueError("Unknown status.")

    titles = {
        "accepted": "Order accepted",
        "preparing": "Order is being prepared",
        "on_the_way": "Courier is on the way",
        "delivered": "Order delivered",
        "cancelled": "Order cancelled",
    }

    order.status = new_status
    order.save(update_fields=["status", "updated_at"])

    notification = Notification.objects.create(
        user=order.user,
        order=order,
        title=titles[new_status],
        message=f"Order #{order.number}: {titles[new_status].lower()}.",
    )
    transaction.on_commit(
        lambda: async_to_sync(get_channel_layer().group_send)(
            f"user_{order.user_id}_notifications",
            {
                "type": "notification.created",
                "data": dict(NotificationSerializer(notification).data),
            },
        )
    )
    return order
