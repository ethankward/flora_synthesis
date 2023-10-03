from django.db import models
from django.utils import timezone

from flora.models.base_model import BaseModel


class ChecklistRecordNote(BaseModel):
    note = models.TextField()
    added_on = models.DateTimeField(default=timezone.now)
