from django.db import models

class IndicadorBase(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])

    class Meta:
        abstract = True