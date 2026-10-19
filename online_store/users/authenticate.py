from django.db.models import F
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings


class LeanUserMixin:
    """Load user without columns auth never reads; deferred fields lazy-load if touched."""
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            # seller_pk / customer_pk come from the same query (LEFT JOIN on the one-to-one tables),
            # so views can tell the role without another query. None means the user has no such profile.
            user = (self.user_model.objects
                    .defer('password', 'last_login', 'is_superuser')
                    .annotate(seller_pk=F('seller__id'), customer_pk=F('customer__id'))
                    .get(**{api_settings.USER_ID_FIELD: user_id}))
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")
        return user


class CookieJWTAuthentication(LeanUserMixin, JWTAuthentication):
    def authenticate(self, request):
        # Look for the 'access_token' in cookies
        raw_token = request.COOKIES.get('access_token')

        if raw_token is None:
            return None

        # Pass the token to the standard validator
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
