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


def validate_phone_number(phonenumber):
    if re.search(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$',phonenumber) == None:
        raise ValidationError(
            _("%(value)s неверный формат номера телефона")
        )


class CUser(AbstractUser, models.Model):#<====================================
    UserSlug = models.SlugField(unique=True)
    MiddleName = models.CharField(max_length=50)
    TelephoneNumber = models.CharField(max_length=11, null=False, validators=[validate_phone_number])

    # following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False, blank=True)
    is_intermediary = models.BooleanField(default=False)
    Email = models.EmailField()
    Rating = models.FloatField(default=0.0)
    # Reviews = models.ForeignKey('Reviews', on_delete=models.SET_NULL, null=True)
    Description = models.CharField(max_length=250)
    Posts = models.ForeignKey('Posts', on_delete=models.SET_NULL, null=True)
    FromCountry = models.CharField(max_length=50, null=True)
    ImageIntermediares = models.ImageField(upload_to=f"{UserSlug}/Image/Avatar/", null=True)

    def __str__(self) -> str:
        return super().get_full_name()
    def save(self, *args, **kwargs) -> None:
        self.UserSlug = slugify(self.username)
        return super(CUser, self).save(self,*args, **kwargs)
    def get_absolute_url(self):
        return reverse(('intermediary_personal'), kwargs={'slug': self.UserSlug})


class Posts(models.Model):
    #User.objects.using("legacy_users").get(username="fred")
    posts_intermediary_id = models.ForeignKey(CUser, on_delete=models.CASCADE)
    text_post = models.TextField(max_length=1000, null=False)
    ImagePost = models.ImageField(upload_to=f"{posts_intermediary_id}/Post_Image/", null=True)
    # DatePost = models.DateTimeField(auto_now_add=True)
    # Like = models.IntegerField()

# class Reviews(models.Model):
#     ClientID = models.ForeignKey(CUser, on_delete=models.CASCADE)
#     Intermediares = models.ForeignKey(CUser, on_delete=models.CASCADE)
#     Review = models.TextField(max_length=200, null=False)
#     Image = models.ImageField(upload_to=f"{ClientID}/Review_Image/", null=True)


# class Clients(AbstractUser, models.Model):
#     MiddleName = models.CharField(max_length=50, null=False)
#     TelephoneNumber = models.CharField(max_length=11, null=False, validators=[validate_phone_number])
#     SlugClient = models.SlugField(unique=True)
#     # Subscriptions = models.ManyToManyField('Intermediares', related_name='followers', symmetrical=False, blank=True)
    
#     def __str__(self) -> str:
#         return super().get_full_name()
#     def save(self, *args, **kwargs) -> None:
#         self.SlugClient = slugify(self.username)
#         return super(Clients, self).save(self,*args, **kwargs)
#     def get_absolute_url(self):
#         return reverse('test_startapp', kwargs={'client_slug': self.SlugClient})
    
# class Intermediares(Clients, models.Model):
#     # Intermed = models.OneToOneField(User, on_delete=models.CASCADE)
#     SlugIntermediary = models.SlugField(unique=True)
#     Name = models.CharField(max_length=50, null=False, unique=True)
#     Rating = models.FloatField(default=0.0)
#     Reviews = models.ForeignKey(Reviews, on_delete=models.SET_NULL, null=True)
#     Email = models.EmailField(null=False)
#     Description = models.CharField(max_length=250, null=False)
#     Posts = models.ForeignKey('Posts', on_delete=models.SET_NULL, null=True)
#     # FromCountry = models.CharField(max_length=50, null=True)
#     # ImageIntermediares = models.ImageField(upload_to=f"{Name}/Image/Avatar/", null=True)
#     def get_absolute_url(self):
#         return reverse('test_startapp', kwargs={'slug': self.SlugIntermediary})
    
#     def save(self, *args, **kwargs) -> None:
#         self.SlugIntermediary = slugify(self.Name)
#         return super(Intermediares, self).save(self, *args, **kwargs)

#     def __str__(self) -> str:
#         return self.Name
    '''
    Пример использования другой бд
    using = 'other'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
    '''