from django.contrib import admin

from api.expense.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trip_id",
        "user_id",
        "username",
        "title",
        "cost",
        "category",
        "date",
    )
    list_filter = ("trip", "category", "date")
    ordering = ("-date",)

    def trip_id(self, obj: Expense) -> int:
        return obj.trip.id

    def user_id(self, obj: Expense) -> int:
        return obj.trip.user.id

    def username(self, obj: Expense) -> str:
        return obj.trip.user.username


admin.site.register(Expense, ExpenseAdmin)
