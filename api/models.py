import uuid

from django.db import models


class Vps(models.Model):

    STATUS_CHOICES = (
        ('started', 'started'),
        ('blocked', 'blocked'),
        ('stopped', 'stopped')
    )

    cpu_cores = models.IntegerField()
    ram = models.IntegerField()
    hdd = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return 'Vps - ' + self.status

    class Meta:
        verbose_name_plural = 'Vps'
