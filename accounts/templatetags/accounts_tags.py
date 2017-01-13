from django import template

register = template.Library()

@register.simple_tag()
def field_validation_states(filed_error):
    if filed_error:
        return "has-error has-feedback"
    else:
        return "has-feedback"

