from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Door(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    gpio_port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(28)])

    def __str__(self):
        return self.name


class accessKey(models.Model):
    key = models.CharField(max_length=30)
    notify = models.BooleanField(default=False)
    notify_email = models.CharField(max_length=30, blank=True, default='')
    uses = models.BigIntegerField(default=0)
    use_limit = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(null=True, blank=True, default=None)
    unlock_time = models.FloatField(blank=True, default=7.0)
    instruction_message = models.TextField(blank=True)
    internal_comment = models.TextField(blank=True)
    door = models.ForeignKey(Door, on_delete=models.CASCADE)

    def __str__(self):
        return self.key

