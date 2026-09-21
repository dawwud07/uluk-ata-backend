from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    delivery_time = models.IntegerField()
    delivery_price = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='estate/images/')

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'


class EstablishmentTab(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='tabs')

    class Meta:
        verbose_name = 'Вкладка заведения'
        verbose_name_plural = 'Вкладки заведения'


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tab = models.ForeignKey(EstablishmentTab, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Dish(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='estate/images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    cooking_time = models.IntegerField(default=0)
    ingredients = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class FavoriteDish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное блюдо'
        verbose_name_plural = 'Избранные блюда'
        unique_together = ('user', 'dish')


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ('cart', 'dish')