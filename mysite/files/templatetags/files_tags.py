# coding: utf-8

from django import template
from django.utils.http import urlquote


register = template.Library()


@register.inclusion_tag('files/include/_response.html', takes_context=True)
def query_string(context, cite_string):
    """
    Allows a brief citation of query string parameters.

    _response.html is just {{ response }}

    Usage:
    http://www.url.com/{% query_string "dir,q" %}
    """

    # Written as an inclusion tag to simplify getting the context.
    params = context['query'].copy()
    # print(params, type(params))
    cite_list = string_to_list(cite_string)
    response = get_query_string(params, cite_list)
    return {'response': response}

'''
def query_helper(query, add=None, remove=None):
    """
    Helper Function for use within views.
    """

    add = string_to_dict(add)
    remove = string_to_list(remove)
    params = query.copy()
    return get_query_string(params, add, remove)
'''


def get_query_string(p, cite_list):
    return '?' + '&'.join([u'%s=%s' % (urlquote(k), urlquote(v)) for k, v in p.items()])

'''
def string_to_dict(string):
    """
    Usage:
        {{ url|thumbnail:"width=10,height=20" }}
        {{ url|thumbnail:"width=10" }}
        {{ url|thumbnail:"height=20" }}
    """

    kwargs = {}
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '':
                continue
            kw, val = arg.split('=', 1)
            kwargs[kw] = val
    return kwargs
'''


def string_to_list(string):
    """
    Usage:
        {{ url|thumbnail:"width,height" }}
    """

    args = []
    if string:
        string = str(string)
        if ',' not in string:
            # ensure at least one ','
            string += ','
        for arg in string.split(','):
            arg = arg.strip()
            if arg == '':
                continue
            args.append(arg)
    return args

