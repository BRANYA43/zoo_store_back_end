from accounts import permissions, serializers
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsOwner]
    http_method_names = ['get', 'patch']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related(
        Prefetch('profile', queryset=Profile.objects.all())
    ).all()
    create_serializer_class = serializers.UserCreateSerializer
    manage_serializer_class = serializers.UserSerializer
    create_permissions_classes = [rest_permissions.AllowAny]
    manage_permissions_classes = [permissions.IsOwnerOrStaff]

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        return self.manage_serializer_class

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = self.create_permissions_classes
        else:
            self.permission_classes = self.manage_permissions_classes
        return super().get_permissions()
