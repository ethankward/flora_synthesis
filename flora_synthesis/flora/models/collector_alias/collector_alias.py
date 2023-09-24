from django.db import models


class CollectorAlias(models.Model):
    collector = models.ForeignKey("Collector", on_delete=models.CASCADE, related_name="collector_aliases")
    alias = models.TextField()

    class Meta:
        unique_together = [('alias',)]
