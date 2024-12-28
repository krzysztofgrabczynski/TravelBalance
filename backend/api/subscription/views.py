from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
import requests
import os
from dotenv import load_dotenv

from api.subscription.JWT import generate_app_store_server_jwt
from api.subscription.tasks import send_purchase_subscription_notification


load_dotenv()


class Subscription(APIView):
    def post(self, request, *args, **kwargs):
        status_code = None

        try:
            data, user_id = self.subscription(request, *args, **kwargs)
            status_code = 200
            email_context = {
                "subscription_data": data,
                "status": "PASSED",
                "user_id": user_id,
                "to": os.environ.get("EMAIL_HOST_USER"),
            }
        except PermissionDenied as e:
            if isinstance(e.detail, dict):
                status_code = e.detail["status"]
                error_msg = e.detail["error_msg"]
            else:
                status_code = e.detail
                error_msg = None
            email_context = {
                "status": "FAILED",
                "status_code": status_code,
                "message": error_msg,
                "to": os.environ.get("EMAIL_HOST_USER"),
            }
        except Exception as e:
            status_code = 3000
            email_context = {
                "status": "FAILED",
                "status_code": status_code,
                "message": str(e),
                "to": os.environ.get("EMAIL_HOST_USER"),
            }

        send_purchase_subscription_notification.delay(email_context)
        return Response(
            {"status_code": status_code},
            status=200 if status_code == 200 else 401,
        )

    def subscription(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied("2001")
        transaction_id = request.data.get("transaction_id")
        if not transaction_id:
            raise PermissionDenied("2002")

        environment = request.data.get("environment", "PRODUCTION")
        if environment == "SANDBOX":
            url_path = (
                "https://api.storekit-sandbox.itunes.apple.com/inApps/v1/transactions/"
                + str(transaction_id)
            )
        if environment == "PRODUCTION":
            url_path = (
                "https://api.storekit.itunes.apple.com/inApps/v1/transactions/"
                + str(transaction_id)
            )

        headers = {
            "Authorization": "Bearer " + generate_app_store_server_jwt()
        }
        transaction = requests.get(url=url_path, headers=headers)
        response_data = transaction.json()

        if "errorMessage" in response_data:
            raise PermissionDenied(
                {"status": "2005", "error_msg": response_data["errorMessage"]}
            )

        decoded_transaction = jwt.decode(
            response_data["signedTransactionInfo"],
            algorithms="ES256",
            options={"verify_signature": False},
        )

        if not decoded_transaction["bundleId"] == os.environ.get(
            "IOS_IAP_BID"
        ):
            raise PermissionDenied("2003")

        try:
            user.is_premium = True
            user.save()
        except:
            raise PermissionDenied("2004")

        return decoded_transaction, user.id


# TESTING APPLE SERVER NOTIFICATIONS

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse


@require_POST
@csrf_exempt
def subscription_notifications(request):
    print("Start subscription notifications...")
    print("Request: ", request)
    print("Request dir: ", dir(request))
    print("Request vars: ", vars(request))
    try:
        data = request.data
        print("data: ", data)
    except:
        print("nie udalo sie printowac daty")

    print("End subscription notifications...")
    return HttpResponse("subscription notifications not impemented")
