from django import template
register = template.Library()


@register.simple_tag
def change_str(value):
    if type(value) != str:
        return value
    return "《" + value+"》"

