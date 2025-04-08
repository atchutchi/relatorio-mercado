from django import template
import json as json_lib
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    elif isinstance(obj, (list, tuple)) and isinstance(key, int):
        return obj[key] if 0 <= key < len(obj) else None
    return None

@register.filter
def getattr_filter(obj, attr):
    """
    Permite acessar atributos aninhados de objetos usando notação de ponto.
    Ex: {{ objeto|getattr_filter:"operadora.nome" }}
    """
    if '.' in attr:
        attrs = attr.split('.')
        for a in attrs:
            obj = getattr(obj, a, None)
            if obj is None:
                return None
        return obj
    return getattr(obj, attr, None)

@register.filter
def replace_underscore(value):
    return value.replace('_', ' ').title()

@register.filter(is_safe=True)
def json(value):
    return json_lib.dumps(value)

@register.filter
def percentage(value, total):
    """
    Calcula a porcentagem entre dois números.
    - value: o valor parcial
    - total: o valor total
    Retorna: uma string formatada como "xx.xx%"
    """
    try:
        # Evita divisão por zero e erros de tipo
        if total == 0 or value is None or total is None:
            return "0.00%"
        percentage_value = (float(value) / float(total)) * 100
        return f"{percentage_value:.2f}%"
    except (ValueError, TypeError):
        return "0.00%"

@register.filter
def currency(value, symbol=''):
    """
    Formata um valor como moeda.
    - value: o valor monetário
    - symbol: símbolo monetário opcional (ex: '$', '€')
    Retorna: uma string formatada como "x,xxx.xx" com o símbolo especificado
    """
    try:
        if value is None or value == '':
            return f"{symbol}0,00"
        
        # Converter para Decimal com tratamento de erro mais robusto
        if not isinstance(value, Decimal):
            try:
                value = Decimal(str(value))
            except (ValueError, TypeError, Decimal.InvalidOperation):
                return f"{symbol}0,00"
                
        # Formatação para o padrão brasileiro (vírgula como separador decimal)
        return f"{symbol}{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        # Captura qualquer outro erro que possa ocorrer
        return f"{symbol}0,00"

@register.filter
def format_number(value, decimal_places=0):
    """
    Formata um número com separadores de milhares e casas decimais opcionais.
    - value: o valor a formatar
    - decimal_places: número de casas decimais (padrão: 0)
    """
    try:
        if value is None:
            return "0" if decimal_places == 0 else f"0.{'0' * decimal_places}"
        
        format_str = '{:,.' + str(decimal_places) + 'f}'
        return format_str.format(float(value))
    except (ValueError, TypeError):
        return "0" if decimal_places == 0 else f"0.{'0' * decimal_places}"

@register.filter
def growth_class(value):
    """
    Retorna uma classe CSS com base no valor de crescimento,
    para estilizar valores positivos e negativos diferentemente.
    """
    try:
        value = float(value)
        if value > 0:
            return "positive-growth"
        elif value < 0:
            return "negative-growth"
        else:
            return "zero-growth"
    except (ValueError, TypeError):
        return "zero-growth"
