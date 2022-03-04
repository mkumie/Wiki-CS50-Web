from multiprocessing.sharedctypes import Value
from django import template
from django.template.defaultfilters import stringfilter


import markdown as md
import re

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):

    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter
@stringfilter
def doc_title(value):

    ttl = markdown(value)

    title = re.findall("<h1>(.*?)</h1>", ttl)

    return title[0]