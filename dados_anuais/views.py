from tablib import Dataset
from .resource import DadosAnuaisResource
from django.views.generic import ListView, DetailView
from django.db.models import Sum, IntegerField, DecimalField, BigIntegerField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from openpyxl import Workbook
import json
import logging
from .models import DadosAnuais
from .tasks import process_excel_upload

logger = logging.getLogger(__name__)


class DadosAnuaisListView(ListView):
    model = DadosAnuais
    template_name = 'dados_anuais/dados_anuais_list.html'
    context_object_name = 'dados_anuais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Definir todos os campos do modelo
        todos_campos = [f.name for f in DadosAnuais._meta.get_fields() if f.name not in ['id', 'ano', 'operadora']]
        
        # Identificar campos numéricos
        campos_numericos = [f.name for f in DadosAnuais._meta.get_fields() 
                            if isinstance(f, (IntegerField, BigIntegerField, DecimalField))]
        
        # Obter anos distintos
        anos = DadosAnuais.objects.values_list('ano', flat=True).distinct().order_by('ano')
        
        # Calcular dados totais por ano
        dados_totais = []
        for ano in anos:
            total_ano = DadosAnuais.objects.filter(ano=ano).aggregate(
                **{campo: Sum(campo) for campo in campos_numericos}
            )
            total_ano['ano'] = ano
            dados_totais.append(total_ano)
        
        # Preparar dados para gráficos
        context['dados_graficos'] = {
            'anos': [d['ano'] for d in dados_totais],
            **{campo: [d.get(campo, 0) for d in dados_totais] for campo in campos_numericos}
        }
        
        # Calcular estatísticas para todos os campos numéricos
        context['estatisticas'] = {}
        if dados_totais:
            for campo in campos_numericos:
                valor_atual = dados_totais[-1].get(campo, 0)
                crescimento = self.calcular_crescimento(dados_totais, campo)
                context['estatisticas'][f'{campo}_atual'] = valor_atual
                context['estatisticas'][f'{campo}_crescimento'] = crescimento
        
        context['campos'] = todos_campos
        
        return context

    def calcular_crescimento(self, dados, campo):
        if len(dados) < 2:
            return 0
        valor_anterior = dados[-2].get(campo, 0)
        valor_atual = dados[-1].get(campo, 0)
        if valor_anterior and valor_atual:
            return ((valor_atual - valor_anterior) / valor_anterior) * 100
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos'] = [f.name for f in DadosAnuais._meta.get_fields() if f.name not in ['id', 'ano', 'operadora']]
        return context


def comparacao_operadoras(request, ano):
    dados_mtn = DadosAnuais.objects.filter(ano=ano, operadora='MTN').first()
    dados_orange = DadosAnuais.objects.filter(ano=ano, operadora='ORANGE').first()
    dados_total = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()

    indicadores = [
        'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
        'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_3g_box', 'assinantes_3g_usb',
        'assinantes_4g', 'assinantes_4g_box', 'assinantes_4g_usb', 'assinantes_banda_larga_fixa',
        'banda_larga_256kbps', 'banda_larga_256k_2m', 'banda_larga_2m_4m', 'banda_larga_5m_10m',
        'banda_larga_10m', 'banda_larga_outros', 'volume_negocio', 'investimentos',
        'trafego_voz_originado', 'trafego_voz_on_net', 'trafego_voz_off_net', 'trafego_voz_numeros_curtos',
        'trafego_voz_internacional', 'trafego_sms', 'trafego_sms_on_net', 'trafego_sms_off_net',
        'trafego_sms_internacional', 'trafego_dados', 'trafego_dados_2g', 'trafego_dados_3g',
        'trafego_dados_3g_box', 'trafego_dados_3g_usb', 'trafego_dados_4g', 'trafego_dados_4g_box',
        'trafego_dados_4g_usb', 'chamadas_originadas', 'chamadas_originadas_on_net',
        'chamadas_originadas_off_net', 'chamadas_originadas_numeros_curtos',
        'chamadas_originadas_internacional', 'trafego_voz_terminado', 'trafego_voz_terminado_off_net',
        'trafego_voz_terminado_internacional', 'trafego_sms_terminado', 'trafego_sms_terminado_off_net',
        'trafego_sms_terminado_internacional', 'chamadas_terminadas', 'chamadas_terminadas_off_net',
        'chamadas_terminadas_internacional', 'roaming_in_minutos', 'roaming_out_minutos',
        'roaming_in_chamadas', 'roaming_out_chamadas', 'volume_internet_nacional',
        'volume_internet_internacional', 'trafego_sms_roaming_in', 'trafego_sms_roaming_out',
        'receita_total', 'receita_servicos_voz', 'receita_roaming_out', 'receita_servicos_mensagens',
        'receita_dados_moveis', 'receita_chamadas_originadas', 'receita_chamadas_on_net',
        'receita_chamadas_off_net', 'receita_chamadas_internacional', 'receita_chamadas_terminadas',
        'receita_chamadas_terminadas_off_net', 'receita_chamadas_terminadas_internacional',
        'receita_mobile_money', 'banda_larga_internacional', 'emprego_total', 'emprego_homens',
        'emprego_mulheres'
    ]

    context = {
        'ano': ano,
        'dados_mtn': dados_mtn,
        'dados_orange': dados_orange,
        'dados_total': dados_total,
        'indicadores': indicadores,
        'dadosComparacao': {
            'mtn': dados_mtn,
            'orange': dados_orange
        }
    }

    return render(request, 'dados_anuais/comparacao_operadoras.html', context)


def evolucao_indicadores(request):
    anos = DadosAnuais.objects.values_list('ano', flat=True).distinct().order_by('ano')
    
    indicadores = [
        'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
        'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_3g_box', 'assinantes_3g_usb',
        'assinantes_4g', 'assinantes_4g_box', 'assinantes_4g_usb', 'assinantes_banda_larga_fixa',
        'banda_larga_256kbps', 'banda_larga_256k_2m', 'banda_larga_2m_4m', 'banda_larga_5m_10m',
        'banda_larga_10m', 'banda_larga_outros', 'volume_negocio', 'investimentos',
        'trafego_voz_originado', 'trafego_voz_on_net', 'trafego_voz_off_net', 'trafego_voz_numeros_curtos',
        'trafego_voz_internacional', 'trafego_sms', 'trafego_sms_on_net', 'trafego_sms_off_net',
        'trafego_sms_internacional', 'trafego_dados', 'trafego_dados_2g', 'trafego_dados_3g',
        'trafego_dados_3g_box', 'trafego_dados_3g_usb', 'trafego_dados_4g', 'trafego_dados_4g_box',
        'trafego_dados_4g_usb', 'chamadas_originadas', 'chamadas_originadas_on_net',
        'chamadas_originadas_off_net', 'chamadas_originadas_numeros_curtos',
        'chamadas_originadas_internacional', 'trafego_voz_terminado', 'trafego_voz_terminado_off_net',
        'trafego_voz_terminado_internacional', 'trafego_sms_terminado', 'trafego_sms_terminado_off_net',
        'trafego_sms_terminado_internacional', 'chamadas_terminadas', 'chamadas_terminadas_off_net',
        'chamadas_terminadas_internacional', 'roaming_in_minutos', 'roaming_out_minutos',
        'roaming_in_chamadas', 'roaming_out_chamadas', 'volume_internet_nacional',
        'volume_internet_internacional', 'trafego_sms_roaming_in', 'trafego_sms_roaming_out',
        'receita_total', 'receita_servicos_voz', 'receita_roaming_out', 'receita_servicos_mensagens',
        'receita_dados_moveis', 'receita_chamadas_originadas', 'receita_chamadas_on_net',
        'receita_chamadas_off_net', 'receita_chamadas_internacional', 'receita_chamadas_terminadas',
        'receita_chamadas_terminadas_off_net', 'receita_chamadas_terminadas_internacional',
        'receita_mobile_money', 'banda_larga_internacional', 'emprego_total', 'emprego_homens',
        'emprego_mulheres'
    ]

    dados_evolucao = {indicador: [] for indicador in indicadores}
    dados_evolucao['anos'] = list(anos)

    for ano in anos:
        # Tente obter os dados 'TOTAL' primeiro
        dados_ano = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
        
        # Se não houver dados 'TOTAL', some os dados de todas as operadoras
        if not dados_ano:
            dados_ano = DadosAnuais.objects.filter(ano=ano).aggregate(**{
                indicador: Sum(indicador) for indicador in indicadores
            })
        
        if dados_ano:
            for indicador in indicadores:
                valor = getattr(dados_ano, indicador, None) if isinstance(dados_ano, DadosAnuais) else dados_ano.get(indicador)
                dados_evolucao[indicador].append(valor if valor is not None else 0)
        else:
            # Se não houver dados para o ano, preencha com zeros
            for indicador in indicadores:
                dados_evolucao[indicador].append(0)
        
        # Log para debug
        logger.debug(f"Dados para o ano {ano}: {dados_ano}")

    # Selecione alguns indicadores chave para os gráficos
    indicadores_chave = [
        'assinantes_rede_movel',
        'volume_negocio',
        'trafego_voz_originado',
        'trafego_dados',
        'receita_total'
    ]

    dados_graficos = {
        indicador: dados_evolucao[indicador]
        for indicador in indicadores_chave
    }
    dados_graficos['anos'] = dados_evolucao['anos']

    context = {
        'anos': list(anos),
        'dados_evolucao': dados_evolucao,
        'indicadores': indicadores,
        'dados_graficos': dados_graficos
    }

    # Log para debug
    logger.debug(f"Contexto enviado para o template: {context}")

    return render(request, 'dados_anuais/evolucao_indicadores.html', context)


def is_admin(user):
    return user.is_authenticated and user.is_staff
