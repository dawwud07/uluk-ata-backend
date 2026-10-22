from django.urls import include, path

urlpatterns = [
    path("restaurant/", include("apps.Restaurant.urls")),
    path("users/", include("apps.Users.urls")),
    path("discounts/", include("apps.Discounts.urls")),
    path("profile/", include("apps.Profile.urls")),
    path("", include("api.yasg")),
]
