from import_export import resources, fields
from import_export.widgets import IntegerWidget, DecimalWidget
from .models import DadosAnuais

class DadosAnuaisResource(resources.ModelResource):
    ano = fields.Field(attribute='ano', column_name='Ano', widget=IntegerWidget())
    operadora = fields.Field(attribute='operadora', column_name='Operadora')
    assinantes_rede_movel = fields.Field(attribute='assinantes_rede_movel', column_name='Assinantes rede movel', widget=IntegerWidget())
    assinantes_pos_pago = fields.Field(attribute='assinantes_pos_pago', column_name='Pos-pago', widget=IntegerWidget())
    assinantes_pre_pago = fields.Field(attribute='assinantes_pre_pago', column_name='Pre-pago', widget=IntegerWidget())
    utilizacao_efetiva = fields.Field(attribute='utilizacao_efetiva', column_name='Utilização efetiva', widget=IntegerWidget())
    assinantes_banda_larga_movel = fields.Field(attribute='assinantes_banda_larga_movel', column_name='Assinantes Banda Larga Movel', widget=IntegerWidget())
    assinantes_3g = fields.Field(attribute='assinantes_3g', column_name='3G', widget=IntegerWidget())
    assinantes_3g_box = fields.Field(attribute='assinantes_3g_box', column_name='dos quais com ligação através de Placas (Box) 3G', widget=IntegerWidget())
    assinantes_3g_usb = fields.Field(attribute='assinantes_3g_usb', column_name='dos quais com ligação através de Placas (USB) 3G', widget=IntegerWidget())
    assinantes_4g = fields.Field(attribute='assinantes_4g', column_name='4G', widget=IntegerWidget())
    assinantes_4g_box = fields.Field(attribute='assinantes_4g_box', column_name='dos quais com ligação através de Placas (Box) 4G', widget=IntegerWidget())
    assinantes_4g_usb = fields.Field(attribute='assinantes_4g_usb', column_name='dos quais com ligação através de Placas (USB) 4G', widget=IntegerWidget())
    assinantes_banda_larga_fixa = fields.Field(attribute='assinantes_banda_larga_fixa', column_name='Assinantes Internet Banda Larga Fixa via Radio', widget=IntegerWidget())
    banda_larga_256kbps = fields.Field(attribute='banda_larga_256kbps', column_name='Banda Larga ≥ 256 Kbps', widget=IntegerWidget())
    banda_larga_256k_2m = fields.Field(attribute='banda_larga_256k_2m', column_name='256 Kbit/s - 2 Mbit/s', widget=IntegerWidget())
    banda_larga_2m_4m = fields.Field(attribute='banda_larga_2m_4m', column_name='2 - 4 Mbit/s', widget=IntegerWidget())
    banda_larga_5m_10m = fields.Field(attribute='banda_larga_5m_10m', column_name='5-10 Mbit/s', widget=IntegerWidget())
    banda_larga_10m = fields.Field(attribute='banda_larga_10m', column_name='10 Mbit/s', widget=IntegerWidget())
    banda_larga_outros = fields.Field(attribute='banda_larga_outros', column_name='Outros (10+ Mbit/s)', widget=IntegerWidget())
    volume_negocio = fields.Field(attribute='volume_negocio', column_name='Velume de Negocio', widget=DecimalWidget())
    investimentos = fields.Field(attribute='investimentos', column_name='Investimentos no setor', widget=DecimalWidget())
    trafego_voz_originado = fields.Field(attribute='trafego_voz_originado', column_name='Voz', widget=IntegerWidget())
    trafego_voz_on_net = fields.Field(attribute='trafego_voz_on_net', column_name='On-Net', widget=IntegerWidget())
    trafego_voz_off_net = fields.Field(attribute='trafego_voz_off_net', column_name='Off-Net', widget=IntegerWidget())
    trafego_voz_numeros_curtos = fields.Field(attribute='trafego_voz_numeros_curtos', column_name='Numeros curtos e numeros não geograficos', widget=IntegerWidget())
    trafego_voz_internacional = fields.Field(attribute='trafego_voz_internacional', column_name='Operadores das redes Internacionais', widget=IntegerWidget())
    trafego_sms = fields.Field(attribute='trafego_sms', column_name='SMS', widget=IntegerWidget())
    trafego_sms_on_net = fields.Field(attribute='trafego_sms_on_net', column_name='On-Net SMS', widget=IntegerWidget())
    trafego_sms_off_net = fields.Field(attribute='trafego_sms_off_net', column_name='Off-Net SMS', widget=IntegerWidget())
    trafego_sms_internacional = fields.Field(attribute='trafego_sms_internacional', column_name='Operadores das redes Internacionais SMS', widget=IntegerWidget())
    trafego_dados = fields.Field(attribute='trafego_dados', column_name='Dados tráfego', widget=IntegerWidget())
    trafego_dados_2g = fields.Field(attribute='trafego_dados_2g', column_name='2G', widget=IntegerWidget())
    trafego_dados_3g = fields.Field(attribute='trafego_dados_3g', column_name='3G', widget=IntegerWidget())
    trafego_dados_3g_box = fields.Field(attribute='trafego_dados_3g_box', column_name='Atraves de placa modem(BOX) 3G', widget=IntegerWidget())
    trafego_dados_3g_usb = fields.Field(attribute='trafego_dados_3g_usb', column_name='Atraves de placa modem(USB) 3G', widget=IntegerWidget())
    trafego_dados_4g = fields.Field(attribute='trafego_dados_4g', column_name='4G', widget=IntegerWidget())
    trafego_dados_4g_box = fields.Field(attribute='trafego_dados_4g_box', column_name='Atraves de placa modem(BOX) 4G', widget=IntegerWidget())
    trafego_dados_4g_usb = fields.Field(attribute='trafego_dados_4g_usb', column_name='Atraves de placa modem(USB) 4G', widget=IntegerWidget())
    chamadas_originadas = fields.Field(attribute='chamadas_originadas', column_name='Nº Chamadas originada(saida)', widget=IntegerWidget())
    chamadas_originadas_on_net = fields.Field(attribute='chamadas_originadas_on_net', column_name='On-Net Chamadas', widget=IntegerWidget())
    chamadas_originadas_off_net = fields.Field(attribute='chamadas_originadas_off_net', column_name='Off-Net Chamadas', widget=IntegerWidget())
    chamadas_originadas_numeros_curtos = fields.Field(attribute='chamadas_originadas_numeros_curtos', column_name='Numeros curtos e numeros não geograficos Chamadas', widget=IntegerWidget())
    chamadas_originadas_internacional = fields.Field(attribute='chamadas_originadas_internacional', column_name='Operadores das redes Internacionais Chamadas', widget=IntegerWidget())
    trafego_voz_terminado = fields.Field(attribute='trafego_voz_terminado', column_name='Voz Terminada', widget=IntegerWidget())
    trafego_voz_terminado_off_net = fields.Field(attribute='trafego_voz_terminado_off_net', column_name='Off-Net Terminada', widget=IntegerWidget())
    trafego_voz_terminado_internacional = fields.Field(attribute='trafego_voz_terminado_internacional', column_name='Operadores das redes Internacionais Terminada', widget=IntegerWidget())
    trafego_sms_terminado = fields.Field(attribute='trafego_sms_terminado', column_name='SMS Terminado', widget=IntegerWidget())
    trafego_sms_terminado_off_net = fields.Field(attribute='trafego_sms_terminado_off_net', column_name='Off-Net SMS Terminado', widget=IntegerWidget())
    trafego_sms_terminado_internacional = fields.Field(attribute='trafego_sms_terminado_internacional', column_name='Operadores das redes Internacionais SMS Terminado', widget=IntegerWidget())
    chamadas_terminadas = fields.Field(attribute='chamadas_terminadas', column_name='Nº Chamadas terminada(entrada)', widget=IntegerWidget())
    chamadas_terminadas_off_net = fields.Field(attribute='chamadas_terminadas_off_net', column_name='Off-Net Chamadas Terminadas', widget=IntegerWidget())
    chamadas_terminadas_internacional = fields.Field(attribute='chamadas_terminadas_internacional', column_name='Operadores das redes Internacionais Chamadas Terminadas', widget=IntegerWidget())
    roaming_in_minutos = fields.Field(attribute='roaming_in_minutos', column_name='IN', widget=IntegerWidget())
    roaming_out_minutos = fields.Field(attribute='roaming_out_minutos', column_name='OUT', widget=IntegerWidget())
    roaming_in_chamadas = fields.Field(attribute='roaming_in_chamadas', column_name='IN Chamadas', widget=IntegerWidget())
    roaming_out_chamadas = fields.Field(attribute='roaming_out_chamadas', column_name='OUT Chamadas', widget=IntegerWidget())
    volume_internet_nacional = fields.Field(attribute='volume_internet_nacional', column_name='Volume de acesso a Internet dentro do pais(Mbit)', widget=IntegerWidget())
    volume_internet_internacional = fields.Field(attribute='volume_internet_internacional', column_name='Volume de acesso a Internet fora do pais(Mbit)', widget=IntegerWidget())
    trafego_sms_roaming_in = fields.Field(attribute='trafego_sms_roaming_in', column_name='IN SMS', widget=IntegerWidget())
    trafego_sms_roaming_out = fields.Field(attribute='trafego_sms_roaming_out', column_name='OUT SMS', widget=IntegerWidget())
    receita_total = fields.Field(attribute='receita_total', column_name='Receita', widget=DecimalWidget())
    receita_servicos_voz = fields.Field(attribute='receita_servicos_voz', column_name='Receitas de serviços de voz', widget=DecimalWidget())
    receita_roaming_out = fields.Field(attribute='receita_roaming_out', column_name='Receitas de serviços de voz em Roaming-out', widget=DecimalWidget())
    receita_servicos_mensagens = fields.Field(attribute='receita_servicos_mensagens', column_name='Receitas de serviços de mensagens', widget=DecimalWidget())
    receita_dados_moveis = fields.Field(attribute='receita_dados_moveis', column_name='Receitas de serviços de dados móveis', widget=DecimalWidget())
    receita_chamadas_originadas = fields.Field(attribute='receita_chamadas_originadas', column_name='Receita de chamadas Originadas de voz', widget=DecimalWidget())
    receita_chamadas_on_net = fields.Field(attribute='receita_chamadas_on_net', column_name='Receitas de chamadas On-net', widget=DecimalWidget())
    receita_chamadas_off_net = fields.Field(attribute='receita_chamadas_off_net', column_name='Receitas de chamadas Off-net', widget=DecimalWidget())
    receita_chamadas_internacional = fields.Field(attribute='receita_chamadas_internacional', column_name='Receitas de chamadas Internacional', widget=DecimalWidget())
    receita_chamadas_terminadas = fields.Field(attribute='receita_chamadas_terminadas', column_name='Receita de chamadasTerminadas de voz', widget=DecimalWidget())
    receita_chamadas_terminadas_off_net = fields.Field(attribute='receita_chamadas_terminadas_off_net', column_name='Receitas de chamadas Off-net Terminadas', widget=DecimalWidget())
    receita_chamadas_terminadas_internacional = fields.Field(attribute='receita_chamadas_terminadas_internacional', column_name='Receitas de chamadas Internacional Terminadas', widget=DecimalWidget())
    receita_mobile_money = fields.Field(attribute='receita_mobile_money', column_name='Receita Transferencia Mobile Money', widget=DecimalWidget())
    banda_larga_internacional = fields.Field(attribute='banda_larga_internacional', column_name='Banda Larga Internacional(BLI)', widget=DecimalWidget())
    emprego_total = fields.Field(attribute='emprego_total', column_name='Emprego', widget=IntegerWidget())
    emprego_homens = fields.Field(attribute='emprego_homens', column_name='Homens', widget=IntegerWidget())
    emprego_mulheres = fields.Field(attribute='emprego_mulheres', column_name='Mulheres', widget=IntegerWidget())

    class Meta:
        model = DadosAnuais
        import_id_fields = ('ano', 'operadora')
        fields = ('ano', 'operadora', 'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
                'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_3g_box', 'assinantes_3g_usb', 'assinantes_4g',
                'assinantes_4g_box', 'assinantes_4g_usb', 'assinantes_banda_larga_fixa', 'banda_larga_256kbps', 'banda_larga_256k_2m',
                'banda_larga_2m_4m', 'banda_larga_5m_10m', 'banda_larga_10m', 'banda_larga_outros', 'volume_negocio', 'investimentos',
                'trafego_voz_originado', 'trafego_voz_on_net', 'trafego_voz_off_net', 'trafego_voz_numeros_curtos',
                'trafego_voz_internacional', 'trafego_sms', 'trafego_sms_on_net', 'trafego_sms_off_net', 'trafego_sms_internacional',
                'trafego_dados', 'trafego_dados_2g', 'trafego_dados_3g', 'trafego_dados_3g_box', 'trafego_dados_3g_usb',
                'trafego_dados_4g', 'trafego_dados_4g_box', 'trafego_dados_4g_usb', 'chamadas_originadas',
                'chamadas_originadas_on_net', 'chamadas_originadas_off_net', 'chamadas_originadas_numeros_curtos',
                'chamadas_originadas_internacional', 'trafego_voz_terminado', 'trafego_voz_terminado_off_net',
                'trafego_voz_terminado_internacional', 'trafego_sms_terminado', 'trafego_sms_terminado_off_net',
                'trafego_sms_terminado_internacional', 'chamadas_terminadas', 'chamadas_terminadas_off_net',
                'chamadas_terminadas_internacional', 'roaming_in_minutos', 'roaming_out_minutos', 'roaming_in_chamadas',
                'roaming_out_chamadas', 'volume_internet_nacional', 'volume_internet_internacional', 'trafego_sms_roaming_in',
                'trafego_sms_roaming_out', 'receita_total', 'receita_servicos_voz', 'receita_roaming_out',
                'receita_servicos_mensagens', 'receita_dados_moveis', 'receita_chamadas_originadas', 'receita_chamadas_on_net',
                'receita_chamadas_off_net', 'receita_chamadas_internacional', 'receita_chamadas_terminadas',
                'receita_chamadas_terminadas_off_net', 'receita_chamadas_terminadas_internacional', 'receita_mobile_money',
                'banda_larga_internacional', 'emprego_total', 'emprego_homens', 'emprego_mulheres')

    def before_import_row(self, row, **kwargs):
        # Validações personalizadas
        if int(row['Ano']) < 2000 or int(row['Ano']) > 2100:
            raise ValueError(f"Ano inválido: {row['Ano']}")
        if row['Operadora'] not in ['MTN', 'ORANGE', 'TOTAL']:
            raise ValueError(f"Operadora inválida: {row['Operadora']}")
        # Adicione mais validações conforme necessário