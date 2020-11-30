from django import template

register = template.Library()


@register.filter
def currency(value, cur="GH¢"):
    return f"<span class='currency'>{cur}</span>{value}"
