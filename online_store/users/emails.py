from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    # Token stops working once the address is verified or changed.
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.email}{user.email_verified}{timestamp}'


email_verification_token = EmailVerificationTokenGenerator()


def encode_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def user_from_uid(uid):
    try:
        return User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return None


def _send(user, subject, intro, path, token):
    link = f'{settings.FRONTEND_URL}/{path}?uid={encode_uid(user)}&token={token}'
    send_mail(
        subject=subject,
        message=f'{intro}\n\n{link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def send_verification_email(user):
    if not user.email or user.email_verified:
        return
    _send(user, 'Verify your email | تأكيد البريد الإلكتروني',
          'Open this link to verify your email.\nافتح هذا الرابط لتأكيد بريدك الإلكتروني.',
          'verify-email', email_verification_token.make_token(user))


def send_password_reset_email(user):
    _send(user, 'Reset your password | إعادة تعيين كلمة المرور',
          'Open this link to choose a new password. Ignore this email if you did not ask for it.\n'
          'افتح هذا الرابط لاختيار كلمة مرور جديدة. تجاهل هذه الرسالة إذا لم تطلب ذلك.',
          'reset-password', default_token_generator.make_token(user))
