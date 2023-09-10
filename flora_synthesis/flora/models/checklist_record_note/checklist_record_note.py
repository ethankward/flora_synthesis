from django.db import models
from django.utils import timezone


class ChecklistRecordNote(models.Model):
    note = models.TextField()
    added_on = models.DateTimeField(default=timezone.now)
