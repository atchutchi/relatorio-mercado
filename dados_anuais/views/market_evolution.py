# views/market_evolution.py
from django.views.generic import TemplateView
from ..models import DadosAnuais
from django.db.models import Sum
import json
from decimal import Decimal

class MarketEvolutionView(TemplateView):
    template_name = 'dados_anuais/market_evolution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anos = list(DadosAnuais.get_anos_disponiveis())
        
        evolution_data = []
        
        for ano in anos:
            dados_totais = DadosAnuais.objects.filter(ano=ano).aggregate(
                assinantes_total=Sum('assinantes_rede_movel'),
                receita_total=Sum('receita_total'),
                trafego_dados=Sum('trafego_dados'),
                investimentos=Sum('investimentos'),
                movel_total=Sum('assinantes_banda_larga_movel'),
                movel_3g=Sum('assinantes_3g'),
                movel_4g=Sum('assinantes_4g'),
                # Banda Larga Fixa
                fixa_total=Sum('banda_larga_256kbps'), # Total é igual ao valor de banda_larga_256kbps
                fixa_256k_2m=Sum('banda_larga_256k_2m'),
                fixa_2m_4m=Sum('banda_larga_2m_4m'),
                fixa_5m_10m=Sum('banda_larga_5m_10m'),
                fixa_10m=Sum('banda_larga_10m'),
                fixa_outros=Sum('banda_larga_outros')
            )

            data = {
                'ano': ano,
                'assinantes_total': dados_totais['assinantes_total'] or 0,
                'receita_total': float(dados_totais['receita_total'] or 0),
                'trafego_dados': dados_totais['trafego_dados'] or 0,
                'investimentos': float(dados_totais['investimentos'] or 0),
                'banda_larga_movel': {
                    'total': dados_totais['movel_total'] or 0,
                    '3g': dados_totais['movel_3g'] or 0,
                    '4g': dados_totais['movel_4g'] or 0
                },
                'banda_larga_fixa': {
                    'total': dados_totais['fixa_total'] or 0,  # Usando o valor correto para o total
                    '256k_2m': dados_totais['fixa_256k_2m'] or 0,
                    '2m_4m': dados_totais['fixa_2m_4m'] or 0,
                    '5m_10m': dados_totais['fixa_5m_10m'] or 0,
                    '10m': dados_totais['fixa_10m'] or 0,
                    'outros': dados_totais['fixa_outros'] or 0
                }
            }
            evolution_data.append(data)

        context['evolution_data'] = json.dumps(evolution_data)
        context['anos'] = json.dumps(anos)
        context['assinantes_total'] = json.dumps([data['assinantes_total'] for data in evolution_data])
        context['receita_total'] = json.dumps([data['receita_total'] for data in evolution_data])
        context['trafego_dados_total'] = json.dumps([data['trafego_dados'] for data in evolution_data])
        context['investimentos_total'] = json.dumps([data['investimentos'] for data in evolution_data])
        context['banda_larga_movel'] = json.dumps([data['banda_larga_movel'] for data in evolution_data])
        context['banda_larga_fixa'] = json.dumps([data['banda_larga_fixa'] for data in evolution_data])

        return context