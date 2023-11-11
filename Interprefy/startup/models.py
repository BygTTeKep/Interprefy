from django.db import models

# Create your models here.
from collections.abc import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
import re
from django.utils.text import slugify
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib import messages

class Clients(AbstractUser, models.Model):
    MiddleName = models.CharField(max_length=50, null=False)
    TelephoneNumber = models.CharField(max_length=11, null=False)
    SlugClient = models.SlugField(unique=True)
    # Subscriptions = models.ManyToManyField('Intermediares', related_name='followers', symmetrical=False, blank=True)
    
    def __str__(self) -> str:
        return super().get_full_name()
    def save(self, *args, **kwargs) -> None:
        self.SlugClient = slugify(self.username)
        return super(Clients, self).save(self,*args, **kwargs)
    def get_absolute_url(self):
        return reverse('test_startapp', kwargs={'client_slug': self.SlugClient})
    


class Reviews(models.Model):
    ClientID = models.ForeignKey(Clients, on_delete=models.CASCADE)
    Intermediares = models.ForeignKey('Intermediares', on_delete=models.CASCADE)
    Review = models.TextField(max_length=200, null=False)
    Image = models.ImageField(upload_to=f"{ClientID}/Review_Image/", null=True)

class Intermediares(models.Model):
    SlugIntermediary = models.SlugField(unique=True)
    Name = models.CharField(max_length=50, null=False, unique=True)
    Rating = models.FloatField(default=0.0)
    Reviews = models.ForeignKey(Reviews, on_delete=models.SET_NULL, null=True)
    Email = models.EmailField(null=False)
    Description = models.CharField(max_length=250, null=False)
    Posts = models.ForeignKey('Posts', on_delete=models.SET_NULL, null=True)
    FromCountry = models.CharField(max_length=50, null=True)
    # ImageIntermediares = models.ImageField(upload_to=f"{Name}/Image/Avatar/", null=True)

    def get_absolute_url(self):
        return reverse('test_startapp', kwargs={'client_slug': self.SlugIntermediary})
    
    def save(self, *args, **kwargs) -> None:
        self.SlugIntermediary = slugify(self.Name)
        return super(Intermediares, self).save(self, *args, **kwargs)

    def __str__(self) -> str:
        return self.Name
    
class Subscription(models.Model):
    Subscribe_client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    Subscribe_intermediary_id = models.ForeignKey(Intermediares, on_delete=models.CASCADE)

class Posts(models.Model):
    #User.objects.using("legacy_users").get(username="fred")
    posts_intermediary_id = models.ForeignKey(Intermediares, on_delete=models.CASCADE)
    text_post = models.TextField(max_length=1000, null=False)
    ImagePost = models.ImageField(upload_to=f"{posts_intermediary_id}/Post_Image/", null=True)
    DatePost = models.DateTimeField(auto_now_add=True)
    # Like = models.IntegerField()