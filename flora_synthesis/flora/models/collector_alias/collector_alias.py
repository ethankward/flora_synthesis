from django.db import models

from flora.models.base_model import BaseModel


class CollectorAlias(BaseModel):
    collector = models.ForeignKey(
        "Collector", on_delete=models.CASCADE, related_name="collector_aliases"
    )
    alias = models.TextField()

    class Meta:
        unique_together = [("alias",)]
