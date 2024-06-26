from django.contrib import admin

from .webFuncts import models

admin.site.register(models.VideoStorage)
admin.site.register(models.ResultStorage)

# Register your models here.
