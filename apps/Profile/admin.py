from django.contrib import admin

from .models import Address, Notification, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'title', 'address', 'is_default')
	list_filter = ('is_default',)
	search_fields = ('user__email', 'address')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'address', 'total', 'created_at')
	list_filter = ('status', 'user')
	search_fields = ('user__email', 'address__title', 'address__address')
	inlines = (OrderItemInline,)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'food', 'created_at')
	list_filter = ('order__status',)
	search_fields = ('order__user__email', 'food__name')
