from django.contrib import admin
from .models import (
	Institution,EstablishmentTab,Category,Dish,FavoriteDish,Cart,CartItem,
)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'delivery_time', 'delivery_price')
    search_fields = ('name', 'description')

@admin.register(EstablishmentTab)
class EstablishmentTabAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institution')
    list_filter = ('institution',)
    search_fields = ('name', 'description')
    
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'cooking_time')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'ingredients')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tab')
    list_filter = ('tab',)
    search_fields = ('name', 'description')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'dish', 'quantity')
    list_filter = ('cart', 'dish')
    
@admin.register(FavoriteDish)
class FavoriteDishAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dish', 'created_at')
    list_filter = ('user', 'dish')


