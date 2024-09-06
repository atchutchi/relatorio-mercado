from django.db import models

class DadosAnuais(models.Model):
    OPERADORAS = [
        ('MTN', 'MTN'),
        ('ORANGE', 'Orange'),
        ('TOTAL', 'Total')
    ]
    
    ano = models.IntegerField()
    operadora = models.CharField(max_length=10, choices=OPERADORAS)

    # 1. Assinantes rede móvel
    assinantes_rede_movel = models.IntegerField()
    assinantes_pos_pago = models.IntegerField()
    assinantes_pre_pago = models.IntegerField()
    utilizacao_efetiva = models.IntegerField()

    # 2. Assinantes Banda Larga Móvel
    assinantes_banda_larga_movel = models.IntegerField()
    assinantes_3g = models.IntegerField()
    assinantes_3g_box = models.IntegerField()
    assinantes_3g_usb = models.IntegerField()
    assinantes_4g = models.IntegerField()
    assinantes_4g_box = models.IntegerField()
    assinantes_4g_usb = models.IntegerField()

    # 3. Assinantes Internet Banda Larga Fixa via Rádio
    assinantes_banda_larga_fixa = models.IntegerField()
    banda_larga_256kbps = models.IntegerField()
    banda_larga_256k_2m = models.IntegerField()
    banda_larga_2m_4m = models.IntegerField()
    banda_larga_5m_10m = models.IntegerField()
    banda_larga_10m = models.IntegerField()
    banda_larga_outros = models.IntegerField()

    # 4. Volume de Negócio
    volume_negocio = models.DecimalField(max_digits=20, decimal_places=2)

    # 5. Investimentos no setor
    investimentos = models.DecimalField(max_digits=20, decimal_places=2)

    # 6. Volume Tráfego em min. de comum. Originada(saída)
    trafego_voz_originado = models.BigIntegerField()
    trafego_voz_on_net = models.BigIntegerField()
    trafego_voz_off_net = models.BigIntegerField()
    trafego_voz_numeros_curtos = models.BigIntegerField()
    trafego_voz_internacional = models.BigIntegerField()

    # 7. SMS
    trafego_sms = models.BigIntegerField()
    trafego_sms_on_net = models.BigIntegerField()
    trafego_sms_off_net = models.BigIntegerField()
    trafego_sms_internacional = models.BigIntegerField()

    # 8. Dados tráfego
    trafego_dados = models.BigIntegerField()
    trafego_dados_2g = models.BigIntegerField()
    trafego_dados_3g = models.BigIntegerField()
    trafego_dados_3g_box = models.BigIntegerField()
    trafego_dados_3g_usb = models.BigIntegerField()
    trafego_dados_4g = models.BigIntegerField()
    trafego_dados_4g_box = models.BigIntegerField()
    trafego_dados_4g_usb = models.BigIntegerField()

    # 9. Nº de comunicação de voz
    chamadas_originadas = models.BigIntegerField()
    chamadas_originadas_on_net = models.BigIntegerField()
    chamadas_originadas_off_net = models.BigIntegerField()
    chamadas_originadas_numeros_curtos = models.BigIntegerField()
    chamadas_originadas_internacional = models.BigIntegerField()

    # 10. Volume Tráfego em min. de comum. Terminada(entrada)
    trafego_voz_terminado = models.BigIntegerField()
    trafego_voz_terminado_off_net = models.BigIntegerField()
    trafego_voz_terminado_internacional = models.BigIntegerField()

    # 11. SMS terminado
    trafego_sms_terminado = models.BigIntegerField()
    trafego_sms_terminado_off_net = models.BigIntegerField()
    trafego_sms_terminado_internacional = models.BigIntegerField()

    # 12. Nº Chamadas terminada(entrada)
    chamadas_terminadas = models.BigIntegerField()
    chamadas_terminadas_off_net = models.BigIntegerField()
    chamadas_terminadas_internacional = models.BigIntegerField()

    # 13. Tráfego de roaming internacional
    roaming_in_minutos = models.IntegerField()
    roaming_out_minutos = models.IntegerField()
    roaming_in_chamadas = models.IntegerField()
    roaming_out_chamadas = models.IntegerField()

    # 14. Volume de acesso à Internet dentro do país (Mbit)
    volume_internet_nacional = models.BigIntegerField()

    # 15. Volume de acesso à Internet fora do país (Mbit)
    volume_internet_internacional = models.BigIntegerField()

    # 16. Tráfego SMS roaming
    trafego_sms_roaming_in = models.IntegerField()
    trafego_sms_roaming_out = models.IntegerField()

    # 17. Receita
    receita_total = models.DecimalField(max_digits=20, decimal_places=2)
    receita_servicos_voz = models.DecimalField(max_digits=20, decimal_places=2)
    receita_roaming_out = models.DecimalField(max_digits=20, decimal_places=2)
    receita_servicos_mensagens = models.DecimalField(max_digits=20, decimal_places=2)
    receita_dados_moveis = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_originadas = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_on_net = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_off_net = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_internacional = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_terminadas = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_terminadas_off_net = models.DecimalField(max_digits=20, decimal_places=2)
    receita_chamadas_terminadas_internacional = models.DecimalField(max_digits=20, decimal_places=2)
    receita_mobile_money = models.DecimalField(max_digits=20, decimal_places=2)

    # 18. Banda Larga Internacional (BLI)
    banda_larga_internacional = models.DecimalField(max_digits=20, decimal_places=2)

    # 19. Emprego
    emprego_total = models.IntegerField()
    emprego_homens = models.IntegerField()
    emprego_mulheres = models.IntegerField()

    def __str__(self):
        return f"{self.operadora} - {self.ano}"

    class Meta:
        verbose_name = "Dados Anuais"
        verbose_name_plural = "Dados Anuais"
        unique_together = ('ano', 'operadora')
        ordering = ['-ano', 'operadora']