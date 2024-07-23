from django.views.generic import TemplateView
from .models import EstacoesMoveisEfetivas, EmpregoSetor, TrafegoNacional, QuotaMercado, TaxaPenetracao, VolumeNegocio, Operadora
import json
from django.utils.safestring import mark_safe
import logging

class MercadoTelefoniaMovelView(TemplateView):
    template_name = 'indicadores/mercado_de_telefonia_movel.html'


class EstacoesMoveisView(TemplateView):
    template_name = 'indicadores/estacoes_moveis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estacoes_moveis = EstacoesMoveisEfetivas.objects.order_by('ano', 'trimestre')
        
        context['estacoes_moveis_data'] = {
            'labels': [],
            'mtn': [],
            'orange': [],
            'total': [],
        }
        
        for estacao in estacoes_moveis:
            label = f"{estacao.trimestre} {estacao.ano}"
            if label not in context['estacoes_moveis_data']['labels']:
                context['estacoes_moveis_data']['labels'].append(label)
                context['estacoes_moveis_data']['mtn'].append(0)
                context['estacoes_moveis_data']['orange'].append(0)
                context['estacoes_moveis_data']['total'].append(0)
            
            index = context['estacoes_moveis_data']['labels'].index(label)
            
            if estacao.operadora.nome.lower() == 'mtn':
                context['estacoes_moveis_data']['mtn'][index] += estacao.numero_estacoes
            elif estacao.operadora.nome.lower() == 'orange':
                context['estacoes_moveis_data']['orange'][index] += estacao.numero_estacoes
            
            context['estacoes_moveis_data']['total'][index] += estacao.numero_estacoes
        
        # Convertendo os dados em JSON para passar para o template
        json_data = json.dumps(context['estacoes_moveis_data'])
        context['estacoes_moveis_data'] = json_data
        print(json_data)  # Adicione este print para verificar os dados no console do servidor
        
        return context


logger = logging.getLogger(__name__)

class EmpregoSetorView(TemplateView):
    template_name = 'indicadores/emprego_sector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar os dados mais recentes
        latest_data = EmpregoSetor.objects.order_by('-ano', '-trimestre')
        
        emprego_data = {}
        for operadora in Operadora.objects.all():
            data = latest_data.filter(operadora=operadora).first()
            if data:
                emprego_data[operadora.nome.lower()] = {
                    'direto': data.emprego_direto,
                    'nacionais': data.nacionais,
                    'homem': data.homens,
                    'mulher': data.mulheres,
                    'indireto': data.emprego_indireto,
                }
                logger.info(f"Dados encontrados para {operadora.nome}: {emprego_data[operadora.nome.lower()]}")
            else:
                logger.warning(f"Nenhum dado encontrado para {operadora.nome}")
                emprego_data[operadora.nome.lower()] = {
                    'direto': 0, 'nacionais': 0, 'homem': 0, 'mulher': 0, 'indireto': 0
                }

        context['emprego_data'] = mark_safe(json.dumps(emprego_data))
        return context


class TrafegoNacionalView(TemplateView):
    template_name = 'indicadores/trafego_nacional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trafego = TrafegoNacional.objects.all().order_by('ano', 'trimestre')
    
        trafego_data = {
            'labels': [],
            'originadas': {
                'on_net': [], 'off_net': [], 'saida_internacional': [], 'total': []
            },
            'terminadas': {
                'off_net_entrada': [], 'entrada_internacional': [], 'total': []
            },
            'roaming': {
                'in': [], 'out': [], 'total': []
            }
        }
        
        for t in trafego:
            label = f"{t.trimestre} {t.ano}"
            trafego_data['labels'].append(label)
            
            # Chamadas Originadas
            trafego_data['originadas']['on_net'].append(t.on_net)
            trafego_data['originadas']['off_net'].append(t.off_net)
            trafego_data['originadas']['saida_internacional'].append(t.saida_internacional)
            trafego_data['originadas']['total'].append(t.total_originadas)
            
            # Chamadas Terminadas
            trafego_data['terminadas']['off_net_entrada'].append(t.off_net_entrada)
            trafego_data['terminadas']['entrada_internacional'].append(t.entrada_internacional)
            trafego_data['terminadas']['total'].append(t.total_terminadas)
            
            # Roaming
            trafego_data['roaming']['in'].append(t.roaming_in)
            trafego_data['roaming']['out'].append(t.roaming_out)
            trafego_data['roaming']['total'].append(t.total_roaming)
        
        context['trafego_data'] = mark_safe(json.dumps(trafego_data))
        return context


class QuotaMercadoView(TemplateView):
    template_name = 'indicadores/quota_mercado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todos os registros de QuotaMercado ordenados por ano e trimestre
        quotas = QuotaMercado.objects.order_by('ano', 'trimestre')
        
        # Inicializar o dicionário para armazenar os dados de quota
        quota_data = {
            'labels': [],
            'mtn': [],
            'orange': [],
        }
        
        current_label = ''
        mtn_quota = 0
        orange_quota = 0
        
        # Iterar sobre todos os registros de quota
        for q in quotas:
            # Criar um rótulo para o período atual
            label = f"{q.trimestre} {q.ano}"
            
            # Se o rótulo mudou, adicionar os dados do período anterior ao dicionário
            if label != current_label:
                if current_label:
                    quota_data['labels'].append(current_label)
                    quota_data['mtn'].append(mtn_quota)
                    quota_data['orange'].append(orange_quota)
                
                # Resetar para o novo período
                current_label = label
                mtn_quota = 0
                orange_quota = 0
            
            # Atribuir a quota ao operador correto
            if q.operadora.nome.lower() == 'mtn':
                mtn_quota = float(q.quota_estacoes_moveis)
            elif q.operadora.nome.lower() == 'orange':
                orange_quota = float(q.quota_estacoes_moveis)
        
        # Adicionar o último conjunto de dados após o loop
        if current_label:
            quota_data['labels'].append(current_label)
            quota_data['mtn'].append(mtn_quota)
            quota_data['orange'].append(orange_quota)
        
        # Adicionar os dados de quota ao contexto, convertendo para JSON
        context['quota_data'] = mark_safe(json.dumps(quota_data))
        
        return context


class TaxaPenetracaoView(TemplateView):
    template_name = 'indicadores/taxa_penetracao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taxas = TaxaPenetracao.objects.order_by('ano', 'trimestre')
        
        taxa_data = {
            'labels': [],
            'numero_estacoes': [],
            'variacao': [],
            'taxa_penetracao': [],
            'numero_estacoes_3g': [],
            'variacao_3g': [],
            'taxa_penetracao_3g': [],
            'numero_estacoes_4g': [],
            'variacao_4g': [],
            'taxa_penetracao_4g': [],
        }
        
        for t in taxas:
            label = f"{t.trimestre} {t.ano}"
            taxa_data['labels'].append(label)
            taxa_data['numero_estacoes'].append(t.numero_estacoes)
            taxa_data['variacao'].append(t.variacao)
            taxa_data['taxa_penetracao'].append(float(t.taxa_penetracao))
            taxa_data['numero_estacoes_3g'].append(t.numero_estacoes_3g)
            taxa_data['variacao_3g'].append(t.variacao_3g)
            taxa_data['taxa_penetracao_3g'].append(float(t.taxa_penetracao_3g))
            taxa_data['numero_estacoes_4g'].append(t.numero_estacoes_4g)
            taxa_data['variacao_4g'].append(t.variacao_4g)
            taxa_data['taxa_penetracao_4g'].append(float(t.taxa_penetracao_4g))
        
        context['taxa_data'] = mark_safe(json.dumps(taxa_data))
        return context


class VolumeNegocioView(TemplateView):
    template_name = 'indicadores/volume_negocio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volumes = VolumeNegocio.objects.order_by('ano', 'trimestre')
        
        volume_data = {
            'labels': [],
            'mtn': [],
            'orange': [],
            'total': [],
        }
        
        for v in volumes:
            label = f"{v.trimestre} {v.ano}"
            volume_data['labels'].append(label)
            volume_data['mtn'].append(float(v.volume_mtn))
            volume_data['orange'].append(float(v.volume_orange))
            volume_data['total'].append(float(v.volume_mtn + v.volume_orange))
        
        context['volume_data'] = mark_safe(json.dumps(volume_data))
        return context