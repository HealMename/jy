from django import template
register = template.Library()


@register.simple_tag
def change_str(value):
    if type(value) != str:
        return value
    return "《" + value+"》"


@register.inclusion_tag("tages/page.html")
def page_next(goods, page):
    return {'goods': goods[(page-1)*4:page*4], 'pages': page}

