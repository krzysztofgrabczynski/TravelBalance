import stripe
from django.http import HttpResponse
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User


@require_POST
@csrf_exempt
def stripe_webhook(request: WSGIRequest) -> HttpResponse:
    print("start webhook")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.errors.SignatureVerificationError:
        return HttpResponse(status=400)

    session = event.data.object
    print(session)
    if event.type == "payment_intent.succeeded":
        webhook_event_completed(session)

    return HttpResponse(status=200)


def webhook_event_completed(session: stripe.checkout._session.Session) -> None:
    if session.mode == "payment" and session.payment_status == "paid":
        print(session)
