from django.urls import path, include

urlpatterns = [
    path('restaurant/', include("apps.Restaraunt.urls")),
    path('users/', include("apps.Users.urls")),
    path('ckidki/', include("apps.Ckidki.urls")),
    path('profile/', include("apps.Profile.urls")),
    path("", include("api.yasg")),
]