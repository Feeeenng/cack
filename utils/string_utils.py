# -*- coding: utf8 -*-
from __future__ import unicode_literals


def camel_to_underscore_line(name):
    s = ''
    for i, c in enumerate(name):
        if c.isupper():
            s += '_{0}'.format(c.lower())
        else:
            s += c

    if s.startswith('_'):
        s = s[1:]
    return s


def get_upper_letters(s):
    m = ''
    for c in s:
        if c.isupper():
            m += c

    return m