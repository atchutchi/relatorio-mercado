import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relatorio_mercado.relatorio_mercado.settings')
django.setup()

from dados_anuais.models import DadosAnuais
from django.db import connection

# Imprimir o modelo
print("Modelo DadosAnuais:")
print("operadora field:", DadosAnuais._meta.get_field('operadora').__class__)

# Verificar a tabela
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(dados_anuais_dadosanuais);")
    print("\nEstrutura da tabela no banco:")
    for col in cursor.fetchall():
        print(col) 