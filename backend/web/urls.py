from django.urls import path

from web import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "privacy-policy/",
        views.PrivacyPolicyView.as_view(),
        name="privacy-policy",
    ),
    path(
        "terms-of-use/",
        views.TermsOfUsereView.as_view(),
        name="terms-of-use",
    ),
    path(
        "account-deletion/",
        views.AccountDeletionView.as_view(),
        name="account-deletion",
    ),
]
