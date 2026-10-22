from django.urls import path

from .views import (
    AddressDetailView,
    AddressView,
    CreateOrderView,
    NotificationView,
    OrderDetailView,
    OrderReviewView,
    OrderView,
    PendingReviewsView,
    ReadNotificationsView,
    UpdateOrderStatusView,
)

urlpatterns = [
    path("addresses/", AddressView.as_view(), name="address-list"),
    path("addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
    path("orders/", OrderView.as_view(), name="order-list"),
    path("orders/create/", CreateOrderView.as_view(), name="order-create"),
    path(
        "orders/pending-reviews/",
        PendingReviewsView.as_view(),
        name="order-pending-reviews",
    ),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/review/", OrderReviewView.as_view(), name="order-review"),
    path(
        "orders/<int:pk>/status/", UpdateOrderStatusView.as_view(), name="order-status"
    ),
    path("notifications/", NotificationView.as_view(), name="notification-list"),
    path(
        "notifications/read-all/",
        ReadNotificationsView.as_view(),
        name="notification-read-all",
    ),
]
