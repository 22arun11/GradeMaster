from django import template

register = template.Library()

@register.filter
def average(value):
    if not value:
        return 0
    return sum(value) / len(value)