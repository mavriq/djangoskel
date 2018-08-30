# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
from django.utils.six import string_types, integer_types
import logging
import time


def debug_method(fn=None, debug_level=None):
    '''
    usage:
    class C:
        @debug_method
        def f(self):
            pass
        @debug_method(debug_level=pprint)
        def x(self):
            pass
        @debug_method(debug_level='INFO')
        def x(self):
            pass
        @staticmethod
        @debug_method('C')
        def y(self):
            pass
    '''

    def _repr(obj):
        try:
            return repr(obj)
        except Exception as e:
            # полезно при попытке декорировать __init__ или __repr__
            _cls = obj.__class__.__name__
            _avg_obj = '{0}(...)'.format(_cls)
            logging.error('attempt to get repr({0})'.format(_avg_obj))
            return _avg_obj

    var = {}
    var['log'] = None
    if isinstance(fn, string_types):
        var['cls'] = fn
        fn = None
    else:
        var['cls'] = None
    if debug_level is None:
        var['log'] = 'debug'
    elif isinstance(debug_level, string_types):
        _l_level = debug_level.lower()
        if _l_level in ('debug', 'info', 'warn', 'warning', 'error',
                        'exception', 'critical', 'fatal'):
            var['log'] = _l_level
        else:
            raise AttributeError('incorrect attribute debug_level={0}'.format(
                repr(debug_level)))
    elif isinstance(debug_level, integer_types):
        if debug_level >= logging.CRITICAL:
            var['log'] = 'critical'
        elif debug_level >= logging.ERROR:
            var['log'] = 'error'
        elif debug_level >= logging.WARNING:
            var['log'] = 'warn'
        elif debug_level >= logging.INFO:
            var['log'] = 'info'
        else:
            var['log'] = 'debug'
    elif hasattr(debug_level, '__call__'):
        var['log'] = debug_level
    else:
        raise AttributeError('incorrect attribute debug_level={0}'.format(
            _repr(debug_level)))

    def next_step_decorator(fn):
        _log = var['log']
        if var['cls']:
            _func_name = '{0}.{1}'.format(var['cls'], fn.__name__)
        else:
            _func_name = fn.__name__
        if isinstance(_log, string_types):
            _mod = fn.__module__
            _logger = logging.getLogger(_mod)
            _log = getattr(_logger, _log)

        def wrapper(*args, **kwargs):
            _kw_items = tuple(kwargs.items())
            _hash = int(time.time() * 1e+6)
            _start_msg = '<{0:x}>: {1}({2})...'.format(
                _hash, _func_name, ', '.join(
                    [_repr(_a) for _a in args] + [
                        '{0}={1}'.format(k, _repr(v))
                        for k, v in _kw_items]))
            _log(_start_msg)
            try:
                _result = fn(*args, **kwargs)
            except Exception:
                e = sys.exc_info()
                _exception_msg = '<{0:x}>: exception {1}'.format(_hash, e)
                _log(_exception_msg)
                raise e
            else:
                _ret_msg = '<{0:x}>: ... {1}'.format(_hash, _repr(_result))
                _log(_ret_msg)
                return _result
        #
        return wrapper
    #
    if fn is None:
        return next_step_decorator
    else:
        return next_step_decorator(fn)
