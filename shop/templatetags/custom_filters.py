# shop/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies value by arg"""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
