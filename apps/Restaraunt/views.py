from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Institution, Dish, FavoriteDish, Cart, CartItem
from .serializer import (
    InstitutionSerializer,
    InstitutionDetailSerializer,
    DishListSerializer,
    DishDetailSerializer,
    CartSerializer,
    CartItemSerializer
)


class InstitutionListView(generics.ListAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionDetailView(generics.RetrieveAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionDetailSerializer


class DishListView(generics.ListAPIView):
    serializer_class = DishListSerializer

    def get_queryset(self):
        queryset = Dish.objects.all()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class DishDetailView(generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishDetailSerializer


class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        favorite = FavoriteDish.objects.filter(user=request.user, dish=dish).first()

        if favorite:
            favorite.delete()
            return Response({'is_favorite': False}, status=status.HTTP_200_OK)

        FavoriteDish.objects.create(user=request.user, dish=dish)
        return Response({'is_favorite': True}, status=status.HTTP_201_CREATED)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            dish_id = serializer.validated_data['dish_id']
            quantity = serializer.validated_data.get('quantity', 1)

            dish = get_object_or_404(Dish, id=dish_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)