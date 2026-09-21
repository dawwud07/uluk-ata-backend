from rest_framework import serializers
from .models import Institution, EstablishmentTab, Category, Dish, FavoriteDish, Cart, CartItem


class EstablishmentTabSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentTab
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'image', 'category']


class DishDetailSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'image', 'cooking_time', 'ingredients', 'is_favorite']

    def get_is_favorite(self, dish):
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            return FavoriteDish.objects.filter(user=request.user, dish=dish).exists()
            
        return False


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class InstitutionDetailSerializer(serializers.ModelSerializer):
    tabs = EstablishmentTabSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.IntegerField(write_only=True)
    dish = DishListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'dish_id', 'dish', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.dish.price * item.quantity for item in obj.items.all())