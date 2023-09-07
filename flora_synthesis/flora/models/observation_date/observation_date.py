from django.db import models


class ObservationDate(models.Model):
    date = models.DateField()
    url = models.URLField(blank=True, null=True)
