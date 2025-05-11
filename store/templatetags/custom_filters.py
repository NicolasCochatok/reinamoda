from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter(name='filter_by_category')
def filter_by_category(queryset, category_name):
    return queryset.filter(variation_category=category_name)
