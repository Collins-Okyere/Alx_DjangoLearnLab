from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not exposed

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Use create_user for proper hashing
        Token.objects.create(user=user)  # Generate token upon registration
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return {'token': token.key, 'user_id': user.id, 'username': user.username}
        raise serializers.ValidationError("Invalid credentials")
