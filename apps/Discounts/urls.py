from django.urls import path

from .views import PromotionDetailAPIView, PromotionListAPIView

urlpatterns = [
    path("promotions/", PromotionListAPIView.as_view(), name="promotion-list"),
    path(
        "promotions/<int:pk>/",
        PromotionDetailAPIView.as_view(),
        name="promotion-detail",
    ),
]
