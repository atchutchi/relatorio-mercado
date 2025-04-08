import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relatorio_mercado.relatorio_mercado.settings')
django.setup()

from django.db import connection

def execute_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        return None

# Verificar operadoras existentes
operadoras = execute_sql("SELECT * FROM dados_anuais_operadora;")
print("Operadoras existentes:", operadoras)

# Criar um mapeamento de nome para ID
operadora_map = {}
for op in operadoras:
    operadora_map[op[1]] = op[0]  # nome -> id

print("Mapeamento de operadoras:", operadora_map)

# Criar uma tabela temporária
execute_sql("""
CREATE TABLE dados_anuais_dadosanuais_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano INTEGER NOT NULL,
    operadora_id INTEGER NOT NULL,
    assinantes_rede_movel INTEGER,
    assinantes_pos_pago INTEGER,
    assinantes_pre_pago INTEGER,
    utilizacao_efetiva INTEGER,
    assinantes_banda_larga_movel INTEGER,
    assinantes_3g INTEGER,
    assinantes_3g_box INTEGER,
    assinantes_3g_usb INTEGER,
    assinantes_4g INTEGER,
    assinantes_4g_box INTEGER,
    assinantes_4g_usb INTEGER,
    assinantes_banda_larga_fixa INTEGER,
    banda_larga_256kbps INTEGER,
    banda_larga_256k_2m INTEGER,
    banda_larga_2m_4m INTEGER,
    banda_larga_5m_10m INTEGER,
    banda_larga_10m INTEGER,
    banda_larga_outros INTEGER,
    investimentos DECIMAL,
    trafego_voz_originado BIGINT,
    trafego_voz_on_net BIGINT,
    trafego_voz_off_net BIGINT,
    trafego_voz_numeros_curtos BIGINT,
    trafego_voz_internacional BIGINT,
    trafego_sms BIGINT,
    trafego_sms_on_net BIGINT,
    trafego_sms_off_net BIGINT,
    trafego_sms_internacional BIGINT,
    trafego_dados BIGINT,
    trafego_dados_2g BIGINT,
    trafego_dados_3g BIGINT,
    trafego_dados_3g_box BIGINT,
    trafego_dados_3g_usb BIGINT,
    trafego_dados_4g BIGINT,
    trafego_dados_4g_box BIGINT,
    trafego_dados_4g_usb BIGINT,
    chamadas_originadas BIGINT,
    chamadas_originadas_on_net BIGINT,
    chamadas_originadas_off_net BIGINT,
    chamadas_originadas_numeros_curtos BIGINT,
    chamadas_originadas_internacional BIGINT,
    trafego_voz_terminado BIGINT,
    trafego_voz_terminado_off_net BIGINT,
    trafego_voz_terminado_internacional BIGINT,
    trafego_sms_terminado BIGINT,
    trafego_sms_terminado_off_net BIGINT,
    trafego_sms_terminado_internacional BIGINT,
    chamadas_terminadas BIGINT,
    chamadas_terminadas_off_net BIGINT,
    chamadas_terminadas_internacional BIGINT,
    roaming_in_minutos INTEGER,
    roaming_out_minutos INTEGER,
    roaming_in_chamadas INTEGER,
    roaming_out_chamadas INTEGER,
    volume_internet_nacional BIGINT,
    volume_internet_internacional BIGINT,
    trafego_sms_roaming_in INTEGER,
    trafego_sms_roaming_out INTEGER,
    receita_total DECIMAL,
    receita_servicos_voz DECIMAL,
    receita_roaming_out DECIMAL,
    receita_servicos_mensagens DECIMAL,
    receita_dados_moveis DECIMAL,
    receita_chamadas_originadas DECIMAL,
    receita_chamadas_on_net DECIMAL,
    receita_chamadas_off_net DECIMAL,
    receita_chamadas_internacional DECIMAL,
    receita_chamadas_terminadas DECIMAL,
    receita_chamadas_terminadas_off_net DECIMAL,
    receita_chamadas_terminadas_internacional DECIMAL,
    receita_mobile_money DECIMAL,
    banda_larga_internacional DECIMAL,
    emprego_total INTEGER,
    emprego_homens INTEGER,
    emprego_mulheres INTEGER,
    volume_negocio DECIMAL,
    FOREIGN KEY (operadora_id) REFERENCES dados_anuais_operadora(id)
);
""")

# Inserir dados com conversão de nome para ID
registros = execute_sql("SELECT * FROM dados_anuais_dadosanuais")
for reg in registros:
    id = reg[0]
    ano = reg[1]
    operadora_nome = reg[2]