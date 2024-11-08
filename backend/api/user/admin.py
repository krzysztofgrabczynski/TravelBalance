from django.contrib import admin

from api.user.models import ForgotPasswordToken, FeedbackFromUser


admin.site.register(ForgotPasswordToken)


@admin.register(FeedbackFromUser)
class FeedbackFromUserAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "message", "created_date", "resolved")
    list_filter = ("user", "type", "resolved")
    ordering = ("-created_date",)
