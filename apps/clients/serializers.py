# apps/clients/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cliente
User = get_user_model()

class CrearUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id_usuario', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # Incluye aquí todos los campos de tu modelo
        fields = [
            'id_cliente',
            'apellidos',
            'nombres',
            'ci',
            'sexo',
            'fecha_nacimiento',
            'telefono',
        ]