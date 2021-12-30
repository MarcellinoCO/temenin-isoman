from django.db import models

# Create your models here.
class TipsAndTrick(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=500)
    published_date = models.DateField()
    brief_description = models.TextField()
    image_url =  models.CharField(max_length=500)
    article_url = models.CharField(max_length=500)