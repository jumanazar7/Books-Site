from django.urls import path
from .views import register, logout_user, login_user, password_reset

app_name = "auth"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('password/reset/', password_reset, name="password_reset")
]