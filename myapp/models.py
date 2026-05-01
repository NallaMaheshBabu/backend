from django.db import models
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid
from django.db import models
from django.shortcuts import get_object_or_404









class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("superuser must have")

        return self.create_user(email, password, **extra_fields)



   

class Userdata(AbstractBaseUser,PermissionsMixin):
    user_id = models.AutoField(primary_key=True)# Auto-incrementing ID
    username = models.CharField(max_length=100,unique=True) 
    profiles=models.ImageField(upload_to='uploads/' ,default='uploads/defaults.jpg')
 # Max length of 150 characters
    email = models.EmailField(unique=True)  # Ensures email uniqueness
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']# Use hashed passwords for security

    def __str__(self):
        return self.username



class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True, editable=False)
    user = models.OneToOneField(Userdata, related_name='CustomToken', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex  # Generate unique token key
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.key





class ImagePost(models.Model):
    id=models.AutoField(primary_key=True) 
    user=models.ForeignKey(Userdata,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='uploads/')
    title = models.CharField(max_length=10)
    description = models.TextField()
    totallikes=models.PositiveIntegerField(default= 0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    post = models.ForeignKey(ImagePost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevents duplicate likes


    

