from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Task
from django.core.exceptions import ValidationError

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.EmailField()

    class Meta:
        model = Task
        fields = "__all__"

    def validate_assigned_to(self, value):
        assigned_user = get_object_or_404(User, email=value)
        return assigned_user
