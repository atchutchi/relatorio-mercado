from import_export import resources, fields
from import_export.widgets import IntegerWidget, DecimalWidget
from .models import DadosAnuais

class DadosAnuaisResource(resources.ModelResource):
    ano = fields.Field(attribute='ano', column_name='Ano')
    operadora = fields.Field(attribute='operadora', column_name='Operadora')

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
        skip_unchanged = True
        report_skipped = False

    def before_import_row(self, row, **kwargs):
        # Identificar o ano a partir das colunas
        year_columns = [col for col in row.keys() if col and col.isdigit()]
        if not year_columns:
            return False  # Pula linhas que não têm ano

        # Processamento para cada ano
        for year in year_columns:
            new_row = row.copy()
            new_row['Ano'] = year
            
            # Identificar a operadora
            if 'Indicadores' in new_row:
                if 'ORANGE' in new_row['Indicadores'].upper():
                    new_row['Operadora'] = 'ORANGE'
                elif 'MTN' in new_row['Indicadores'].upper():
                    new_row['Operadora'] = 'MTN'
                elif 'TOTAL' in new_row['Indicadores'].upper():
                    new_row['Operadora'] = 'TOTAL'
                else:
                    return False  # Pula linhas sem operadora identificável

            # Mapeamento de colunas
            for field in self.fields:
                if field not in ['ano', 'operadora']:
                    column_name = self.fields[field].column_name
                    if column_name in new_row:
                        # Permitir campos vazios ao definir o valor como None se estiver vazio
                        new_row[field] = new_row[column_name] if new_row[column_name] != '' else None

            # Adiciona a nova linha processada
            if 'dataset' in kwargs:
                kwargs['dataset'].append(new_row)

        # Retorna False para pular a linha original
        return False

    def get_instance(self, instance_loader, row):
        try:
            params = {}
            for key in self.get_import_id_fields():
                field = self.fields[key]
                params[field.attribute] = field.clean(row)
            return self.get_queryset().get(**params)
        except Exception:
            return None
