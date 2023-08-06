from django import template
from datetime import date

register = template.Library()

@register.filter
def future_date(value):
    return value >= date.today()
