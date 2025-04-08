from django.views.generic import TemplateView
from ..models import DadosAnuais, Operadora
import json
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class MarketAnalysisView(TemplateView):
    template_name = 'dados_anuais/market_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = list(Operadora.objects.values_list('nome', flat=True))

        market_share_data = {}
        hhi_data = {}
        volume_negocio_data = {}
        investimentos_data = {}
        trafego_dados_data = {}
        emprego_data = {}

        for ano in anos:
            # Calcular market share com método dinâmico
            market_share_data[ano] = self.calculate_market_share(ano)
            
            # Usar o método calculate_hhi do modelo
            hhi_data[ano] = float(DadosAnuais.calculate_hhi(ano, 'assinantes_rede_movel'))
            
            # Obter dados de indicadores para cada operadora
            volume_negocio_data[ano] = self.get_indicator_data(ano, 'volume_negocio')
            investimentos_data[ano] = self.get_indicator_data(ano, 'investimentos')
            trafego_dados_data[ano] = self.get_indicator_data(ano, 'trafego_dados')
            emprego_data[ano] = self.get_indicator_data(ano, 'emprego_total')

        logger.debug(f"Anos: {anos}")
        logger.debug(f"Operadoras: {operadoras}")
        logger.debug(f"Dados de participação de mercado: {market_share_data}")
        logger.debug(f"Dados de HHI: {hhi_data}")
        logger.debug(f"Dados de volume de negócio: {volume_negocio_data}")
        logger.debug(f"Dados de investimentos: {investimentos_data}")
        logger.debug(f"Dados de tráfego de dados: {trafego_dados_data}")
        logger.debug(f"Dados de emprego: {emprego_data}")

        context['anos'] = json.dumps(anos)
        context['operadoras'] = json.dumps(operadoras)
        context['market_share_data'] = json.dumps(market_share_data)
        context['hhi_data'] = json.dumps(hhi_data)
        context['volume_negocio_data'] = json.dumps(volume_negocio_data)
        context['investimentos_data'] = json.dumps(investimentos_data)
        context['trafego_dados_data'] = json.dumps(trafego_dados_data)
        context['emprego_data'] = json.dumps(emprego_data)
        
        return context

    def calculate_market_share(self, ano):
        """
        Calcula a participação de mercado de cada operadora para um determinado ano,
        em relação ao número de assinantes.
        """
        market_shares = {}
        total_assinantes = DadosAnuais.get_total_mercado(ano, 'assinantes_rede_movel')
        
        if total_assinantes:
            # Obter todas as operadoras que têm dados para este ano
            operadoras_no_ano = DadosAnuais.get_operadoras_por_ano(ano)
            
            for operadora in operadoras_no_ano:
                dados = DadosAnuais.objects.filter(
                    ano=ano, 
                    operadora=operadora
                ).select_related('operadora').first()
                
                if dados and dados.assinantes_rede_movel:
                    # Calcular a porcentagem e arredondar para 2 casas decimais
                    market_share = (dados.assinantes_rede_movel / total_assinantes) * 100
                    market_shares[operadora.nome] = float(round(market_share, 2))
                else:
                    market_shares[operadora.nome] = 0
        
        logger.debug(f"Market shares para o ano {ano}: {market_shares}")
        return market_shares

    def get_indicator_data(self, ano, indicator):
        """
        Obtém os valores de um indicador específico para todas as operadoras em um determinado ano.
        """
        data = {}
        operadoras_no_ano = DadosAnuais.get_operadoras_por_ano(ano)
        
        for operadora in operadoras_no_ano:
            dados = DadosAnuais.objects.filter(
                ano=ano, 
                operadora=operadora
            ).select_related('operadora').first()
            
            if dados:
                value = getattr(dados, indicator)
                # Converter Decimal para float para serialização JSON
                data[operadora.nome] = float(value) if isinstance(value, Decimal) else value
        
        return data