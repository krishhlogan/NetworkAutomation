from django.db import models
from django.utils.timezone import now


# Create your models here


class DeviceConfigurationLogs(models.Model):
    TYPES = [('ADD', 'ADD'), ('REMOVE', 'REMOVE')]
    device = models.SlugField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPES)
    message = models.TextField()
    success = models.BooleanField()
    meta_data = models.TextField(default="{}")
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return self.device
