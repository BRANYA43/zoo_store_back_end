from accounts.models import Profile
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
        extra_kwargs = {
            'key': {
                'label': 'token',
                'read_only': True,
            },
        }


class AuthTokenCreateSerializer(AuthTokenSerializer):
    email = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(min_length=8, trim_whitespace=False, write_only=True)

    class Meta(AuthTokenSerializer.Meta):
        fields = ['key', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise AuthenticationFailed

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token = Token.objects.get_or_create(user=user)
        return token


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'uuid', 'user', 'first_name', 'last_name']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'user': {'read_only': True},
            'first_name': {'style': {'placeholder': 'Rick'}},
            'last_name': {'style': {'placeholder': 'Sanchez'}},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'uuid', 'profile', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login',
                  'joined']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'email': {'style': {'placeholder': 'email@example.com'}},
            'password': {
                'write_only': True,
                'trim_whitespace': True,
                'style': {'input_type': 'password'}
            },
            'last_login': {'read_only': True},
            'joined': {'read_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['url', 'uuid', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
