from rest_framework.routers import DefaultRouter
from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    re_path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
