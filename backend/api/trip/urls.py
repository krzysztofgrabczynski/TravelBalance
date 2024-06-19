from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.trip.views import TripViewSet

router = SimpleRouter()
router.register(r"trip", TripViewSet, basename="trip")


urlpatterns = [
    path("", include(router.urls)),
]
