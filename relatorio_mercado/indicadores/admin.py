from django.contrib import admin
from .models import Operadora, EstacoesMoveisEfetivas, EmpregoSetor, TrafegoNacional, QuotaMercado, TaxaPenetracao, VolumeNegocio

admin.site.register(Operadora)
admin.site.register(EstacoesMoveisEfetivas)
admin.site.register(EmpregoSetor)
admin.site.register(TrafegoNacional)
admin.site.register(QuotaMercado)
admin.site.register(TaxaPenetracao)
admin.site.register(VolumeNegocio)