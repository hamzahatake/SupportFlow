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
    plan = models.CharField(max_length=100, choices=PLANS, default="BEST")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        ("supervisor", "SUPERVISOR")
    ]
    
    email = models.EmailField(unique=True) 
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [] # When USERNAME_FIELD is email, email must NOT be in REQUIRED_FIELDS
    role = models.CharField(max_length=50, choices=ROLES, default="Customer")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.email}: {self.role}"
    

