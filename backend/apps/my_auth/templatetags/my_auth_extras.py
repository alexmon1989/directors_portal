from django import template

register = template.Library()


@register.simple_tag
def get_field_placeholder_attr(value):
    return f"placeholder:{value}"
