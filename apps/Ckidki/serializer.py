from rest_framework import serializers
from .models import Promotion, PromotionCondition


class PromotionConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCondition
        fields = ['id', 'condition_text']


class PromotionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'background_image', 'name', 'tag', 'valid_until', 'is_active']


class PromotionDetailSerializer(serializers.ModelSerializer):
    conditions = PromotionConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = ['id', 'background_image', 'name', 'tag', 'valid_until', 'ob_akcii', 'conditions']
        
        