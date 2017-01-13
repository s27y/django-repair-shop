import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    print context['request'].path, pattern_or_urlname
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
        print "except"
    path = context['request'].path
    print pattern,path
    if re.search(pattern, path)  :
        return 'active'
    return ''

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')
