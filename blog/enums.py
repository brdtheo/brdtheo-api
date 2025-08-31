from django.db import models


class PostCategories(models.TextChoices):
    JAPAN = "JAPAN"
    FRANCE = "FRANCE"
    AUTOMOTIVE = "AUTOMOTIVE"
