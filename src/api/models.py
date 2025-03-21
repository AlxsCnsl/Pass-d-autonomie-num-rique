from django.db import models

class StructureType(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Structure(models.Model):
    type = models.ForeignKey(StructureType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
class Need(models.Model):
    description = models.CharField(max_length=255)
    
class Situation(models.Model):
    description = models.CharField(max_length=255)

class Town(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Street(models.Model):
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
    user = models.ForeignKey(Recipient, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    distribution_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, blank=True)

class Agent(models.Model):
    username = models.CharField(max_length=255)
    password = None
    Role = None
    Structure = None
