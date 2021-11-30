from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE 
from users.models import NewUser 

# Create your models here.
class User(models.Model):
    name = models.ForeignKey(NewUser, on_delete=models.CASCADE) 
 
