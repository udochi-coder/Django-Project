from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.constants import LEVEL_CHOICES, ROLE_STUDENT


class StudentEnrollmentSerializer(serializers.Serializer):
    department = serializers.CharField(max_length=55, required=True)
    level = serializers.ChoiceField(choices=LEVEL_CHOICES, required=False, default="100")
    entry_year = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class StaffRegistrationSerializer(serializers.Serializer):
    department = serializers.CharField(max_length=55, required=True)
    email = serializers.EmailField()
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user.role != ROLE_STUDENT:
            raise serializers.ValidationError(
                "Only student accounts can sign in here. Please check the demo account instead."
            )

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
        }
        return data
