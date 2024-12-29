from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, LoginSerializer
from .permissions import IsOwner


User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ["retrieve", "update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        if self.action in ["register", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, user)
        return user

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(
            {"error": "User Registration Successful."},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = authenticate(**serializer.validated_data)
            if not user:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def retrieve(self, request, pk):
        try:
            user = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        try:
            user = self.get_object()
            serializer = UserSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        try:
            user = self.get_object()
        except ObjectDoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response(
            {"detail": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
