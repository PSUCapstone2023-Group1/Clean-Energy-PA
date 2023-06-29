from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def string(value):
    return str(value)

@register.filter
def format_rate(value):
    output = f"${str(abs(value))[:8]}"
    if(value<0):
        return output + " more than"
    else:
        return output + " less than"