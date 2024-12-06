from django.db import models
from django.db.models import Sum

class DadosAnuais(models.Model):
    OPERADORAS = [
        ('MTN', 'MTN'),
        ('ORANGE', 'Orange')
    ]
    
    ano = models.IntegerField()
    operadora = models.CharField(max_length=10, choices=OPERADORAS)

    # 1. Assinantes rede móvel
    assinantes_rede_movel = models.IntegerField(null=True, blank=True)
    assinantes_pos_pago = models.IntegerField(null=True, blank=True)
    assinantes_pre_pago = models.IntegerField(null=True, blank=True)
    utilizacao_efetiva = models.IntegerField(null=True, blank=True)

    # 2. Assinantes Banda Larga Móvel
    assinantes_banda_larga_movel = models.IntegerField(null=True, blank=True)
    assinantes_3g = models.IntegerField(null=True, blank=True)
    assinantes_3g_box = models.IntegerField(null=True, blank=True)
    assinantes_3g_usb = models.IntegerField(null=True, blank=True)
    assinantes_4g = models.IntegerField(null=True, blank=True)
    assinantes_4g_box = models.IntegerField(null=True, blank=True)
    assinantes_4g_usb = models.IntegerField(null=True, blank=True)

    # 3. Assinantes Internet Banda Larga Fixa via Rádio
    assinantes_banda_larga_fixa = models.IntegerField(null=True, blank=True)
    banda_larga_256kbps = models.IntegerField(null=True, blank=True)
    banda_larga_256k_2m = models.IntegerField(null=True, blank=True)
    banda_larga_2m_4m = models.IntegerField(null=True, blank=True)
    banda_larga_5m_10m = models.IntegerField(null=True, blank=True)
    banda_larga_10m = models.IntegerField(null=True, blank=True)
    banda_larga_outros = models.IntegerField(null=True, blank=True)

    # 4. Volume de Negócio
    volume_negocio = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    # 5. Investimentos no setor
    investimentos = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    # 6. Volume Tráfego em min. de comum. Originada(saída)
    trafego_voz_originado = models.BigIntegerField(null=True, blank=True)
    trafego_voz_on_net = models.BigIntegerField(null=True, blank=True)
    trafego_voz_off_net = models.BigIntegerField(null=True, blank=True)
    trafego_voz_numeros_curtos = models.BigIntegerField(null=True, blank=True)
    trafego_voz_internacional = models.BigIntegerField(null=True, blank=True)

    # 7. SMS
    trafego_sms = models.BigIntegerField(null=True, blank=True)
    trafego_sms_on_net = models.BigIntegerField(null=True, blank=True)
    trafego_sms_off_net = models.BigIntegerField(null=True, blank=True)
    trafego_sms_internacional = models.BigIntegerField(null=True, blank=True)

    # 8. Dados tráfego
    trafego_dados = models.BigIntegerField(null=True, blank=True)
    trafego_dados_2g = models.BigIntegerField(null=True, blank=True)
    trafego_dados_3g = models.BigIntegerField(null=True, blank=True)
    trafego_dados_3g_box = models.BigIntegerField(null=True, blank=True)
    trafego_dados_3g_usb = models.BigIntegerField(null=True, blank=True)
    trafego_dados_4g = models.BigIntegerField(null=True, blank=True)
    trafego_dados_4g_box = models.BigIntegerField(null=True, blank=True)
    trafego_dados_4g_usb = models.BigIntegerField(null=True, blank=True)

    # 9. Nº de comunicação de voz
    chamadas_originadas = models.BigIntegerField(null=True, blank=True)
    chamadas_originadas_on_net = models.BigIntegerField(null=True, blank=True)
    chamadas_originadas_off_net = models.BigIntegerField(null=True, blank=True)
    chamadas_originadas_numeros_curtos = models.BigIntegerField(null=True, blank=True)
    chamadas_originadas_internacional = models.BigIntegerField(null=True, blank=True)

    # 10. Volume Tráfego em min. de comum. Terminada(entrada)
    trafego_voz_terminado = models.BigIntegerField(null=True, blank=True)
    trafego_voz_terminado_off_net = models.BigIntegerField(null=True, blank=True)
    trafego_voz_terminado_internacional = models.BigIntegerField(null=True, blank=True)

    # 11. SMS terminado
    trafego_sms_terminado = models.BigIntegerField(null=True, blank=True)
    trafego_sms_terminado_off_net = models.BigIntegerField(null=True, blank=True)
    trafego_sms_terminado_internacional = models.BigIntegerField(null=True, blank=True)

    # 12. Nº Chamadas terminada(entrada)
    chamadas_terminadas = models.BigIntegerField(null=True, blank=True)
    chamadas_terminadas_off_net = models.BigIntegerField(null=True, blank=True)
    chamadas_terminadas_internacional = models.BigIntegerField(null=True, blank=True)

    # 13. Tráfego de roaming internacional
    roaming_in_minutos = models.IntegerField(null=True, blank=True)
    roaming_out_minutos = models.IntegerField(null=True, blank=True)
    roaming_in_chamadas = models.IntegerField(null=True, blank=True)
    roaming_out_chamadas = models.IntegerField(null=True, blank=True)

    # 14. Volume de acesso à Internet dentro do país (Mbit)
    volume_internet_nacional = models.BigIntegerField(null=True, blank=True)

    # 15. Volume de acesso à Internet fora do país (Mbit)
    volume_internet_internacional = models.BigIntegerField(null=True, blank=True)

    # 16. Tráfego SMS roaming
    trafego_sms_roaming_in = models.IntegerField(null=True, blank=True)
    trafego_sms_roaming_out = models.IntegerField(null=True, blank=True)

    # 17. Receita
    receita_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_servicos_voz = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_roaming_out = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_servicos_mensagens = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_dados_moveis = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_originadas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_on_net = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_off_net = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_internacional = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_terminadas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_terminadas_off_net = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_chamadas_terminadas_internacional = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    receita_mobile_money = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    # 18. Banda Larga Internacional (BLI)
    banda_larga_internacional = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    # 19. Emprego
    emprego_total = models.IntegerField(null=True, blank=True)
    emprego_homens = models.IntegerField(null=True, blank=True)
    emprego_mulheres = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.operadora} - {self.ano}"

    class Meta:
        verbose_name = "Dados Anuais"
        verbose_name_plural = "Dados Anuais"
        unique_together = ('ano', 'operadora')
        ordering = ['-ano', 'operadora']

    def __str__(self):
        return f"{self.operadora} - {self.ano}"

    @property
    def market_share_assinantes(self):
        total = DadosAnuais.objects.filter(ano=self.ano, operadora='TOTAL').first()
        if total and total.assinantes_rede_movel:
            return (self.assinantes_rede_movel / total.assinantes_rede_movel) * 100
        return 0

    @property
    def market_share_receita(self):
        total = DadosAnuais.objects.filter(ano=self.ano, operadora='TOTAL').first()
        if total and total.receita_total:
            return (self.receita_total / total.receita_total) * 100
        return 0

    def calcular_crescimento(self, campo):
        ano_anterior = self.ano - 1
        dados_anterior = DadosAnuais.objects.filter(ano=ano_anterior, operadora=self.operadora).first()
        if dados_anterior:
            valor_anterior = getattr(dados_anterior, campo)
            valor_atual = getattr(self, campo)
            if valor_anterior and valor_atual:
                return ((valor_atual - valor_anterior) / valor_anterior) * 100
        return 0

    @classmethod
    def get_total_mercado(cls, ano):
        """
        Calcula os totais de mercado somando os dados de todas as operadoras para o ano especificado.
        """
        totais = cls.objects.filter(ano=ano).aggregate(
            assinantes_rede_movel=Sum('assinantes_rede_movel'),
            receita_total=Sum('receita_total'),
            trafego_dados=Sum('trafego_dados'),
            investimentos=Sum('investimentos')
        )
        return totais


    @classmethod
    def get_operadoras(cls, ano):
        return cls.objects.filter(ano=ano).exclude(operadora='TOTAL')

    @classmethod
    def get_anos_disponiveis(cls):
        return cls.objects.values_list('ano', flat=True).distinct().order_by('ano')

    @property
    def arpu(self):
        if self.assinantes_rede_movel:
            return self.receita_total / self.assinantes_rede_movel
        return 0

    @property
    def market_concentration(self):
        total = DadosAnuais.objects.filter(ano=self.ano, operadora='TOTAL').first()
        if total and total.assinantes_rede_movel:
            hhi = sum((op.assinantes_rede_movel / total.assinantes_rede_movel * 100) ** 2 
                      for op in DadosAnuais.objects.filter(ano=self.ano).exclude(operadora='TOTAL'))
            return hhi
        return 0
