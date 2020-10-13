from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    #def validate_password(self, value):
       # if value.isalnum():
        #    raise serializers.ValidationError('password must have atleast one special character.')
        #return value