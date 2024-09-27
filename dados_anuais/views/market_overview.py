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
            total = DadosAnuais.get_total_mercado(ano)
            if total:
                if isinstance(total, DadosAnuais):
                    data = {
                        'ano': ano,
                        'assinantes_total': total.assinantes_rede_movel or 0,
                        'receita_total': float(total.receita_total or 0),
                        'trafego_dados_total': total.trafego_dados or 0,
                        'investimentos_total': float(total.investimentos or 0)
                    }
                else:
                    data = {
                        'ano': ano,
                        'assinantes_total': total['assinantes_rede_movel'] or 0,
                        'receita_total': float(total['receita_total'] or 0),
                        'trafego_dados_total': total['trafego_dados'] or 0,
                        'investimentos_total': float(total['investimentos'] or 0)
                    }
                overview_data.append(data)

        context['overview_data'] = json.dumps(overview_data)
        context['anos'] = json.dumps(anos)
        context['assinantes_total'] = json.dumps([data['assinantes_total'] for data in overview_data])
        context['receita_total'] = json.dumps([data['receita_total'] for data in overview_data])
        context['trafego_dados_total'] = json.dumps([data['trafego_dados_total'] for data in overview_data])
        context['investimentos_total'] = json.dumps([data['investimentos_total'] for data in overview_data])

        return context