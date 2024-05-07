from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.user import views as user_views


router = DefaultRouter()
router.register(r"user", user_views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
]
