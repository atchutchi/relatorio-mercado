from django.views.generic import TemplateView
from .models import EstacoesMoveisEfetivas, EmpregoSetor, TrafegoNacional, QuotaMercado, TaxaPenetracao, VolumeNegocio
import json
from django.utils.safestring import mark_safe


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


class EmpregoSetorView(TemplateView):
    template_name = 'indicadores/emprego_sector.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_data = EmpregoSetor.objects.order_by('-ano', '-trimestre')
       
        if latest_data.exists():
            mtn_data = latest_data.filter(operadora__nome='MTN').first()
            orange_data = latest_data.filter(operadora__nome='Orange').first()
            
            emprego_data = {
                'mtn': {
                    'direto': mtn_data.emprego_direto if mtn_data else 0,
                    'nacionais': mtn_data.nacionais if mtn_data else 0,
                    'homem': mtn_data.homens if mtn_data else 0,
                    'mulher': mtn_data.mulheres if mtn_data else 0,
                    'indireto': mtn_data.emprego_indireto if mtn_data else 0,
                },
                'orange': {
                    'direto': orange_data.emprego_direto if orange_data else 0,
                    'nacionais': orange_data.nacionais if orange_data else 0,
                    'homem': orange_data.homens if orange_data else 0,
                    'mulher': orange_data.mulheres if orange_data else 0,
                    'indireto': orange_data.emprego_indireto if orange_data else 0,
                },
            }
        json_data = json.dumps(emprego_data)
        context['emprego_data'] = mark_safe(json_data)
        return context


class TrafegoNacionalView(TemplateView):
    template_name = 'indicadores/trafego_nacional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trafego = TrafegoNacional.objects.order_by('ano', 'trimestre')
    
        context['trafego_data'] = {
            'labels': [],
            'on_net': [],
            'off_net': [],
            'saida_internacional': [],
            'entrada_internacional': [],
            'roaming_in': [],
            'roaming_out': [],
        }
        
        for t in trafego:
            label = f"{t.trimestre} {t.ano}"
            context['trafego_data']['labels'].append(label)
            context['trafego_data']['on_net'].append(t.trafego_on_net)
            context['trafego_data']['off_net'].append(t.trafego_off_net)
            context['trafego_data']['saida_internacional'].append(t.trafego_internacional_saida)
            context['trafego_data']['entrada_internacional'].append(t.trafego_internacional_entrada)
            context['trafego_data']['roaming_in'].append(t.trafego_roaming_in)
            context['trafego_data']['roaming_out'].append(t.trafego_roaming_out)
        
        return context


import json
from django.utils.safestring import mark_safe

class QuotaMercadoView(TemplateView):
    template_name = 'indicadores/quota_mercado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotas = QuotaMercado.objects.order_by('ano', 'trimestre')
        
        quota_data = {
            'labels': [],
            'mtn': [],
            'orange': [],
        }
        
        for q in quotas:
            label = f"{q.trimestre} {q.ano}"
            quota_data['labels'].append(label)
            if q.operadora.nome.lower() == 'mtn':
                quota_data['mtn'].append(float(q.quota_estacoes_moveis))
                quota_data['orange'].append(0)
            elif q.operadora.nome.lower() == 'orange':
                quota_data['mtn'].append(0)
                quota_data['orange'].append(float(q.quota_estacoes_moveis))
        
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