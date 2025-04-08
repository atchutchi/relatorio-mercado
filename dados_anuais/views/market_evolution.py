# views/market_evolution.py
from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal

class MarketEvolutionView(TemplateView):
    template_name = 'dados_anuais/market_evolution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anos = list(DadosAnuais.get_anos_disponiveis())
        
        evolution_data = []
        
        for ano in anos:
            # Usar get_total_mercado para obter os totais
            assinantes_total = DadosAnuais.get_total_mercado(ano, 'assinantes_rede_movel')
            receita_total = DadosAnuais.get_total_mercado(ano, 'receita_total')
            trafego_dados = DadosAnuais.get_total_mercado(ano, 'trafego_dados')
            investimentos = DadosAnuais.get_total_mercado(ano, 'investimentos')
            movel_total = DadosAnuais.get_total_mercado(ano, 'assinantes_banda_larga_movel')
            movel_3g = DadosAnuais.get_total_mercado(ano, 'assinantes_3g')
            movel_4g = DadosAnuais.get_total_mercado(ano, 'assinantes_4g')
            fixa_total = DadosAnuais.get_total_mercado(ano, 'banda_larga_256kbps')
            fixa_256k_2m = DadosAnuais.get_total_mercado(ano, 'banda_larga_256k_2m')
            fixa_2m_4m = DadosAnuais.get_total_mercado(ano, 'banda_larga_2m_4m')
            fixa_5m_10m = DadosAnuais.get_total_mercado(ano, 'banda_larga_5m_10m')
            fixa_10m = DadosAnuais.get_total_mercado(ano, 'banda_larga_10m')
            fixa_outros = DadosAnuais.get_total_mercado(ano, 'banda_larga_outros')

            data = {
                'ano': ano,
                'assinantes_total': assinantes_total,
                'receita_total': float(receita_total) if isinstance(receita_total, Decimal) else receita_total,
                'trafego_dados': trafego_dados,
                'investimentos': float(investimentos) if isinstance(investimentos, Decimal) else investimentos,
                'banda_larga_movel': {
                    'total': movel_total,
                    '3g': movel_3g,
                    '4g': movel_4g
                },
                'banda_larga_fixa': {
                    'total': fixa_total,
                    '256k_2m': fixa_256k_2m,
                    '2m_4m': fixa_2m_4m,
                    '5m_10m': fixa_5m_10m,
                    '10m': fixa_10m,
                    'outros': fixa_outros
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