from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Uluk Ata Food Delivery API",
        default_version="v1",
        description=(
            "Public API of the Uluk Ata food delivery service. "
            "Browse establishments, tabs, categories and dishes, manage the "
            "shopping cart, place orders, verify email/phone with OTP codes, "
            "and manage user profile and addresses."
        ),
        terms_of_service="https://uluk-ata.example.com/terms/",
        contact=openapi.Contact(email="api-support@uluk-ata.example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
