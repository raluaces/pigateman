from django.db import models

class accessKey(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    notify = models.BooleanField(default=False)
    notify_email = models.CharField(max_length=30, blank=True, default='')
    uses = models.BigIntegerField(default=0)
    use_limit = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(null=True, blank=True, default=None)
    unlock_time = models.FloatField(blank=True, default=7.0)
    instruction_message = models.TextField(blank=True)
    internal_comment = models.TextField(blank=True)