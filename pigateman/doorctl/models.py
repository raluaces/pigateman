from django.db import models

class accessKey(models.Model):
    key = models.CharField(max_length=30,primary_key=True)
    notify = models.BooleanField(default=False)
    uses = models.BigIntegerField(default=0)
    use_limit = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(null=True, blank=True, default=None)
    unlock_time = models.IntegerField(blank=True, default=7)
