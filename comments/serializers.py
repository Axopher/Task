from rest_framework import serializers
from .models import Comment
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
