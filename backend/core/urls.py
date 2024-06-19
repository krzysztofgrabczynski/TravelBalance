from django.contrib import admin
from django.urls import path, include

from api.user import urls as user_urls
from api.trip import urls as trip_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(user_urls)),
    path("api/", include(trip_urls)),
]
