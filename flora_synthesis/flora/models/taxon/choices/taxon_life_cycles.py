from django.db import models


class LifeCycleChoices(models.TextChoices):
    a = 'a', 'Annual'
    p = 'p', 'Perennial'
    b = 'b', 'Biennial'
    u = 'u', 'Unknown'
