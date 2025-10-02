from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

USER = settings.AUTH_USER_MODEL


class Organization(models.Model):
    PLANS = [
        ("basic", "BASIC"),
        ("best", "BEST"),
        ("premium", "PREMIUM")
    ]

    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(blank=False, null=False, unique=True)
    invite_token = models.UUIDField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    plan = models.CharField(max_length=100, choices=PLANS, default="best")
    domain = models.CharField(max_length=255, blank=True, null=True)
    settings = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    max_users = models.PositiveIntegerField(default=10)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['plan']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) #This is enough for changing name into slug
            slug = base_slug
            counter = 1  

            while Organization.objects.filter(slug=slug).exists(): # Adding counter logic so organizations with same name can exist like 'toei-1' 'toei-2' etc
                slug = f"{base_slug} - {counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class User(AbstractUser):
    # email, password, first_name, last_name, is_active, date_joined, last_login
    ROLES = [
        ("customer", "CUSTOMER"),
        ("agent", "AGENT"),
        ("supervisor", "SUPERVISOR"),
        ("admin", "ADMIN")
    ]
    
    email = models.EmailField(unique=True) 
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [] # When USERNAME_FIELD is email, email must NOT be in REQUIRED_FIELDS
    role = models.CharField(max_length=50, choices=ROLES, default="customer")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['organization']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_verified']),
        ]

    def __str__(self):
        return f"{self.email}: {self.role}"
    

class Customer(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High'),
        ('vip', 'VIP')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    profile_image = models.ImageField(upload_to="media/customer/profile_image", blank=True, null=True)
 
    company = models.CharField(max_length=255, blank=True, null=True)
    priority_level = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Supervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supervisor")
    profile_image = models.ImageField(upload_to="media/supervisor/profile_image", blank=True, null=True)
    
    department = models.CharField(max_length=100, blank=True, null=True)
    can_create_agents = models.BooleanField(default=True)
    max_agents = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent")
    profile_image = models.ImageField(upload_to="media/agent/profile_image", blank=True, null=True)
    created_by = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    
    department = models.CharField(max_length=100, blank=True, null=True)
    max_tickets = models.PositiveIntegerField(default=50)
    is_available = models.BooleanField(default=True)
    skills = models.JSONField(default=list, blank=True)  # e.g., ['technical', 'billing']
    working_hours = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    
    permissions = models.JSONField(default=list, blank=True)
    can_manage_organizations = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)