from django.db import models


class ChecklistTypeChoices(models.TextChoices):
    INAT = "i", "iNaturalist"
    SEINET = "s", "SEINet"
    FLORA = "f", "Flora"
