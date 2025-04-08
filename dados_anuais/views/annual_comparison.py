from django.views.generic import TemplateView
from ..models import DadosAnuais, Operadora
import json
from decimal import Decimal

class AnnualComparisonView(TemplateView):
   template_name = 'dados_anuais/annual_comparison.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       
       anos = list(DadosAnuais.get_anos_disponiveis())
       operadoras = list(Operadora.objects.values_list('nome', flat=True))

       comparison_data = {}
       for ano in anos:
           comparison_data[ano] = {}
           
           # Obter todas as operadoras com dados para este ano
           operadoras_no_ano = DadosAnuais.get_operadoras_por_ano(ano)
           
           # Obter todos os dados para este ano em uma única consulta
           dados_por_operadora = {}
           for dado in DadosAnuais.objects.filter(ano=ano).select_related('operadora'):
               dados_por_operadora[dado.operadora.nome] = dado
           
           for operadora in operadoras_no_ano:
               dados = dados_por_operadora.get(operadora.nome)
               if dados:
                   # Obter os campos principais
                   dados_dic = {
                       'assinantes_rede_movel': dados.assinantes_rede_movel,
                       'assinantes_banda_larga_movel': dados.assinantes_banda_larga_movel,
                       'assinantes_3g': dados.assinantes_3g,
                       'assinantes_4g': dados.assinantes_4g,
                       'banda_larga_fixa': dados.banda_larga_256kbps,
                       '256k_2m': dados.banda_larga_256k_2m,
                       '2m_4m': dados.banda_larga_2m_4m,
                       '5m_10m': dados.banda_larga_5m_10m,
                       '10m': dados.banda_larga_10m,
                       'outros': dados.banda_larga_outros,
                       'receita_total': float(dados.receita_total),
                       'trafego_dados': dados.trafego_dados,
                       'investimentos': float(dados.investimentos),
                       'volume_negocio': float(dados.volume_negocio),
                   }
                   comparison_data[ano][operadora.nome] = dados_dic
       
       # Adicionar dados totais para cada ano
       for ano in anos:
           comparison_data[ano]['TOTAL'] = {
               'assinantes_rede_movel': DadosAnuais.get_total_mercado(ano, 'assinantes_rede_movel'),
               'assinantes_banda_larga_movel': DadosAnuais.get_total_mercado(ano, 'assinantes_banda_larga_movel'),
               'assinantes_3g': DadosAnuais.get_total_mercado(ano, 'assinantes_3g'),
               'assinantes_4g': DadosAnuais.get_total_mercado(ano, 'assinantes_4g'),
               'banda_larga_fixa': DadosAnuais.get_total_mercado(ano, 'banda_larga_256kbps'),
               '256k_2m': DadosAnuais.get_total_mercado(ano, 'banda_larga_256k_2m'),
               '2m_4m': DadosAnuais.get_total_mercado(ano, 'banda_larga_2m_4m'),
               '5m_10m': DadosAnuais.get_total_mercado(ano, 'banda_larga_5m_10m'),
               '10m': DadosAnuais.get_total_mercado(ano, 'banda_larga_10m'),
               'outros': DadosAnuais.get_total_mercado(ano, 'banda_larga_outros'),
               'receita_total': float(DadosAnuais.get_total_mercado(ano, 'receita_total')),
               'trafego_dados': DadosAnuais.get_total_mercado(ano, 'trafego_dados'),
               'investimentos': float(DadosAnuais.get_total_mercado(ano, 'investimentos')),
               'volume_negocio': float(DadosAnuais.get_total_mercado(ano, 'volume_negocio')),
           }

       context['comparison_data'] = json.dumps(comparison_data, default=self.decimal_default)
       context['anos'] = json.dumps(anos)
       context['operadoras'] = json.dumps(operadoras + ['TOTAL'])  # Adicionar 'TOTAL' para mostrar na interface

       return context

   def decimal_default(self, obj):
       if isinstance(obj, Decimal):
           return float(obj)
       raise TypeError