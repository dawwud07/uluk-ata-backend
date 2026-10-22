from django.contrib import admin

from .models import Address, Notification, Order, OrderItem, OrderReview


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "address", "is_default")
    list_filter = ("is_default",)
    search_fields = ("user__email", "address")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "user",
        "status",
        "promo",
        "address",
        "total",
        "created_at",
    )
    list_filter = ("status", "user")
    search_fields = ("user__email", "number", "address__title", "address__address")
    inlines = (OrderItemInline,)


@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__email", "comment")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order", "title", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__email", "title", "message")
