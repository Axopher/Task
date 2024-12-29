from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import ValidationError
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        # Normally we will have separate endpoint for updating the password of the user
        # but here just accomodating in five endpoints
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
