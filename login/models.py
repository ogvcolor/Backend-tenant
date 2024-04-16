from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid



class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

class CustomUser(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True

    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(email, password, **extra_fields)
        

class UserProfile(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    job_position = models.CharField(max_length=100)
    directory = models.CharField(max_length=100)
    email = models.CharField(max_length=200, default='teste@teste.com.br')
    privacy_policy = models.BooleanField(default=False) # se o ususario aceitou os termos de privacidade
    canseename = models.BooleanField(default = False) # Indica se o usuario pode ser visualizado ou não. 
    
    def __str__(self) -> str:
        return self.email

class AccessLevel(models.Model):

    id = models.BigAutoField(primary_key=True)
    profile	= models.CharField(max_length=100)
    column = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default = 'Plant')
    source_column = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    

class UserAccessLevel(models.Model):

    id = models.BigAutoField(primary_key=True)
    auth_user = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    access_level = models.CharField(max_length=100)
