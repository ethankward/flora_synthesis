from django.db import models


class IntroducedChoices(models.TextChoices):
    introduced = 'i', 'introduced'
    native = 'n', 'native'
    possibly_introduced = 'p', 'possibly introduced'
