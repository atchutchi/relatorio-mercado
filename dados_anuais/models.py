from django.db import models
from django.db.models import Sum, F, Value, Case, When, FloatField
from django.db.models.functions import Cast
from decimal import Decimal, ROUND_HALF_UP

class Operadora(models.Model):
    """Representa uma operadora de telecomunicações."""
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Operadora"
        verbose_name_plural = "Operadoras"
        ordering = ['nome']

class DadosAnuais(models.Model):
    """Armazena dados estatísticos anuais por operadora."""
    ano = models.IntegerField(db_index=True)
    operadora = models.ForeignKey(Operadora, on_delete=models.PROTECT, related_name='dados_anuais')

    # Campos numéricos agora usam default=0 ou default=Decimal('0.0')
    # em vez de null=True, blank=True, assumindo que ausência de dado significa zero.
    # Avalie se 'null=True' é realmente necessário para algum campo específico
    # onde 'None' tem um significado distinto de 0.

    # 1. Assinantes rede móvel
    assinantes_rede_movel = models.IntegerField(default=0)
    assinantes_pos_pago = models.IntegerField(default=0)
    assinantes_pre_pago = models.IntegerField(default=0)
    utilizacao_efetiva = models.IntegerField(default=0)

    # 2. Assinantes Banda Larga Móvel
    assinantes_banda_larga_movel = models.IntegerField(default=0)
    assinantes_3g = models.IntegerField(default=0)
    assinantes_3g_box = models.IntegerField(default=0)
    assinantes_3g_usb = models.IntegerField(default=0)
    assinantes_4g = models.IntegerField(default=0)
    assinantes_4g_box = models.IntegerField(default=0)
    assinantes_4g_usb = models.IntegerField(default=0)

    # 3. Assinantes Internet Banda Larga Fixa via Rádio
    assinantes_banda_larga_fixa = models.IntegerField(default=0)
    banda_larga_256kbps = models.IntegerField(default=0)
    banda_larga_256k_2m = models.IntegerField(default=0)
    banda_larga_2m_4m = models.IntegerField(default=0)
    banda_larga_5m_10m = models.IntegerField(default=0)
    banda_larga_10m = models.IntegerField(default=0)
    banda_larga_outros = models.IntegerField(default=0)

    # 4. Volume de Negócio
    volume_negocio = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))

    # 5. Investimentos no setor
    investimentos = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))

    # 6. Volume Tráfego em min. de comum. Originada(saída)
    trafego_voz_originado = models.BigIntegerField(default=0)
    trafego_voz_on_net = models.BigIntegerField(default=0)
    trafego_voz_off_net = models.BigIntegerField(default=0)
    trafego_voz_numeros_curtos = models.BigIntegerField(default=0)
    trafego_voz_internacional = models.BigIntegerField(default=0)

    # 7. SMS
    trafego_sms = models.BigIntegerField(default=0)
    trafego_sms_on_net = models.BigIntegerField(default=0)
    trafego_sms_off_net = models.BigIntegerField(default=0)
    trafego_sms_internacional = models.BigIntegerField(default=0)

    # 8. Dados tráfego (Assumindo que a unidade é consistente, e.g., Megabytes ou Gigabytes)
    trafego_dados = models.BigIntegerField(default=0) # Unidade? MB? GB?
    trafego_dados_2g = models.BigIntegerField(default=0)
    trafego_dados_3g = models.BigIntegerField(default=0)
    trafego_dados_3g_box = models.BigIntegerField(default=0)
    trafego_dados_3g_usb = models.BigIntegerField(default=0)
    trafego_dados_4g = models.BigIntegerField(default=0)
    trafego_dados_4g_box = models.BigIntegerField(default=0)
    trafego_dados_4g_usb = models.BigIntegerField(default=0)

    # 9. Nº de comunicação de voz
    chamadas_originadas = models.BigIntegerField(default=0)
    chamadas_originadas_on_net = models.BigIntegerField(default=0)
    chamadas_originadas_off_net = models.BigIntegerField(default=0)
    chamadas_originadas_numeros_curtos = models.BigIntegerField(default=0)
    chamadas_originadas_internacional = models.BigIntegerField(default=0)

    # 10. Volume Tráfego em min. de comum. Terminada(entrada)
    trafego_voz_terminado = models.BigIntegerField(default=0)
    trafego_voz_terminado_off_net = models.BigIntegerField(default=0)
    trafego_voz_terminado_internacional = models.BigIntegerField(default=0)

    # 11. SMS terminado
    trafego_sms_terminado = models.BigIntegerField(default=0)
    trafego_sms_terminado_off_net = models.BigIntegerField(default=0)
    trafego_sms_terminado_internacional = models.BigIntegerField(default=0)

    # 12. Nº Chamadas terminada(entrada)
    chamadas_terminadas = models.BigIntegerField(default=0)
    chamadas_terminadas_off_net = models.BigIntegerField(default=0)
    chamadas_terminadas_internacional = models.BigIntegerField(default=0)

    # 13. Tráfego de roaming internacional
    roaming_in_minutos = models.IntegerField(default=0)
    roaming_out_minutos = models.IntegerField(default=0)
    roaming_in_chamadas = models.IntegerField(default=0)
    roaming_out_chamadas = models.IntegerField(default=0)

    # 14. Volume de acesso à Internet dentro do país (Unidade?)
    volume_internet_nacional = models.BigIntegerField(default=0) # Mbit? MB? GB?

    # 15. Volume de acesso à Internet fora do país (Unidade?)
    volume_internet_internacional = models.BigIntegerField(default=0) # Mbit? MB? GB?

    # 16. Tráfego SMS roaming
    trafego_sms_roaming_in = models.IntegerField(default=0)
    trafego_sms_roaming_out = models.IntegerField(default=0)

    # 17. Receita
    receita_total = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_servicos_voz = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_roaming_out = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_servicos_mensagens = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_dados_moveis = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_originadas = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_on_net = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_off_net = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_internacional = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_terminadas = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_terminadas_off_net = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_chamadas_terminadas_internacional = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))
    receita_mobile_money = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0'))

    # 18. Banda Larga Internacional (BLI) (Unidade?)
    banda_larga_internacional = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0')) # Mbit/s?

    # 19. Emprego
    emprego_total = models.IntegerField(default=0)
    emprego_homens = models.IntegerField(default=0)
    emprego_mulheres = models.IntegerField(default=0)

    def __str__(self):
        # Acesso seguro ao nome da operadora, caso o objeto Operadora não esteja carregado
        op_nome = self.operadora.nome if self.operadora_id and hasattr(self, 'operadora') and self.operadora else f"ID {self.operadora_id}"
        return f"{op_nome} - {self.ano}"

    class Meta:
        verbose_name = "Dados Anuais"
        verbose_name_plural = "Dados Anuais"
        # Garante que cada operadora tem apenas uma entrada por ano
        unique_together = ('ano', 'operadora')
        ordering = ['-ano', 'operadora__nome'] # Ordena pelo nome da operadora

    @classmethod
    def get_total_mercado(cls, ano, campo):
        """
        Calcula o total de um campo específico para um determinado ano,
        somando os valores de todas as operadoras.
        Retorna Decimal('0.0') ou 0 se não houver dados ou o total for zero.
        """
        total = cls.objects.filter(ano=ano).aggregate(total_campo=Sum(campo))['total_campo']
        # Verifica o tipo de campo para retornar o zero apropriado
        field = cls._meta.get_field(campo)
        if isinstance(field, models.DecimalField):
            return total or Decimal('0.0')
        elif isinstance(field, (models.IntegerField, models.BigIntegerField)):
            return total or 0
        else:
            # Para outros tipos (embora não esperado aqui), retorna o valor ou None
            return total

    def _get_market_share(self, campo):
        """Helper para calcular market share de um campo numérico."""
        valor_operadora = getattr(self, campo)
        if valor_operadora is None or valor_operadora == 0:
            return Decimal('0.0')

        # Obtém o total do mercado para o ano e campo específicos
        total_mercado = DadosAnuais.get_total_mercado(self.ano, campo)

        if total_mercado is None or total_mercado == 0:
            return Decimal('0.0') # Evita divisão por zero

        # Garante que ambos são Decimais para a divisão
        share = (Decimal(valor_operadora) / Decimal(total_mercado)) * Decimal(100)
        return share.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) # Arredonda para 2 casas decimais

    @property
    def market_share_assinantes(self):
        """Calcula a quota de mercado baseada nos assinantes da rede móvel."""
        return self._get_market_share('assinantes_rede_movel')

    @property
    def market_share_receita(self):
        """Calcula a quota de mercado baseada na receita total."""
        return self._get_market_share('receita_total')

    def calcular_crescimento(self, campo):
        """
        Calcula a taxa de crescimento percentual de um campo em relação ao ano anterior.
        Retorna Decimal('0.0') se não houver dados do ano anterior ou se o valor anterior for zero.
        """
        valor_atual = getattr(self, campo)
        if valor_atual is None: # Não se pode calcular crescimento sem valor atual
             return Decimal('0.0')

        try:
            dados_anterior = DadosAnuais.objects.get(ano=self.ano - 1, operadora=self.operadora)
            valor_anterior = getattr(dados_anterior, campo)

            if valor_anterior is None or valor_anterior == 0:
                # Crescimento indefinido ou infinito se valor anterior for 0 ou None
                return Decimal('0.0') # Ou poderia retornar None ou lançar uma exceção

            # Converte para Decimal para cálculo preciso
            crescimento = ((Decimal(valor_atual) - Decimal(valor_anterior)) / Decimal(valor_anterior)) * Decimal(100)
            return crescimento.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        except DadosAnuais.DoesNotExist:
            return Decimal('0.0') # Não há dados do ano anterior para comparar

    @classmethod
    def get_operadoras_por_ano(cls, ano):
        """Retorna um queryset das operadoras com dados para o ano especificado."""
        # Obtém os IDs das operadoras que têm registos para o ano
        operadora_ids = cls.objects.filter(ano=ano).values_list('operadora_id', flat=True).distinct()
        return Operadora.objects.filter(id__in=operadora_ids)

    @classmethod
    def get_anos_disponiveis(cls):
        """Retorna uma lista ordenada de anos únicos presentes nos dados."""
        return cls.objects.values_list('ano', flat=True).distinct().order_by('-ano') # Mais recente primeiro

    @property
    def arpu(self):
        """Calcula a Receita Média Por Utilizador (ARPU)."""
        if self.assinantes_rede_movel and self.receita_total is not None:
            arpu = Decimal(self.receita_total) / Decimal(self.assinantes_rede_movel)
            return arpu.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return Decimal('0.0')

    @classmethod
    def calculate_hhi(cls, ano, campo='assinantes_rede_movel'):
        """
        Calcula o Índice Herfindahl-Hirschman (HHI) para um determinado ano e campo.
        O HHI mede a concentração do mercado.
        """
        total_mercado = cls.get_total_mercado(ano, campo)

        if total_mercado is None or total_mercado == 0:
            return Decimal('0.0') # Mercado inexistente ou sem dados

        # Obtém os valores do campo para cada operadora no ano
        operadoras_data = cls.objects.filter(ano=ano).values('operadora_id', campo)

        # Calcula a soma dos quadrados das quotas de mercado percentuais
        hhi_sum = Decimal('0.0')
        for data in operadoras_data:
            valor = data[campo]
            if valor is not None and valor != 0:
                market_share_percent = (Decimal(valor) / Decimal(total_mercado)) * Decimal(100)
                hhi_sum += market_share_percent ** 2

        return hhi_sum.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Propriedade para aceder facilmente ao HHI de assinantes (exemplo)
    @property
    def market_concentration_assinantes(self):
         # Note: Isto executa uma query para cada instância.
         # Para listas, é mais eficiente chamar calculate_hhi uma vez.
        return DadosAnuais.calculate_hhi(self.ano, 'assinantes_rede_movel')

    # Propriedade para aceder facilmente ao HHI de receita (exemplo)
    @property
    def market_concentration_receita(self):
         # Note: Isto executa uma query para cada instância.
        return DadosAnuais.calculate_hhi(self.ano, 'receita_total')
