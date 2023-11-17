from django.db import models


class Armor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        abstract = True


class Helmet(Armor):
    pass


class PlateArmor(Armor):
    pass


class FirstWeapon(Armor):
    pass


class SecondWeapon(Armor):
    pass


class FirstRing(Armor):
    pass


class SecondRing(Armor):
    pass


class Amulet(Armor):
    pass


class Gloves(Armor):
    pass


class FirstBracer(Armor):
    pass


class SecondBracer(Armor):
    pass


class Boots(Armor):
    pass
