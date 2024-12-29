from rest_framework import viewsets, permissions

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsProjectMember


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
