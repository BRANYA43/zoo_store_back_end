from accounts import serializers
from accounts.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,  GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
