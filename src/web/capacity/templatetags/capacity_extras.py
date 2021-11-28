from django import template

register = template.Library()

@register.filter
def index_of(array, index):
    try:
        return array[index]
    except:
        return None

@register.filter
def property_of(object, property_name: str):
    return object[property_name]