from django.db import models


class SEINETObservationTypeChoices(models.TextChoices):
    COLLECTION = 'C', 'Collection'
    GENERAL_RESEARCH = 'G', 'General Research'
    NOTE_PLACEHOLDER = 'P', 'Placeholder note'
