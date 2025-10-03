from zoneinfo import available_timezones
import phonenumbers
from django.conf import settings
from .models import Department, Agent, Organization, User
from rest_framework.validators import ValidationError

USER = settings.AUTH_USER_MODEL

def validate_phone_number(value): 
    if not value:
        return value
    
    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(f"Invalid phone number format: '{value}'. Please provide a valid phone number.")
    except phonenumbers.NumberParseException as e:
        raise ValidationError(f"Invalid phone number format: '{value}'. Error: {str(e)}")
    
    return value

def validate_email(value):
    if not value:
        raise ValidationError("Email address is required.")
    
    if USER.objects.filter(email=value).exists():
        raise ValidationError(f"Email address '{value}' is already registered. Please use a different email address.")
    
    return value

def validate_password_match(attrs): 
    password = attrs.get("password")
    confirm_password = attrs.get("confirm_password")

    if not password:
        raise ValidationError("Password field is required.")
    
    if not confirm_password:
        raise ValidationError("Confirm password field is required.")

    if password != confirm_password:
        raise ValidationError("Password and confirm password do not match. Please ensure both fields contain the same password.")
    
    return attrs

def validate_password_strength(value): 
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    if not any(c.isupper() for c in value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    
    if not any(c.islower() for c in value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    if not any(c.isdigit() for c in value):
        raise ValidationError("Password must contain at least one number.")
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in value):
        raise ValidationError("Password must contain at least one special character.")
    
    return value

def validate_organization_active(value): 
    if not value:
        raise ValidationError("Organization is required.")
    
    if not value.is_active:
        raise ValidationError(f"Organization '{value.name}' is not active. Please contact the administrator to activate this organization.")
    
    return value

def validate_timezone(value):
    if not value:
        raise ValidationError("Timezone is required.")
    
    valid_timezones = available_timezones()

    if value not in valid_timezones: 
        raise ValidationError(f"Invalid timezone '{value}'. Please provide a valid timezone (e.g., 'Asia/Karachi', 'America/New_York', 'Europe/London').")
    
    return value

def validate_customer_priority(value):
    valid_priorities = ['low', 'medium', 'high', 'VIP']
    
    if not value:
        raise ValidationError("Priority level is required.")
    
    if value not in valid_priorities:
        raise ValidationError(f"Invalid priority level '{value}'. Priority must be one of: {', '.join(valid_priorities)}.")
    
    return value

def validate_working_hours(value):
    minimum_hours = 4
    maximum_hours = 8

    if not isinstance(value, (int, float)):
        raise ValidationError("Working hours must be a valid number.")
    
    if value < minimum_hours:
        raise ValidationError(f"Working hours must be at least {minimum_hours} hours per day. Current value: {value} hours.")
    
    if value > maximum_hours:
        raise ValidationError(f"Working hours cannot exceed {maximum_hours} hours per day. Current value: {value} hours.")
    
    return value

def validate_department_id(value):
    if not value:
        raise ValidationError("Department ID is required.")
    
    try:
        department = Department.objects.get(id=value)
        
        if not department.is_active:
            raise ValidationError(f"Department '{department.name}' (ID: {value}) is not active. Please select an active department.")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError(f"Department with ID '{value}' does not exist. Please select a valid department.")

def validate_department_capacity(value):
    if not value:
        raise ValidationError("Department ID is required.")
    
    try:
        department = Department.objects.get(id=value)
        if not department.is_active:
            raise ValidationError(f"Cannot assign to inactive department '{department.name}' (ID: {value}). Please select an active department.")
        
        current_agent_count = Agent.objects.filter(department=department).count()
        max_capacity = 50
        
        if current_agent_count >= max_capacity:
            raise ValidationError(f"Department '{department.name}' (ID: {value}) is at maximum capacity ({current_agent_count}/{max_capacity} agents). Cannot assign more agents to this department.")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError(f"Department with ID '{value}' does not exist. Please select a valid department.")


def validate_department_assignment(value, user=None): # Validates if a user can be assigned to a specific department.
    if not value:
        raise ValidationError("Department ID is required.")
    
    try:
        department = Department.objects.get(id=value)
        
        if not department.is_active:
            raise ValidationError(f"Cannot assign to inactive department '{department.name}' (ID: {value}). Please select an active department.")
        
        if user:
            if hasattr(user, 'supervisor'): # Check if user is a supervisor trying to assign agents. hasattr gives true or false.
                supervisor = user.supervisor
                if supervisor.department and supervisor.department.id != value:
                    raise ValidationError(f"Supervisors can only assign agents to their own department. You can only assign agents to department '{supervisor.department.name}' (ID: {supervisor.department.id}), not '{department.name}' (ID: {value}).")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError(f"Department with ID '{value}' does not exist. Please select a valid department.")


def validate_department_assignment_field(value): # Field validator version without user parameter
    if not value:
        raise ValidationError("Department ID is required.")
    
    try:
        department = Department.objects.get(id=value)
        
        if not department.is_active:
            raise ValidationError(f"Cannot assign to inactive department '{department.name}' (ID: {value}). Please select an active department.")
        
        return value
        
    except Department.DoesNotExist:
        raise ValidationError(f"Department with ID '{value}' does not exist. Please select a valid department.")


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