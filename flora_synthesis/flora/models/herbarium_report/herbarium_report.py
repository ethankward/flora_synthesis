from django.db import models

from flora.models import base_model


class HerbariumReport(base_model.BaseModel):
    taxon = models.TextField()
    url = models.URLField()
