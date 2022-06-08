import random
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from .models import OtpCode, User
from .forms import UserRegisterForm, VerifyOtpForm
from utils import send_otp_code


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(random_code, form.cleaned_data["mobile_number"])
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
        return render(request, "accounts/register.html", {"form": form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyOtpForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify_code.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_register_info"]
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = get_object_or_404(
                OtpCode, mobile_number=user_session["mobile_number"]
            )
            if cd["code"] == code_instance.code:
                User.objects.create_user(
                    user_session["mobile_number"],
                    user_session["email"],
                    user_session["full_name"],
                    user_session["password"],
                )
                code_instance.delete()
                messages.success(request, "You are registered succesfully", "success")
            else:
                messages.error(request, "Invalid code", "danger")
                return redirect("accounts:user-verify-code")
        return redirect("home:home")
