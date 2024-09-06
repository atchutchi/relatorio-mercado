from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Sum, Avg
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
import logging
from .models import (
    DadosAnuais,
)

logger = logging.getLogger(__name__)

class DadosAnuaisListView(ListView):
    model = DadosAnuais
    template_name = 'dados_anuais/dados_anuais_list.html'
    context_object_name = 'dados_anuais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter dados totais por ano
        dados_totais = DadosAnuais.objects.filter(operadora='TOTAL').order_by('ano')
        
        # Preparar dados para gráficos
        context['dados_graficos'] = {
            'anos': [d.ano for d in dados_totais],
            'assinantes_rede_movel': [d.assinantes_rede_movel for d in dados_totais],
            'volume_negocio': [float(d.volume_negocio) for d in dados_totais],
            'trafego_voz_originado': [d.trafego_voz_originado for d in dados_totais],
            'assinantes_banda_larga_movel': [d.assinantes_banda_larga_movel for d in dados_totais],
        }
        
        # Calcular algumas estatísticas gerais
        context['estatisticas'] = {
            'total_assinantes': dados_totais.last().assinantes_rede_movel if dados_totais else 0,
            'crescimento_assinantes': self.calcular_crescimento(dados_totais, 'assinantes_rede_movel'),
            'volume_negocio_atual': dados_totais.last().volume_negocio if dados_totais else 0,
            'crescimento_volume_negocio': self.calcular_crescimento(dados_totais, 'volume_negocio'),
        }
        
        return context

    def calcular_crescimento(self, dados, campo):
        if len(dados) < 2:
            return 0
        valor_anterior = getattr(dados[len(dados)-2], campo)
        valor_atual = getattr(dados.last(), campo)
        if isinstance(valor_anterior, (int, float)) and isinstance(valor_atual, (int, float)):
            return ((valor_atual - valor_anterior) / valor_anterior) * 100 if valor_anterior else 0
        return 0

class DadosAnuaisDetailView(DetailView):
    model = DadosAnuais
    template_name = 'dados_anuais/dados_anuais_detail.html'
    context_object_name = 'dados'

    def get_object(self):
        return DadosAnuais.objects.filter(
            ano=self.kwargs['ano'],
            operadora=self.kwargs['operadora']
        ).first()

def comparacao_operadoras(request, ano):
    # Buscar dados para MTN, Orange e total para o ano especificado
    dados_mtn = DadosAnuais.objects.filter(ano=ano, operadora='MTN').first()
    dados_orange = DadosAnuais.objects.filter(ano=ano, operadora='ORANGE').first()
    dados_total = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()

    context = {
        'ano': ano,
        'dados_mtn': dados_mtn,
        'dados_orange': dados_orange,
        'dados_total': dados_total,
        'dadosComparacao': {
            'mtn': dados_mtn,
            'orange': dados_orange
        }
    }

    return render(request, 'dados_anuais/comparacao_operadoras.html', context)

def evolucao_indicadores(request):
    # Obter anos únicos ordenados
    anos = DadosAnuais.objects.values_list('ano', flat=True).distinct().order_by('ano')
    
    # Definir indicadores a serem analisados
    indicadores = [
        'assinantes_rede_movel',
        'assinantes_banda_larga_movel',
        'volume_negocio',
        'trafego_voz_originado',
        'trafego_dados',
    ]

    # Inicializar dicionário para armazenar dados de evolução
    dados_evolucao = {indicador: [] for indicador in indicadores}

    # Coletar dados para cada ano
    for ano in anos:
        dados_ano = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
        if dados_ano:
            for indicador in indicadores:
                dados_evolucao[indicador].append(getattr(dados_ano, indicador))

    context = {
        'anos': list(anos),
        'dados_evolucao': dados_evolucao,
        'dadosEvolucao': {
            'anos': list(anos),
            'assinantes_rede_movel': dados_evolucao['assinantes_rede_movel'],
            'volume_negocio': dados_evolucao['volume_negocio'],
            'trafego_dados': dados_evolucao['trafego_dados']
        }
    }

    return render(request, 'dados_anuais/evolucao_indicadores.html', context)
