from django.db import models

# Create your models here.

class Post(models.Model):  
    text = models.TextField()
    img = models.ImageField(upload_to='image/', blank=True, null=True, default=None)
    def __str__(self):  
        return self.text[:50]