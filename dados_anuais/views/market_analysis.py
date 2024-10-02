from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal

class MarketAnalysisView(TemplateView):
    template_name = 'dados_anuais/market_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = DadosAnuais.get_anos_disponiveis()
        operadoras = [op[0] for op in DadosAnuais.OPERADORAS if op[0] != 'TOTAL']

        market_share_data = {}
        hhi_data = {}

        for ano in anos:
            market_share_data[ano] = self.calculate_market_share(ano, operadoras)
            hhi_data[ano] = self.calculate_hhi(market_share_data[ano])

        context['anos'] = json.dumps(list(anos))
        context['operadoras'] = json.dumps(operadoras)
        context['market_share_data'] = json.dumps(market_share_data)
        context['hhi_data'] = json.dumps(hhi_data)
        
        return context

    def calculate_market_share(self, ano, operadoras):
        total = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
        market_shares = {}
        
        if total and total.assinantes_rede_movel:
            for operadora in operadoras:
                dados = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                if dados and dados.assinantes_rede_movel:
                    market_shares[operadora] = (dados.assinantes_rede_movel / total.assinantes_rede_movel) * 100
                else:
                    market_shares[operadora] = 0
        
        return market_shares

    def calculate_hhi(self, market_shares):
        return sum(share ** 2 for share in market_shares.values())