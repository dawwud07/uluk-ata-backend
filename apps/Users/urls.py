from django.urls import path

from . import views
from .otp_send import SendOTPCodeView, VerifyOTPView, ResetPasswordView
from .views import RegisterVerifyView
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("deactivate/", views.DeactivateView.as_view(), name="deactivate"),
    path("otp-verify/", VerifyOTPView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("auth/send-otp/", SendOTPCodeView.as_view()),
    path("auth/register/", RegisterVerifyView.as_view()),
            
]

