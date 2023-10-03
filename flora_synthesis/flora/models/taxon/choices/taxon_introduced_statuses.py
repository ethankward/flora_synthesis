from django.db import models


class IntroducedChoices(models.TextChoices):
    introduced = "i", "Introduced"
    native = "n", "Native"
    possibly_introduced = "p", "Possibly introduced"
