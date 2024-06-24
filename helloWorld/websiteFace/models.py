from django.db import models

class VideoStorage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    vid_name = models.CharField(max_length=100)
    vid_sec_length = models.BigIntegerField()
    vid_key = models.CharField(max_length=11, null=True)
    vid_extracted = models.TextField(null=True, blank=True)



# Create your models here.
