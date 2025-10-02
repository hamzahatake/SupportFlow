from .models import User, Organization, Customer, Agent, Supervisor, Admin
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "organization", "phone_number", "timezone",
                   "is_verified", "last_activity", "notification_preferences"]

class UserLogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("Invalid credentials. Please try again!")
        
        attrs["user"] = user
        return attrs
        
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "organization"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already registered!")
        return value
        
    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]

        if password != confirm_password:
            raise ValidationError("Password and confirm password doesn't match!")
        if len(password) < 8:
            raise ValidationError("Password must be bigger than 8 characters!")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data["password"]

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "plan", "stripe_customer_id", "domain", "settings", 
                 "is_active", "max_users", "trial_ends_at", "created_at", "updated_at"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user", "profile_image", "company", "priority_level", "notes", 
                 "created_at", "updated_at"]


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["id", "user", "profile_image", "department", "can_create_agents", "max_agents",
                   "created_at", "updated_at"]


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "user", "profile_image", "created_by", "department", "max_tickets", "is_available",
                   "skills", "working_hours", "created_at", "updated_at"]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "user", "permissions", "can_manage_organizations", "created_at", "updated_at"]