from django.db import models


class InatObservationTypeChoices(models.TextChoices):
    RESEARCH = 'R', 'Research grade'
    NEEDS_ID = 'N', 'Needs ID'
    CASUAL = 'C', 'Casual'
    UNKNOWN = 'U', 'Unknown'
