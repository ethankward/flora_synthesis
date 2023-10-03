from django.db import models

from flora.models.base_model import BaseModel


class Collector(BaseModel):
    name = models.TextField()
    external_url = models.URLField(blank=True, null=True, max_length=1024)

    first_collection_year = models.IntegerField(blank=True, null=True)
    last_collection_year = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = [("name",)]

    def __str__(self):
        return self.name
