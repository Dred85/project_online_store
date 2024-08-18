import secrets
from django.urls import reverse

from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404

import random
import string

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def generate_random_password(length=8):
    """Генерирует случайный пароль заданной длины."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))


class PasswordResetView(View):
    def get(self, request):
        return render(request, "users/password_reset.html")

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            new_password = User.objects.make_random_password()
            user.password = make_password(new_password)
            user.save()

            # Отправка email с новым паролем
            send_mail(
                "Ваш новый пароль",
                f"Ваш новый пароль: {new_password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
                # fail_silently=False,
            )
            return redirect(reverse("users:login"))
        except Exception as e:
            return render(request, "users/do_not_know_email.html")
