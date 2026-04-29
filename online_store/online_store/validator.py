import re
from rest_framework import serializers

def validate_password(self, password):
  
        if len(password) < 8:
            raise serializers.ValidationError('password is too short')
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError('Password must contain at least upper case character')
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError('Password must contain at least 1 character')
        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return password