from django.db import models
from django.conf import settings


class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
	title = models.CharField(max_length=100, default='Дом')
	address = models.CharField(max_length=255)
	entrance = models.CharField(max_length=50, blank=True)
	floor = models.CharField(max_length=50, blank=True)
	apartment = models.CharField(max_length=50, blank=True)
	comment = models.TextField(blank=True)
	is_default = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering = ('-is_default', '-created_at')

	def __str__(self):
		return f'{self.title}: {self.address}'


class Order(models.Model):
	STATUS_CHOICES = [
		('accepted', 'Принят'),
		('preparing', 'Preparing'),
		('on_the_way', 'Курьер в пути'),
		('delivered', 'Доставлен'),
		('cancelled', 'Отменён'),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
	status = models.CharField(max_length=20, default='accepted')
	fulfillment = models.CharField(max_length=20, default='delivery')
	address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
	address_snapshot = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=50)
	comment = models.TextField(blank=True)
	subtotal = models.DecimalField(max_digits=10, decimal_places=2)
	delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ('-created_at',)



class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	dish = models.ForeignKey('Restaraunt.Dish', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)


class Notification(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
	title = models.CharField(max_length=255)
	message = models.TextField(blank=True)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

