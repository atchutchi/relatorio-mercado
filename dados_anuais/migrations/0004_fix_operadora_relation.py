from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('dados_anuais', '0003_alter_dadosanuais_operadora'),
    ]

    operations = [
        # Certifique-se de que existem registros na tabela operadora
        migrations.RunSQL(
            """
            INSERT OR IGNORE INTO dados_anuais_operadora (id, nome, codigo)
            VALUES 
                (1, 'MTN', 'MTN123'),
                (2, 'ORANGE', 'ORG456');
            """,
            "DELETE FROM dados_anuais_operadora WHERE nome IN ('MTN', 'ORANGE');"
        ),
        
        # Renomear a tabela e criar uma nova com operadora_id
        migrations.RunSQL(
            """
            -- Criar tabela temporária com a nova estrutura
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
            
            -- Copiar os dados, traduzindo o nome da operadora para o ID
            INSERT INTO dados_anuais_dadosanuais_new 
            SELECT 
                d.id, d.ano,
                CASE 
                    WHEN d.operadora = 'MTN' THEN 1 
                    WHEN d.operadora = 'ORANGE' THEN 2
                    ELSE NULL
                END as operadora_id,
                d.assinantes_rede_movel, d.assinantes_pos_pago, d.assinantes_pre_pago,
                d.utilizacao_efetiva, d.assinantes_banda_larga_movel, d.assinantes_3g,
                d.assinantes_3g_box, d.assinantes_3g_usb, d.assinantes_4g, d.assinantes_4g_box,
                d.assinantes_4g_usb, d.assinantes_banda_larga_fixa, d.banda_larga_256kbps,
                d.banda_larga_256k_2m, d.banda_larga_2m_4m, d.banda_larga_5m_10m, d.banda_larga_10m,
                d.banda_larga_outros, d.investimentos, d.trafego_voz_originado, d.trafego_voz_on_net,
                d.trafego_voz_off_net, d.trafego_voz_numeros_curtos, d.trafego_voz_internacional,
                d.trafego_sms, d.trafego_sms_on_net, d.trafego_sms_off_net, d.trafego_sms_internacional,
                d.trafego_dados, d.trafego_dados_2g, d.trafego_dados_3g, d.trafego_dados_3g_box,
                d.trafego_dados_3g_usb, d.trafego_dados_4g, d.trafego_dados_4g_box, d.trafego_dados_4g_usb,
                d.chamadas_originadas, d.chamadas_originadas_on_net, d.chamadas_originadas_off_net,
                d.chamadas_originadas_numeros_curtos, d.chamadas_originadas_internacional,
                d.trafego_voz_terminado, d.trafego_voz_terminado_off_net, d.trafego_voz_terminado_internacional,
                d.trafego_sms_terminado, d.trafego_sms_terminado_off_net, d.trafego_sms_terminado_internacional,
                d.chamadas_terminadas, d.chamadas_terminadas_off_net, d.chamadas_terminadas_internacional,
                d.roaming_in_minutos, d.roaming_out_minutos, d.roaming_in_chamadas, d.roaming_out_chamadas,
                d.volume_internet_nacional, d.volume_internet_internacional, d.trafego_sms_roaming_in,
                d.trafego_sms_roaming_out, d.receita_total, d.receita_servicos_voz, d.receita_roaming_out,
                d.receita_servicos_mensagens, d.receita_dados_moveis, d.receita_chamadas_originadas,
                d.receita_chamadas_on_net, d.receita_chamadas_off_net, d.receita_chamadas_internacional,
                d.receita_chamadas_terminadas, d.receita_chamadas_terminadas_off_net,
                d.receita_chamadas_terminadas_internacional, d.receita_mobile_money, d.banda_larga_internacional,
                d.emprego_total, d.emprego_homens, d.emprego_mulheres, d.volume_negocio
            FROM dados_anuais_dadosanuais d;
            
            -- Substituir a tabela antiga pela nova
            DROP TABLE dados_anuais_dadosanuais;
            ALTER TABLE dados_anuais_dadosanuais_new RENAME TO dados_anuais_dadosanuais;
            """,
            # Não há como reverter isso facilmente
            migrations.RunSQL.noop
        ),
    ]