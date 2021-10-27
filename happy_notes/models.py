from django.db import models

# Create your models here.
class Note (models.Model):
    sender = models.CharField(max_length=32, blank=True, default='')
    title = models.CharField(max_length=32)
    message = models.TextField()
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-uploaded",)