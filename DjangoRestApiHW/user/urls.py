from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationAPIView.as_view(), name="register"),
    path("login/", views.AuthorizationAPIView.as_view(), name="login"),
    path("confirm/", views.ConfirmAPIView.as_view(), name="confirm"),
    path("auth/google/",views.GoogleLoginAPIView.as_view(),name="google-login",),
]
