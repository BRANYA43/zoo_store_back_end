from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'uuid', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'joined']
        extra_kwargs = {
            'uuid': {'read_only': True},
            'email': {'style': {'placeholder': 'email@example.com'}},
            'password': {
                'write_only': True,
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
