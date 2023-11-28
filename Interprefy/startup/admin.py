from django.contrib import admin
from .models import (
    CUser,
    Categories,
    Products,
    Posts,
)
# Register your models here.
admin.site.register(CUser)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Posts)