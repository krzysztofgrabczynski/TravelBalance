from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.user import views as user_views
from api.trip import views as trip_views
from api.expense import views as expense_views


router = DefaultRouter()
router.register(r"user", user_views.UserViewSet, basename="user")
router.register(r"trip", trip_views.TripViewSet, basename="trip")
router.register(r"expense", expense_views.ExpenseViewSet, basename="expense")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
]
