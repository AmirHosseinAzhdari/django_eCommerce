from kavenegar import *

API_Key = "Your API key from kavenegar website"


def send_otp_code(code: int, mobile_number: str) -> None:
    try:
        api = KavenegarAPI(API_Key)
        params = {
            "sender": "",
            "receptor": mobile_number,
            "message": f"کد  تایید شما برای ورود به سامانه: {code}",
        }
        responese = api.sms_send(params)
        print("successfully:: ", responese)
    except (APIException, HTTPException) as e:
        print(e)
