from django.urls import path

from .views import (
    AddToCartView,
    CartItemView,
    CartView,
    CategoryListView,
    ClearCartView,
    DishDetailView,
    DishListView,
    EstablishmentTabListView,
    FavoriteListView,
    InstitutionDetailView,
    InstitutionListView,
    ToggleFavoriteView,
)

urlpatterns = [
    path("institutions/", InstitutionListView.as_view()),
    path("institutions/<int:pk>/", InstitutionDetailView.as_view()),
    path("tabs/", EstablishmentTabListView.as_view()),
    path("categories/", CategoryListView.as_view()),
    path("dishes/", DishListView.as_view()),
    path("dishes/<int:pk>/", DishDetailView.as_view()),
    path("dishes/<int:pk>/favorite/", ToggleFavoriteView.as_view()),
    path("favorites/", FavoriteListView.as_view()),
    path("cart/", CartView.as_view()),
    path("cart/add/", AddToCartView.as_view()),
    path("cart/items/<int:pk>/", CartItemView.as_view()),
    path("cart/clear/", ClearCartView.as_view()),
]
