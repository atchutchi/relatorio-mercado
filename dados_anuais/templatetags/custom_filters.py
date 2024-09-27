from django import template

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