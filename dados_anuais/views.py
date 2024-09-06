from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from openpyxl import Workbook
import json
from .models import DadosAnuais
from .resource import DadosAnuaisResource
from .tasks import process_excel_upload

logger = logging.getLogger(__name__)

class DadosAnuaisListView(ListView):
    model = DadosAnuais
    template_name = 'dados_anuais/dados_anuais_list.html'
    context_object_name = 'dados_anuais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter dados totais por ano
        dados_totais = DadosAnuais.objects.filter(operadora='TOTAL').order_by('ano')
        
        # Definir todos os campos do modelo
        campos = [f.name for f in DadosAnuais._meta.get_fields() if f.name != 'id']
        
        # Preparar dados para gráficos
        context['dados_graficos'] = {
            'anos': [d.ano for d in dados_totais],
            **{campo: [getattr(d, campo) for d in dados_totais] for campo in campos if campo != 'ano' and campo != 'operadora'}
        }
        
        # Calcular algumas estatísticas gerais
        context['estatisticas'] = {
            'total_assinantes': dados_totais.last().assinantes_rede_movel if dados_totais else 0,
            'crescimento_assinantes': self.calcular_crescimento(dados_totais, 'assinantes_rede_movel'),
            'volume_negocio_atual': dados_totais.last().volume_negocio if dados_totais else 0,
            'crescimento_volume_negocio': self.calcular_crescimento(dados_totais, 'volume_negocio'),
        }
        
        context['campos'] = campos
        
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
        dados_ano = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
        if dados_ano:
            for indicador in indicadores:
                dados_evolucao[indicador].append(getattr(dados_ano, indicador))

    context = {
        'anos': list(anos),
        'dados_evolucao': dados_evolucao,
        'indicadores': indicadores
    }

    return render(request, 'dados_anuais/evolucao_indicadores.html', context)


def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def upload_excel(request):
    if request.method == 'POST':
        new_dados = request.FILES['myfile']
        file_path = default_storage.save('tmp/excel_upload.xlsx', ContentFile(new_dados.read()))
        task = process_excel_upload.delay(file_path)
        messages.info(request, f'Upload iniciado. ID da tarefa: {task.id}')
    return render(request, 'dados_anuais/upload_excel.html')

def download_template(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Template DadosAnuais"
    headers = [
        'Ano', 'Operadora',
        'Assinantes rede movel', 'Pos-pago', 'Pre-pago', 'Utilização efetiva',
        'Assinantes Banda Larga Movel', '3G', 'dos quais com ligação através de Placas (Box) 3G',
        'dos quais com ligação através de Placas (USB) 3G', '4G',
        'dos quais com ligação através de Placas (Box) 4G', 'dos quais com ligação através de Placas (USB) 4G',
        'Assinantes Internet Banda Larga Fixa via Radio', 'Banda Larga ≥ 256 Kbps',
        '256 Kbit/s - 2 Mbit/s', '2 - 4 Mbit/s', '5-10 Mbit/s', '10 Mbit/s', 'Outros (10+ Mbit/s)',
        'Velume de Negocio', 'Investimentos no setor',
        'Voz', 'On-Net', 'Off-Net', 'Numeros curtos e numeros não geograficos', 'Operadores das redes Internacionais',
        'SMS', 'On-Net SMS', 'Off-Net SMS', 'Operadores das redes Internacionais SMS',
        'Dados tráfego', '2G', '3G', 'Atraves de placa modem(BOX) 3G', 'Atraves de placa modem(USB) 3G',
        '4G', 'Atraves de placa modem(BOX) 4G', 'Atraves de placa modem(USB) 4G',
        'Nº Chamadas originada(saida)', 'On-Net Chamadas', 'Off-Net Chamadas',
        'Numeros curtos e numeros não geograficos Chamadas', 'Operadores das redes Internacionais Chamadas',
        'Voz Terminada', 'Off-Net Terminada', 'Operadores das redes Internacionais Terminada',
        'SMS Terminado', 'Off-Net SMS Terminado', 'Operadores das redes Internacionais SMS Terminado',
        'Nº Chamadas terminada(entrada)', 'Off-Net Chamadas Terminadas', 'Operadores das redes Internacionais Chamadas Terminadas',
        'IN', 'OUT', 'IN Chamadas', 'OUT Chamadas',
        'Volume de acesso a Internet dentro do pais(Mbit)', 'Volume de acesso a Internet fora do pais(Mbit)',
        'IN SMS', 'OUT SMS',
        'Receita', 'Receitas de serviços de voz', 'Receitas de serviços de voz em Roaming-out',
        'Receitas de serviços de mensagens', 'Receitas de serviços de dados móveis',
        'Receita de chamadas Originadas de voz', 'Receitas de chamadas On-net', 'Receitas de chamadas Off-net',
        'Receitas de chamadas Internacional', 'Receita de chamadasTerminadas de voz',
        'Receitas de chamadas Off-net Terminadas', 'Receitas de chamadas Internacional Terminadas',
        'Receita Transferencia Mobile Money', 'Banda Larga Internacional(BLI)',
        'Emprego', 'Homens', 'Mulheres'
    ]
    ws.append(headers)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=dados_anuais_template.xlsx'
    wb.save(response)
    return response