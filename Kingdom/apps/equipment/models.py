from django.db import models


class ArmorType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    type = models.ForeignKey(ArmorType, related_name='armor_type', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    weight = models.DecimalField(max_digits=7, decimal_places=2, default=0.01)
    armor_class = models.IntegerField(null=True, blank=True)
    attack_bonus = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
