from django.db import models

# Create your models here.
from django.db import models

class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return self.filename

