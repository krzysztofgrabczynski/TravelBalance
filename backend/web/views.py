from django.views.generic import TemplateView
from django.contrib.staticfiles.storage import staticfiles_storage


class HomeView(TemplateView):
    template_name = ...


class PrivacyPolicyView(TemplateView):
    template_name = "policies/privacy-policy.html"


class TermsOfUsereView(TemplateView):
    template_name = "policies/terms-of-use.html"
