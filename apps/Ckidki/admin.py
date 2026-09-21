from django.contrib import admin
from .models import Promotion, PromotionCondition

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tag', 'valid_until', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'tag', 'ob_akcii')

@admin.register(PromotionCondition)
class PromotionConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'promotion', 'condition_text')
    list_filter = ('promotion',)
    search_fields = ('condition_text',)
