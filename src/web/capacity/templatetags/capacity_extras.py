from django import template

register = template.Library()

@register.filter
def index_of(array, index):
    return array[index]