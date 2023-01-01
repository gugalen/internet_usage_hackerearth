from django.db import models


class UsageData(models.Model):
    username = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    usage_time = models.DurationField()
    upload = models.DecimalField(max_digits=12, decimal_places=2)
    download = models.DecimalField(max_digits=12, decimal_places=2)

