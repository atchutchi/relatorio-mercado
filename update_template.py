import os
import re
import fileinput

# Caminho para o template 
template_path = 'dados_anuais/templates/dados_anuais/annual_report.html'
js_path = 'dados_anuais/static/js/annual_report.js'

# Padrões a serem substituídos no HTML
html_replacements = [
    # Corrigir referências de mercado_movel para mercado
    (r'dados_mercado\.mercado_movel', 'dados_mercado.mercado'),
    
    # Atualizar referências de emprego
    (r'dados_mercado\.emprego\.empregos_diretos', 'dados_mercado.emprego.emprego_total'),
    (r'dados_mercado\.emprego\.funcionarios_nacionais', 'dados_mercado.emprego.emprego_homens'),
    (r'dados_mercado\.emprego\.funcionarios_estrangeiros', 'dados_mercado.emprego.emprego_mulheres'),
    
    # Atualizar referências de tráfego
    (r'dados_mercado\.trafego\.voz\.on_net', 'dados_mercado.trafego.trafego_voz_on_net'),
    (r'dados_mercado\.trafego\.voz\.off_net', 'dados_mercado.trafego.trafego_voz_off_net'),
    (r'dados_mercado\.trafego\.voz\.por_operadora', 'dados_mercado.trafego.trafego_voz_on_net')
]

# Padrões a serem substituídos no JavaScript
js_replacements = [
    # Corrigir referências de mercado_movel para mercado
    (r'window\.appData\.mercado_movel', 'window.appData.mercado'),
    
    # Atualizar referências nas funções de renderização de gráficos
    (r'emprego\.empregos_diretos', 'emprego.total'),
    (r'emprego\.funcionarios_nacionais', 'emprego.homens'),
    (r'emprego\.funcionarios_estrangeiros', 'emprego.mulheres'),
    
    # Atualizar outras referências
    (r'trafego\.voz\.on_net', 'trafego.trafego_voz_on_net'),
    (r'trafego\.voz\.off_net', 'trafego.trafego_voz_off_net')
]

# Ler o template HTML e fazer substituições
print(f"Atualizando template HTML: {template_path}")
with fileinput.FileInput(template_path, inplace=True, backup='.bak') as file:
    for line in file:
        for old, new in html_replacements:
            line = re.sub(old, new, line)
        print(line, end='')

# Ler o arquivo JavaScript e fazer substituições
print(f"Atualizando JavaScript: {js_path}")
with fileinput.FileInput(js_path, inplace=True, backup='.bak') as file:
    for line in file:
        for old, new in js_replacements:
            line = re.sub(old, new, line)
        print(line, end='')

print(f"Template e JavaScript atualizados com sucesso!") 