from rest_framework import serializers

from .models import Address, Notification, Order, OrderItem, OrderReview


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("user", "created_at")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "dish", "name", "price", "quantity")


class OrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReview
        fields = ("id", "order", "rating", "comment", "created_at")
        read_only_fields = ("order", "created_at")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    review = OrderReviewSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "number",
            "status",
            "fulfillment",
            "address",
            "address_snapshot",
            "phone",
            "comment",
            "promo",
            "subtotal",
            "discount",
            "delivery_fee",
            "total",
            "items",
            "review",
            "created_at",
            "updated_at",
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("user", "created_at")
