from django.db import models
from .base import IndicadorBase

class EstacoesMoveisIndicador(IndicadorBase):
    afectos_planos_pos_pagos = models.IntegerField()
    afectos_planos_pos_pagos_utilizacao = models.IntegerField()
    afectos_planos_pre_pagos = models.IntegerField()
    afectos_planos_pre_pagos_utilizacao = models.IntegerField()
    associados_situacoes_especificas = models.IntegerField(null=True, blank=True)
    outros_residuais = models.IntegerField(null=True, blank=True)
    
    # Serviços
    sms = models.IntegerField()
    mms = models.IntegerField(null=True, blank=True)
    mobile_tv = models.IntegerField(null=True, blank=True)
    roaming_internacional_out_parc_roaming_out = models.IntegerField()
    banda_larga_movel_3g_4g = models.IntegerField()
    utilizadores_5g_upgrades = models.IntegerField()
    utilizadores_servico_acesso_internet_banda_larga = models.IntegerField()
    utilizadores_placas_box = models.IntegerField()
    utilizadores_placas_usb = models.IntegerField()
    utilizadores_servico_4g = models.IntegerField()
    utilizadores_servico_banda_larga = models.IntegerField()
    utilizadores_placas_box_banda_larga = models.IntegerField()
    utilizadores_placas_usb_banda_larga = models.IntegerField()

    # Serviços de Mobile Money
    numero_utilizadores_mulher = models.IntegerField()
    numero_utilizadores_homem = models.IntegerField()
    total_carregamentos_mulher = models.DecimalField(max_digits=20, decimal_places=2)
    total_carregamentos_homem = models.DecimalField(max_digits=20, decimal_places=2)
    total_levantamentos_mulher = models.DecimalField(max_digits=20, decimal_places=2)
    total_levantamentos_homem = models.DecimalField(max_digits=20, decimal_places=2)
    total_transferencias_mulher = models.DecimalField(max_digits=20, decimal_places=2)
    total_transferencias_homem = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Estações Móveis e Mobile Money - {self.ano}/{self.mes}"

    class Meta:
        unique_together = ('ano', 'mes')

    @property
    def total_utilizadores(self):
        return self.numero_utilizadores_mulher + self.numero_utilizadores_homem

    @property
    def total_carregamentos(self):
        return self.total_carregamentos_mulher + self.total_carregamentos_homem

    @property
    def total_levantamentos(self):
        return self.total_levantamentos_mulher + self.total_levantamentos_homem

    @property
    def total_transferencias(self):
        return self.total_transferencias_mulher + self.total_transferencias_homem