from django.contrib import admin

from api.user.models import ForgotPasswordToken


admin.site.register(ForgotPasswordToken)
