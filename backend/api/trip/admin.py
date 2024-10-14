from django.contrib import admin

from api.trip.models import Trip, Country


admin.site.register(Trip)
admin.site.register(Country)
