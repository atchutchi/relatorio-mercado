from django import template
import json as json_lib

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
    return getattr(obj, attr)

@register.filter
def replace_underscore(value):
    return value.replace('_', ' ')

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
        return f"{percentage_value:.2f}"
    except (ValueError, TypeError):
        return "0.00%"
