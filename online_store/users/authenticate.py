from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Look for the 'access_token' in cookies
        raw_token = request.COOKIES.get('access_token')
        
        if raw_token is None:
            return None

        # Pass the token to the standard validator
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token