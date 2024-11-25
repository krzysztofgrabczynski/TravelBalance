from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


class HomeView(TemplateView):
    template_name = ...


class PrivacyPolicyView(TemplateView):
    template_name = "policies/privacy-policy.html"


class TermsOfUsereView(TemplateView):
    template_name = "policies/terms-of-use.html"


class AdsAppView(RedirectView):
    url = staticfiles_storage.url("ads-app.txt")
