from django.db import models


class MoralIntentions(models.Model):
    name = models.CharField(max_length=100)
