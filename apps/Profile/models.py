from django.db import models
from django.conf import settings


class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
	title = models.CharField(max_length=100, default='Дом')
	address = models.CharField(max_length=255)
	is_default = models.BooleanField(default=False)


	class Meta:
		ordering = ('-is_default', 'title' , 'address')

	def __str__(self):
		return f'{self.title}: {self.address}'


class Order(models.Model):
    STATUS_CHOICES = [
		('pending', 'В обработке' ) ,
		('preparing', 'Готовится'),
		('delivering', 'Доставляется'),
		('completed', 'Завершен'),
		('canceled', 'Отменен'),
	]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, default='pending')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    class Meta:
        ordering = ('-created_at',)



class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	dish = models.ForeignKey('Restaraunt.Dish', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)


class Notification(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications', verbose_name='Заказ')
	food = models.ForeignKey('Restaraunt.Dish', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

