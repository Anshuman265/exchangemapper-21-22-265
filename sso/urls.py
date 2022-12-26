from django.urls import path,include

from . import views

urlpatterns = [
    path("login/", views.redirect_to_login, name="login"),
    path("complete/", views.authenticate_code, name="auth_complete"),
    path("logout/", views.client_logout, name="logout"),
]