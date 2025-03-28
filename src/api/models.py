from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class StructureType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Structure(models.Model):
    type = models.ForeignKey(StructureType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    

class Need(models.Model):
    description = models.CharField(max_length=255)
    

class Situation(models.Model):
    description = models.CharField(max_length=255)


class Town(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Street(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Recipient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthyear = models.IntegerField()
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    need = models.ForeignKey(Need, on_delete=models.SET_NULL, null=True, blank=True)
    situation = models.ForeignKey(Situation, on_delete=models.SET_NULL, null=True, blank=True)


class Workshop(models.Model):
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    hour = models.TimeField()
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    workshop_date = models.DateTimeField()


class Cheque(models.Model):
    number = models.IntegerField(unique=True)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    distribution_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, blank=True)


# User___

class Role(models.Model):
    ADMIN = 'admin'
    DISTRIBUTOR = 'distributor'
    RECEPTOR = 'receptor'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (DISTRIBUTOR, 'Distributor'),
        (RECEPTOR, 'Receptor'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError('Le champ Username est obligatoire')
        if not isinstance(role, Role):
            role = Role.objects.get(id=role) if isinstance(role, int) else Role.objects.get(name=role)
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.objects.get(name='admin'))
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Agent(AbstractBaseUser, PermissionsMixin):  
    username = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='agents')
    structure = models.ForeignKey('Structure', on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions',blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']
    objects = CustomUserManager()
    def __str__(self):
        return self.username

class DownloadFile(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name