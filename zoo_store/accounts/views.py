from accounts import serializers
from django.contrib.auth import get_user_model
from rest_framework import viewsets

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    create_serializer_class = serializers.UserCreateSerializer
    manage_serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        return self.manage_serializer_class
