from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def format_rate(value, length):
    return f"${str(abs(value)).ljust(length, '0')[:length]}"

@register.filter
def format_rate_diff(value, length):
    if(value<0):
        return format_rate(value, length) + " more than"
    else:
        return format_rate(value, length) + " less than"
    
@register.filter
def format_contract_length(value):
    if "months" not in value.lower():
        return f"{value} months"
    else:
        return value