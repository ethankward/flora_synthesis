from django.db import models


class FloraObservationTypeChoices(models.TextChoices):
    PRESENT = "P", "Present"
    MISSING = "M", "Missing"
    SUSPECTED = "S", "Suspected"
    UNKNOWN = "U", "Unknown"
