from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from base_app.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'cpf', 'telefone', 'nivel_acesso', 'first_name', 'last_name']

    def create(self, validated_data):
        # Hash da senha antes de salvar o usuário
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash da senha antes de atualizar o usuário
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):

    user_cpf = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
