from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=100, blank=True)
    favorite_animal = models.CharField(max_length=50, blank=True)
    favorite_hobby = models.CharField(max_length=50, blank=True)
    favorite_movie = models.CharField(max_length=50, blank=True)
    bio = models.TextField()
    avatar = models.ImageField(default='default.jpg',
                               upload_to='profile_pictures')

    def __str__(self):
        return f'{self.user.username} Profile'
