
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'password','confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs    

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must be digits only")
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits")
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']