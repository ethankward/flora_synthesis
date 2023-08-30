from django.db import models


class EndemicChoices(models.TextChoices):
    n = "n", "Not endemic"
    u = "u", "In the US only in Rincons but also occurs outside of the US"
    z = "z", "In Arizona only found in Rincons but also occurs outside of Arizona"
    a = "a", "Only found in Arizona"
    r = "r", "Only found in Rincons"
