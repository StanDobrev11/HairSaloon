from django import template

register = template.Library()


# this is used to place a text on the field and is used in the HTML template
# should import template.Library() and should used @register.filter decorator
# however, in the template the form must be completed manually
@register.filter
def placeholder(field, token):
    field.field.widget.attrs['placeholder'] = token
    return field
