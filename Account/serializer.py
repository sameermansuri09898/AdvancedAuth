
from rest_framework import serializers
from .models import User,Otp
from Account.utils import send_otp_email,random_otp
from django.contrib.auth import get_user_model

User=get_user_model()

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
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data,is_verified=False)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self,attrs):
        email=attrs.get('email')
        otp=attrs.get('otp')

        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")    

        return attrs

    