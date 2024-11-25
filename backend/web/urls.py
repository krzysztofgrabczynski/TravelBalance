from django.urls import path

from web import views


urlpatterns = [
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
        "ads-app.txt/",
        views.AdsAppView.as_view(),
        name="ads-app.txt",
    ),
]
