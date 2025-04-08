from django.views.generic import TemplateView
from django.db.models import Sum
from ..models import DadosAnuais
import json
from decimal import Decimal


class MarketOverviewView(TemplateView):
    template_name = 'dados_anuais/market_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        
        overview_data = []
        for ano in anos:
            # Usar os novos métodos para cálculo de totais dinâmicos
            assinantes_total = DadosAnuais.get_total_mercado(ano, 'assinantes_rede_movel')
            receita_total = DadosAnuais.get_total_mercado(ano, 'receita_total')
            trafego_dados_total = DadosAnuais.get_total_mercado(ano, 'trafego_dados')
            investimentos_total = DadosAnuais.get_total_mercado(ano, 'investimentos')
            
            # Converter para formato adequado para JSON
            data = {
                'ano': ano,
                'assinantes_total': assinantes_total,  # Já é int
                'receita_total': float(receita_total) if isinstance(receita_total, Decimal) else receita_total,
                'trafego_dados_total': trafego_dados_total,  # Já é int
                'investimentos_total': float(investimentos_total) if isinstance(investimentos_total, Decimal) else investimentos_total
            }
            overview_data.append(data)

        context['overview_data'] = json.dumps(overview_data)
        context['anos'] = json.dumps(anos)
        context['assinantes_total'] = json.dumps([data['assinantes_total'] for data in overview_data])
        context['receita_total'] = json.dumps([data['receita_total'] for data in overview_data])
        context['trafego_dados_total'] = json.dumps([data['trafego_dados_total'] for data in overview_data])
        context['investimentos_total'] = json.dumps([data['investimentos_total'] for data in overview_data])

        return context