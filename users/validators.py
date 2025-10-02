from zoneinfo import available_timezones
import phonenumbers
from django.conf import settings
from rest_framework.validators import ValidationError

USER = settings.AUTH_USER_MODEL

def validate_phone_number(value): # For UserSerializer
    if not value:
        return value
    
    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError("Invalid phone number format.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number format.")
    
    return value

def validate_email(value): # For UserRegistrationSerializer
        if USER.objects.filter(email=value).exists():
            raise ValidationError("This email is already registered.")
        return value

def validate_password_match(attrs): # For UserRegistrationSerializer
    password = attrs.get("password")
    confirm_password = attrs.get("confirm_password")

    if not password or not confirm_password:
        raise ValidationError("Both password fields are required.")

    if password != confirm_password:
        raise ValidationError("Password and confirm password doesn't match.")
    
    return attrs

def validate_password_strength(value): # For UserRegistrationSerializer
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    return value

def validate_organization_active(value): # For UserSerializer
    if not value.is_active:
        raise ValidationError("This organization is not active!")
    return value

def validate_timezone(value): # For UserSerializer
    valid_timezones = available_timezones()

    if value not in valid_timezones: 
        raise ValidationError("Please provide a valid timezone (e.g., Asia/Karachi).")
    return value

def validate_customer_priority(value):
    if not value:
        raise ValidationError("Invalid priority. Priority must be one of ['low', 'medium', 'high', 'VIP].")
    return value

def validate_working_hours(value):
    minimum_hours = 4
    maximum_hours = 8

    if value < minimum_hours:
        raise ValidationError("Working hours must be at least 4 hours per day.")
    
    if value > maximum_hours:
        raise ValidationError("Working hours cannot exceed 8 hours per day.")
    
    return value

def validate_department_id(value):
    from .models import Department

    try:
        department = Department.objects.get(id=value)
        
        if not department.is_active:
            raise ValidationError("Department is not active.")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError("Department does not exist.")

def validate_department_capacity(value):
    from .models import Department, Agent
    
    try:
        department = Department.objects.get(id=value)
        if not department.is_active:
            raise ValidationError("Cannot assign to inactive department.")
        
        current_agent_count = Agent.objects.filter(department=department).count()
        
        max_capacity = 50
        if current_agent_count >= max_capacity:
            raise ValidationError(f"Department '{department.name}' is at maximum capacity ({max_capacity} agents).")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError("Department does not exist.")


def validate_department_assignment(value, user=None): # Validates if a user can be assigned to a specific department.
    from .models import Department
    
    try:
        department = Department.objects.get(id=value)
        
        if not department.is_active:
            raise ValidationError("Cannot assign to inactive department.")
        
        if user:
            if hasattr(user, 'supervisor'): # Check if user is a supervisor trying to assign agents
                supervisor = user.supervisor
                if supervisor.department and supervisor.department.id != value:
                    raise ValidationError("Supervisors can only assign agents to their own department.")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError("Department does not exist.")


def validate_department_name_format(value):
    import re
    
    value = value.strip()
    
    if not value:
        raise ValidationError("Department name cannot be empty.")
    
    if len(value) < 2:
        raise ValidationError("Department name must be at least 2 characters long.")
    
    if len(value) > 50:
        raise ValidationError("Department name cannot exceed 50 characters.")
    
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', value):
        raise ValidationError("Department name can only contain letters, numbers, spaces, hyphens, and underscores.")
    
    reserved_names = ["admin", "root", "superuser", "null", "system", "test", "demo"]
    if value.lower() in reserved_names:
        raise ValidationError(f"Name '{value}' is reserved and cannot be used.")
    
    if '  ' in value:  # Double spaces
        raise ValidationError("Department name cannot contain consecutive spaces.")
    
    if value.startswith(' ') or value.endswith(' '):
        raise ValidationError("Department name cannot start or end with spaces.")
    
    return value

    