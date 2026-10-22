from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Dish, EstablishmentTab, FavoriteDish, Institution
from .serializer import (
    CartItemSerializer,
    CartSerializer,
    CategorySerializer,
    DishDetailSerializer,
    DishListSerializer,
    EstablishmentTabSerializer,
    InstitutionDetailSerializer,
    InstitutionSerializer,
)
from .services import (
    add_dish_to_cart,
    clear_user_cart,
    get_or_create_user_cart,
    set_cart_item_quantity,
)


class InstitutionListView(generics.ListAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionDetailView(generics.RetrieveAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionDetailSerializer


class EstablishmentTabListView(generics.ListAPIView):
    serializer_class = EstablishmentTabSerializer

    def get_queryset(self):
        queryset = EstablishmentTab.objects.all()
        institution_id = self.request.query_params.get("institution")
        if institution_id:
            queryset = queryset.filter(institution_id=institution_id)
        return queryset


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        tab_id = self.request.query_params.get("tab")
        if tab_id:
            queryset = queryset.filter(tab_id=tab_id)
        institution_id = self.request.query_params.get("institution")
        if institution_id:
            queryset = queryset.filter(tab__institution_id=institution_id)
        return queryset


class DishListView(generics.ListAPIView):
    serializer_class = DishListSerializer

    def get_queryset(self):
        queryset = Dish.objects.select_related("category__tab__institution").all()
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        tab_id = self.request.query_params.get("tab")
        if tab_id:
            queryset = queryset.filter(category__tab_id=tab_id)
        institution_id = self.request.query_params.get("institution")
        if institution_id:
            queryset = queryset.filter(category__tab__institution_id=institution_id)
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
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
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)

        FavoriteDish.objects.create(user=request.user, dish=dish)
        return Response({"is_favorite": True}, status=status.HTTP_201_CREATED)


class FavoriteListView(generics.ListAPIView):
    serializer_class = DishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dish.objects.filter(favorited_by__user=self.request.user)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_user_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            dish_id = serializer.validated_data["dish_id"]
            quantity = serializer.validated_data.get("quantity", 1)

            cart_item = add_dish_to_cart(request.user, dish_id, quantity)
            return Response(
                CartItemSerializer(cart_item).data, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        quantity = request.data.get("quantity")
        if quantity is None:
            return Response(
                {"quantity": "Provide a quantity."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"quantity": "Quantity must be a number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = set_cart_item_quantity(request.user, pk, quantity)
        if result is None:
            return Response(
                {"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if result == "deleted":
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(CartItemSerializer(result).data)

    def delete(self, request, pk):
        result = set_cart_item_quantity(request.user, pk, 0)
        if result is None:
            return Response(
                {"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        clear_user_cart(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
