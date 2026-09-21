from django.urls import path

from . import views
from apps.Users.otp_send import SendOTPCodeView  , VerifyOTPView , ResetPasswordView
from django.urls import path
from apps.Users.views import SendOTPView, RegisterVerifyView
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("deactivate/", views.DeactivateView.as_view(), name="deactivate"),
    path("otp-email/" , SendOTPCodeView.as_view()) , 
    path("otp-veryfy/" , VerifyOTPView.as_view() ) , 
    path("reset-password/" , ResetPasswordView.as_view()) ,
    path("auth/send-otp/", SendOTPView.as_view()),
    path("auth/register/", RegisterVerifyView.as_view()),
            
]

