from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Divide la cadena 'value' utilizando el delimitador 'key'.
    """
    return value.split(key)
