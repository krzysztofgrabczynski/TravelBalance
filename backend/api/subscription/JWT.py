import jwt
import calendar
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


def generate_app_store_server_jwt() -> str:
    with open(os.environ.get("IOS_IAP_PRIVATE_KEY_PATH"), "r") as file:
        private_key = file.read()

    headers = {"kid": os.environ.get("IOS_IAP_KID")}

    future_time = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(minutes=50)

    payload = {
        "iss": os.environ.get("IOS_IAP_ISS"),
        "exp": calendar.timegm(future_time.timetuple()),
        "aud": "appstoreconnect-v1",
        "bid": os.environ.get("IOS_IAP_BID"),
    }

    return jwt.encode(
        payload=payload, key=private_key, algorithm="ES256", headers=headers
    )
