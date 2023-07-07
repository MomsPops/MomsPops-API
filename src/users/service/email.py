from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site

from ..tasks import send_email_task


class ActivationUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.username)
        )


def get_activation_token(user) -> str:
    return ActivationUserTokenGenerator().make_token(user=user)     # type: ignore


def check_activation_token(user, token: str) -> bool:
    return ActivationUserTokenGenerator().check_token(user=user, token=token)     # type: ignore


def send_email(request, user):
    message_subject = "Activate your user account."
    message_content = render_to_string(
        template_name="users/email_activation.html",
        context={
            "user": user.username,
            "protocol": "https" if request.is_secure() else "http",
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": get_activation_token(user)
        }
    )
    send_email_task.apply_async(
        args=[message_subject, message_content, user.email]
    )


def decode_uid(uid: str):
    return force_str(urlsafe_base64_decode(uid))
