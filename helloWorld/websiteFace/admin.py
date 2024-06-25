from django.contrib import admin

from .models import VideoStorage
from .models import ResultStorage

admin.site.register(VideoStorage)
admin.site.register(ResultStorage)

# Register your models here.
