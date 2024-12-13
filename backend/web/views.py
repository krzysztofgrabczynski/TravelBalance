from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


class PrivacyPolicyView(TemplateView):
    template_name = "policies/privacy-policy.html"


class TermsOfUsereView(TemplateView):
    template_name = "policies/terms-of-use.html"


class AccountDeletionView(TemplateView):
    template_name = "policies/account-deletion.html"
