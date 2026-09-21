from django.urls import path
from .views import (
    InstitutionListView,
    InstitutionDetailView,
    DishListView,
    DishDetailView,
    ToggleFavoriteView,
    CartView,
    AddToCartView
)

urlpatterns = [
    path('institutions/', InstitutionListView.as_view()),
    path('institutions/<int:pk>/', InstitutionDetailView.as_view()),
    path('dishes/', DishListView.as_view()),
    path('dishes/<int:pk>/', DishDetailView.as_view()),
    path('dishes/<int:pk>/favorite/', ToggleFavoriteView.as_view()),
    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
]
