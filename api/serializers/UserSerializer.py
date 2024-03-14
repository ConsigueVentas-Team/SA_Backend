from rest_framework import serializers
from api.model.UserModel import User
from api.functions.getRol import getRol

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.IntegerField(required=False)
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user       

# Serializer para el modelo User (para login)
class UserLoginSerializer(serializers.Serializer):
    # Especifica los campos requeridos para la autenticación
    username = serializers.CharField()
    password = serializers.CharField(write_only=False)
    
class UserSerializer(serializers.ModelSerializer):   
    password = serializers.CharField(write_only=False)
    # groups = serializers.CharField(write_only=True)
    # user_permissions = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

        depth = 3
    def get_role(self, user):
        return getRol(user.role)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['role'] = self.get_role(instance)
        
        if data['status_description'] is None:
            data['status_description'] = None
            
        return data

# Serializer para cambio de contraseña
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

class BirthdayDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['birthday']
