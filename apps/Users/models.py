from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields  ):
        if email is None:
            raise ValueError(_("email must be set"))
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    username = None 
    email = models.EmailField(verbose_name = "email" , unique = True  , blank = False , null = False)
    
    phone = PhoneNumberField(verbose_name = "phone" , blank = True , null = True) 
    avatar = ResizedImageField(size=[500 , 500 ], crop=['middle', 'center'], upload_to='avatars/', blank=True, null=True, 
                               verbose_name="avatar" , quality=90 , force_format='JPEG') 
    date_of_birth = models.DateField(verbose_name = "date of birth" , blank = True , null = True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f' {self.first_name} - {str(self.email)}'
    





    
class OTPCode(models.Model):
    class Meta:
        verbose_name = 'OTP code'
        verbose_name_plural = 'OTP code'
        
    email = models.EmailField()
    code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add = True)
    expire_at = models.DateTimeField()
    purpose = models.CharField(max_length=50, default='verification')
    
    def save(self , *args , **kwargs):
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(minutes=5)
        super().save(*args , **kwargs)
        
    def is_expired(self):
        return timezone.now() > self.expire_at
    
    def __str__(self):
        return f'{self.email} = {self.code}'