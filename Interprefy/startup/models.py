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
from django.utils import timezone
import os


def validate_phone_number(phonenumber):
    if re.search(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',phonenumber) == None:
        raise ValidationError(
            _("%(value)s неверный формат номера телефона")
        )

def get_path_upload_image(user, file):
    """
    make path of uploaded file shorter and return it
    in following format: (media)/profile_pics/user_1/myphoto_2018-12-2.png
    """
    time = timezone.now().strftime("%Y-%m-%d")
    end_extention = file.split(".")[-1]
    head = file.split(".")[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + "_" + time + "." + end_extention
    return os.path.join("user_{0}_{1}").format(user, file_name)



class CUser(AbstractUser, models.Model):
    UserSlug = models.SlugField(unique=True)
    MiddleName = models.CharField(max_length=50)
    TelephoneNumber = models.CharField(max_length=11, null=False, validators=[validate_phone_number])
    # following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False, blank=True)
    is_intermediary = models.BooleanField(default=False)
    Email = models.EmailField()
    Rating = models.FloatField(default=0.0)
    Description = models.CharField(max_length=250)
    FromCountry = models.CharField(max_length=50, null=True)
    ImageIntermediares = models.ImageField(upload_to=f"Image/Avatar/", null=True)
    def save(self, *args, **kwargs):
        if self.ImageIntermediares:
            self.ImageIntermediares.name = get_path_upload_image(
                self.username, self.ImageIntermediares.name
            )
        self.UserSlug = slugify(self.username)
        return super(CUser, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse(('intermediary_personal'), kwargs={'slug': self.UserSlug})

class Categories(models.Model):
    CategoryName = models.CharField(max_length=50)


class Products(models.Model):
    IntermediaryID = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name='intermediares')
    CategoryID = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    Name = models.CharField(max_length=100)
    ImageProducts = models.ImageField(upload_to=f'Image/Products/', null=True)
    Price = models.DecimalField(decimal_places=2, max_digits=6)
    UnitsInStock = models.IntegerField()
    def save(self, *args, **kwargs) -> None:
        if self.ImageProducts:
            self.ImageProducts.name = get_path_upload_image(
                self.IntermediaryID.username, self.ImageProducts.name
            )
        return super().save(*args,**kwargs)


class Posts(models.Model):
    #User.objects.using("legacy_users").get(username="fred")
    posts_intermediary_id = models.ForeignKey(CUser, on_delete=models.CASCADE)
    text_post = models.TextField(max_length=1000, null=False)
    ImagePost = models.ImageField(upload_to=f"{posts_intermediary_id}/Post_Image/", null=True)
    # DatePost = models.DateTimeField(auto_now_add=True)
    # Like = models.IntegerField()
