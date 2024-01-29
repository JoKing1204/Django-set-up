from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

class UserItem(models.Model):
    user=models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()