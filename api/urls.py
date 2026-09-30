from django.urls import path, include

urlpatterns = [
    path('restaurant/', include("apps.Restaraunt.urls")),
    path('users/', include("apps.Users.urls")),
    path('discounts/', include("apps.Discounts.urls")),
    path('profile/', include("apps.Profile.urls")),
    path("", include("api.yasg")),
]