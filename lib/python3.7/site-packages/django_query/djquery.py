# -*- coding: utf-8 -*-

import json


def get_default_valcastfunc(val_cast_type=None):
    if val_cast_type == 'int':
        return 0, int
    elif val_cast_type == 'float':
        return .0, float
    elif val_cast_type == 'listjson':
        return '[]', json.loads
    elif val_cast_type == 'dictjson':
        return '{}', json.loads
    return None, None


def get_query_value(request, key, default=None, val_cast_func=None, val_cast_type=None):
    """ Get Query by POST/GET """
    val_default = default
    if val_cast_type in ['int', 'float', 'listjson', 'dictjson']:
        val_default, val_cast_func = get_default_valcastfunc(val_cast_type)
    value = request.POST.get(key) or request.GET.get(key) or default or val_default
    return val_cast_func(value) if val_cast_func else (value or '')
