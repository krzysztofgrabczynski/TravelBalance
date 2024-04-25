from django.urls import path

from api.user import views as user_views


urlpatterns = [
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
]
