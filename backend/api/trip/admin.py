from django.contrib import admin

from api.trip.models import Trip, Country, Image


admin.site.register(Trip)
admin.site.register(Country)
admin.site.register(Image)
