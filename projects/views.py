from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Project, ProjectMember
from .serializers import ProjectSerializer
from .permissions import IsAdminOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    ]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(
            project=project, user=self.request.user, role="Admin"
        )

    def destroy(self, request, pk=None):
        try:
            project = self.get_object()
            project.delete()
            return Response(
                {"detail": "Project deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
