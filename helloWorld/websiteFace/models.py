from django.db import models

class VideoStorage(models.Model):
    vid_name = models.CharField(max_length=100)
    vid_sec_length = models.BigIntegerField()
    vid_key = models.CharField(max_length=11, null=True)
    vid_extracted = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.vid_name
    




# Create your models here.
