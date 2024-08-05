from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# from evaluation.models import Departement



class Departement(models.Model):
    nomDepartement  = models.CharField(max_length=128, default="", blank=True)  

    def __str__(self):
        return self.nomDepartement


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    number_phone = models.CharField(max_length=128, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True) 
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
    note = models.IntegerField(default=0, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE,
                                     blank=True, related_name='departement2', default= 1)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_technician = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


