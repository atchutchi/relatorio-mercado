from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def getattr_filter(obj, attr):
    return getattr(obj, attr)

@register.filter
def replace_underscore(value):
    return value.replace('_', ' ')