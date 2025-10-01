from .models import User, Organization
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class UserSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "organization"]


class UserLogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(email=email, password=password)

        if not User:
            raise ValidationError("Invalid credentials. Please try again!")
        
        attrs["user"] = user
        return attrs
        
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError("Passowrd and confirm password doesn't match!")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data["password"]

        user = User(**validated_data)
        if len(password) < 8:
            raise ValidationError("Password must has 8 or more characters!")
        
        user.set_password(password)
        user.save()
        return user


class OrganizationSerializer(serializers.Serializer):
    class Meta:
        model = Organization
        fields = ["name", "slug", "plan", "stripe_customer_id"]