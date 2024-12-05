# views/annual_report.py
from django.views.generic import TemplateView
from ..models import DadosAnuais
from django.db.models import Sum, Max
import json
from decimal import Decimal
from django.shortcuts import get_object_or_404

class AnnualReportView(TemplateView):
    template_name = 'dados_anuais/annual_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pegar todos os anos disponíveis
        anos_disponiveis = list(DadosAnuais.get_anos_disponiveis())
        
        # Pegar o ano selecionado ou o último ano disponível
        ano_selecionado = self.request.GET.get('ano', anos_disponiveis[-1])
        try:
            ano_selecionado = int(ano_selecionado)
        except (TypeError, ValueError):
            ano_selecionado = anos_disponiveis[-1]

        # 1. Dados gerais do mercado
        dados_mercado = {
            'totais': DadosAnuais.objects.filter(ano=ano_selecionado, operadora='TOTAL').first(),
            'mtn': DadosAnuais.objects.filter(ano=ano_selecionado, operadora='MTN').first(),
            'orange': DadosAnuais.objects.filter(ano=ano_selecionado, operadora='ORANGE').first()
        }

        # 2. Mercado de Telefonia Móvel
        mercado_movel = {
            'assinantes': {
                'total': dados_mercado['totais'].assinantes_rede_movel,
                'pos_pago': dados_mercado['totais'].assinantes_pos_pago,
                'pre_pago': dados_mercado['totais'].assinantes_pre_pago,
                'utilizacao_efetiva': dados_mercado['totais'].utilizacao_efetiva
            },
            'banda_larga_movel': {
                'total': dados_mercado['totais'].assinantes_banda_larga_movel,
                '3g': dados_mercado['totais'].assinantes_3g,
                '3g_box': dados_mercado['totais'].assinantes_3g_box,
                '3g_usb': dados_mercado['totais'].assinantes_3g_usb,
                '4g': dados_mercado['totais'].assinantes_4g,
                '4g_box': dados_mercado['totais'].assinantes_4g_box,
                '4g_usb': dados_mercado['totais'].assinantes_4g_usb
            },
            'banda_larga_fixa': {
                'total': dados_mercado['totais'].banda_larga_256kbps,
                '256k_2m': dados_mercado['totais'].banda_larga_256k_2m,
                '2m_4m': dados_mercado['totais'].banda_larga_2m_4m,
                '5m_10m': dados_mercado['totais'].banda_larga_5m_10m,
                '10m': dados_mercado['totais'].banda_larga_10m,
                'outros': dados_mercado['totais'].banda_larga_outros
            }
        }

        # 3. Indicadores Financeiros
        indicadores_financeiros = {
            'volume_negocio': float(dados_mercado['totais'].volume_negocio or 0),
            'investimentos': float(dados_mercado['totais'].investimentos or 0),
            'receita_total': float(dados_mercado['totais'].receita_total or 0),
            'por_operadora': {
                'MTN': {
                    'volume_negocio': float(dados_mercado['mtn'].volume_negocio or 0),
                    'receita_total': float(dados_mercado['mtn'].receita_total or 0)
                },
                'ORANGE': {
                    'volume_negocio': float(dados_mercado['orange'].volume_negocio or 0),
                    'receita_total': float(dados_mercado['orange'].receita_total or 0)
                }
            }
        }

        # 4. Tráfego
        trafego = {
            'voz': {
                'total': dados_mercado['totais'].trafego_voz_originado,
                'on_net': dados_mercado['totais'].trafego_voz_on_net,
                'off_net': dados_mercado['totais'].trafego_voz_off_net,
                'internacional': dados_mercado['totais'].trafego_voz_internacional
            },
            'dados': {
                'total': dados_mercado['totais'].trafego_dados,
                '3g': dados_mercado['totais'].trafego_dados_3g,
                '4g': dados_mercado['totais'].trafego_dados_4g
            },
            'sms': {
                'total': dados_mercado['totais'].trafego_sms,
                'on_net': dados_mercado['totais'].trafego_sms_on_net,
                'off_net': dados_mercado['totais'].trafego_sms_off_net,
                'internacional': dados_mercado['totais'].trafego_sms_internacional
            }
        }

        # 5. Emprego no Setor
        emprego = {
            'total': dados_mercado['totais'].emprego_total,
            'homens': dados_mercado['totais'].emprego_homens,
            'mulheres': dados_mercado['totais'].emprego_mulheres,
            'por_operadora': {
                'MTN': dados_mercado['mtn'].emprego_total,
                'ORANGE': dados_mercado['orange'].emprego_total
            }
        }

        # Análise de crescimento
        crescimento = self.calcular_crescimento(ano_selecionado)

        context.update({
            'ano_atual': ano_selecionado,
            'anos_disponiveis': anos_disponiveis,
            'mercado_movel': mercado_movel,
            'indicadores_financeiros': indicadores_financeiros,
            'trafego': trafego,
            'emprego': emprego,
            'crescimento': crescimento
        })

        return context

    def calcular_crescimento(self, ano):
        ano_anterior = ano - 1
        dados_atual = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
        dados_anterior = DadosAnuais.objects.filter(ano=ano_anterior, operadora='TOTAL').first()

        if not dados_anterior or not dados_atual:
            return {}

        campos_crescimento = [
            'assinantes_rede_movel',
            'assinantes_banda_larga_movel',
            'banda_larga_256kbps',
            'receita_total',
            'trafego_dados',
            'volume_negocio',
            'investimentos',
            'emprego_total'
        ]

        crescimento = {}
        for campo in campos_crescimento:
            valor_atual = getattr(dados_atual, campo) or 0
            valor_anterior = getattr(dados_anterior, campo) or 0
            
            if isinstance(valor_atual, Decimal):
                valor_atual = float(valor_atual)
            if isinstance(valor_anterior, Decimal):
                valor_anterior = float(valor_anterior)
            
            if valor_anterior:
                crescimento[campo] = ((valor_atual - valor_anterior) / valor_anterior) * 100
            else:
                crescimento[campo] = 0 if valor_atual == 0 else 100

        return crescimento