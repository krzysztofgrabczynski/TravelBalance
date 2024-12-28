from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.user import views as user_views
from api.trip import views as trip_views
from api.expense import views as expense_views

from api.subscription import views as subscription_views


router = DefaultRouter()
router.register(r"user", user_views.UserViewSet, basename="user")
router.register(r"trip", trip_views.TripViewSet, basename="trip")
router.register(
    r"trip/(?P<trip_pk>\d+)/expense",
    expense_views.ExpenseViewSet,
    basename="expense",
)


urlpatterns = [
    path("", include(router.urls)),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path(
        "subscription/",
        subscription_views.Subscription.as_view(),
        name="subscription",
    ),
    path(
        "subscription/notifications/",
        subscription_views.subscription_notifications,
        name="subscription-notifications",
    ),
]
