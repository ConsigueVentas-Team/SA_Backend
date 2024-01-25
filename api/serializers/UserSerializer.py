from rest_framework import serializers
from api.model.UserModel import User
class UserRegisterSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user       

# Serializer para el modelo User (para login)
class UserLoginSerializer(serializers.Serializer):
    # Especifica los campos requeridos para la autenticación
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    

class UserSerializer(serializers.ModelSerializer):   
    password = serializers.CharField(write_only=True)
    # groups = serializers.CharField(write_only=True)
    # user_permissions = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'


# Serializer para cambio de contraseña
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
