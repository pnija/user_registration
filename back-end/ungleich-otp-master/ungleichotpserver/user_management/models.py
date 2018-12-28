from django.db import models

# Create your models here.
class Users(models.Model):
    # user_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=500)