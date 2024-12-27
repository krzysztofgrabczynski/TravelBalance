from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
import requests
import os
from dotenv import load_dotenv

from api.subscription.JWT import generate_app_store_server_jwt


load_dotenv()


class Subscription(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied("status=2001")
        transaction_id = request.data.get("transaction_id")
        if not transaction_id:
            raise PermissionDenied("status=2002")

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

        decoded_transaction = jwt.decode(
            response_data["signedTransactionInfo"],
            algorithms="ES256",
            options={"verify_signature": False},
        )

        if not decoded_transaction["bundleId"] == os.environ.get(
            "IOS_IAP_BID"
        ):
            raise PermissionDenied("status=2003")

        try:
            user.is_premium = True
            user.save()
        except:
            raise PermissionDenied("status=2004")

        return Response(status=200)
