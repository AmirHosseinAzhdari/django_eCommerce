from kavenegar import *


def send_otp_code(code: int, mobile_number: str) -> None:
    try:
        api = KavenegarAPI(
            "3379796B756A68786E33785A4458544F7062616E39596C652F5A76314A56454F56447A51416732424E36303D"
        )
        params = {
            "sender": "",
            "receptor": mobile_number,
            "message": f"کد  تایید شما برای ورود به سامانه: {code}",
        }
        responese = api.sms_send(params)
        print("successfully:: ", responese)
    except (APIException, HTTPException) as e:
        print(e)
