from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.user import views as user_views
from api.trip import views as trip_views


router = DefaultRouter()
router.register(r"user", user_views.UserViewSet, basename="user")
router.register(r"trip", trip_views.TripViewSet, basename="trip")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
]
