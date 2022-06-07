import random
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import OtpCode
from .forms import UserRegisterForm
from utils import send_otp_codes


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_codes(random_code, form.cleaned_data["mobile_number"])
            OtpCode.objects.create(
                mobile_number=form.cleaned_data["mobile_number"], code=random_code
            )
            # add user info to session
            request.session["user_register_info"] = {
                "mobile_number": form.cleaned_data["mobile_number"],
                "email": form.cleaned_data["email"],
                "full_name": form.cleaned_data["full_name"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "Registered code sent successfully", "success")
            return redirect("accounts:user-verify-code")
        return redirect("home:home")


class UserRegisterVerifyCodeView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
