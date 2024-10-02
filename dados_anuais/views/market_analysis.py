from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class MarketAnalysisView(TemplateView):
    template_name = 'dados_anuais/market_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = [op[0] for op in DadosAnuais.OPERADORAS if op[0] != 'TOTAL']

        market_share_data = {}
        hhi_data = {}
        volume_negocio_data = {}
        investimentos_data = {}
        trafego_dados_data = {}
        emprego_data = {}

        for ano in anos:
            market_share_data[ano] = self.calculate_market_share(ano, operadoras)
            hhi_data[ano] = self.calculate_hhi(market_share_data[ano])
            volume_negocio_data[ano] = self.get_indicator_data(ano, operadoras, 'volume_negocio')
            investimentos_data[ano] = self.get_indicator_data(ano, operadoras, 'investimentos')
            trafego_dados_data[ano] = self.get_indicator_data(ano, operadoras, 'trafego_dados')
            emprego_data[ano] = self.get_indicator_data(ano, operadoras, 'emprego_total')

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

    def calculate_market_share(self, ano, operadoras):
        market_shares = {}
        total_assinantes = sum(DadosAnuais.objects.filter(ano=ano, operadora__in=operadoras).values_list('assinantes_rede_movel', flat=True))
        
        if total_assinantes:
            for operadora in operadoras:
                dados = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                if dados and dados.assinantes_rede_movel:
                    market_shares[operadora] = (dados.assinantes_rede_movel / total_assinantes) * 100
                else:
                    market_shares[operadora] = 0
        
        logger.debug(f"Market shares para o ano {ano}: {market_shares}")
        return market_shares

    def calculate_hhi(self, market_shares):
        hhi = sum(share ** 2 for share in market_shares.values())
        logger.debug(f"HHI calculado: {hhi}")
        return hhi

    def get_indicator_data(self, ano, operadoras, indicator):
        data = {}
        for operadora in operadoras:
            dados = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
            if dados:
                value = getattr(dados, indicator)
                data[operadora] = float(value) if isinstance(value, Decimal) else value
        return data