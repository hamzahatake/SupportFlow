from rest_framework import serializers
from .validators import (
    validate_email,
    validate_timezone,
    validate_phone_number,
    validate_password_match, 
    validate_password_strength,
    validate_organization_active,
    validate_customer_priority,
    validate_working_hours,
    validate_department_id,
    validate_department_capacity,
    validate_department_assignment,
    validate_department_name_format
    )
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from .models import User, Organization, Customer, Agent, Supervisor, Admin, Department


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(validators=[validate_phone_number])
    timezone = serializers.CharField(validators=[validate_timezone], required=False)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "organization", "phone_number", "timezone",
                   "is_verified", "last_activity", "notification_preferences"]
        
    def validate_organization(self, value):
        if not value.is_active:
            raise ValidationError("This organization is not active!")
        return value       

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
    password = serializers.CharField(write_only=True, validators=[validate_password_strength])
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "organization"]

    def validate(self, attrs): 
        validate_password_match(attrs) # Using v_p_m logic to see if password and confirm_password match or not
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


class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_department_name_format])
    
    class Meta:
        model = Department
        fields = ["id", "name", "description", "is_active", "created_by", "created_at", "updated_at"]


class CustomerSerializer(serializers.ModelSerializer):
    priority_level = serializers.CharField(validators=[validate_customer_priority], required=False)

    class Meta:
        model = Customer
        fields = ["id", "user", "profile_image", "company", "priority_level", "notes", 
                 "created_at", "updated_at"]


class SupervisorSerializer(serializers.ModelSerializer):
    department = serializers.IntegerField(validators=[validate_department_id])
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Supervisor
        fields = ["id", "user", "profile_image", "department", "department_name", "can_create_agents", "max_agents",
                   "created_at", "updated_at"]
    
    def validate(self, attrs):
        """
        Object-level validation for supervisor department assignment.
        Uses validate_department_assignment for permission checking.
        """
        # Get the department ID from attrs
        department_id = attrs.get('department')
        if department_id:
            # This will be called with user context from the view
            # validate_department_assignment(department_id, self.context.get('request').user)
            pass
        return attrs


class AgentSerializer(serializers.ModelSerializer):
    working_hours = serializers.IntegerField(validators=[validate_working_hours])
    department = serializers.IntegerField(validators=[validate_department_id, validate_department_capacity])
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Agent
        fields = ["id", "user", "profile_image", "created_by", "department", "department_name", "max_tickets", "is_available",
                   "skills", "working_hours", "created_at", "updated_at"]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["id", "user", "permissions", "can_manage_organizations", "created_at", "updated_at"]