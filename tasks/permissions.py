from rest_framework import permissions
from projects.models import ProjectMember


class IsProjectMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return request.user and request.user.is_authenticated

        if view.action == "create":
            # in order to create tasks for a project, project needs to exist
            # Also, that task creating user need to be part of the project
            project_id = request.data.get("project")
            if project_id:
                return ProjectMember.objects.filter(
                    project_id=project_id, user=request.user
                ).exists()
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ["update", "partial_update", "destroy"]:
            if obj.assigned_to == request.user or obj.project.owner == request.user:
                return True
            return False
        return True
