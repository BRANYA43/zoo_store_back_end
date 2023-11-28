from accounts import permissions, serializers
from django.contrib.auth import get_user_model
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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