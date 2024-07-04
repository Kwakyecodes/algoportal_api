from django.db import models

class Records(models.Model):
    call = models.CharField(max_length=100, null=False)
    query = models.CharField(max_length=500, null=False)
    status = models.CharField(max_length=100, null=False)
    reason = models.CharField(max_length=100, null=False) 
    time = models.CharField(max_length=120, null=True)