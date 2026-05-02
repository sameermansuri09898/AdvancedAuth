
from rest_framework import serializers  
from .models import User,Otp
from Account.utils import send_otp_email,random_otp
from django.contrib.auth import get_user_model
from django.utils import timezone

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
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']

class Otpserializer(serializers.Serializer):

    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)


    def validate(self,attrs):
        email=attrs.get('email')
        otp=attrs.get('otp')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        userobject=Otp.objects.filter(user=user).last()    

        if userobject is None:   
            raise serializers.ValidationError("Invalid OTP")
        if user.is_varified:
            raise serializers.ValidationError("User is Already Verified")

        if userobject.is_otp_expired():
            raise serializers.ValidationError("OTP has expired")   

        if userobject.otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        user.is_verified = True
        user.save()
        userobject.delete()
        return attrs    

class ResendOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()


    def validate_email(self,value):
        email=value
        if not email:
            raise serializers.ValidationError("Email is required")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not found")

        user=User.objects.get(email=email)
        if user.is_verified:
            raise serializers.ValidationError("User is already verified")

        lastotp=Otp.objects.filter(user=user).last()    
        time_limit = lastotp.created_at + timezone.timedelta(seconds=60)   
        if time_limit >= timezone.now():
            seconds_remaining = (time_limit - timezone.now()).total_seconds()
            raise serializers.ValidationError(f"Wait for {int(seconds_remaining)} seconds to resend OTP")  

        self.user = user 
        return value
            

class passwordchange(serializers.Serializer):
    email=serializers.EmailField()
    old_password=serializers.CharField()
    new_password=serializers.CharField()
    confirm_new_password=serializers.CharField()



    def validate(self,attrs):
        user=self.context['request'].user
        email=attrs.get('email')
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        confirm_new_password=attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Confirm password not matched")

        if not email or not old_password or not new_password or not confirm_new_password:
            raise serializers.ValidationError("All fields are required")

        user=User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User not found")    

        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid old password")
        
        if old_password == new_password:
            raise serializers.ValidationError("New password should not be same as old password")
        #  wrong methid ye sirf validate krta hai not save
        attrs['user']=user
        return attrs
        
    def save(self):
        user=self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()   
        return {'msg':'Password changed successfully'}
        
        





        
