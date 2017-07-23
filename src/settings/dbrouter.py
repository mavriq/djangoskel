# -*- coding: utf-8 -*-

import django
from django.conf import settings
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
    if isinstance(fn, string_types):
        _cls = fn
        fn = None
    else:
        _cls = None
    if debug_level is None:
        _log = logging.debug
    elif isinstance(debug_level, string_types):
        _l_level = debug_level.lower()
        if _l_level in ('debug', 'info', 'warn', 'warning', 'error',
                        'exception', 'critical', 'fatal'):
            _log = getattr(logging, _l_level)
        else:
            raise AttributeError('incorrect attribute debug_level={0}'.format(
                repr(debug_level)))
    elif isinstance(debug_level, integer_types):
        if debug_level >= logging.CRITICAL:
            _log = logging.critical
        elif debug_level >= logging.ERROR:
            _log = logging.error
        elif debug_level >= logging.WARNING:
            _log = logging.warn
        elif debug_level >= logging.INFO:
            _log = logging.info
        else:
            _log = logging.debug
    elif hasattr(debug_level, '__call__'):
        _log = debug_level
    else:
        raise AttributeError('incorrect attribute debug_level={0}'.format(
            repr(debug_level)))

    def next_step_decorator(fn):
        if _cls:
            func_name = '{0}.{1}'.format(_cls, fn.__name__)
        else:
            func_name = fn.__name__

        def wrapper(*args, **kwargs):
            _kw_items = tuple(kwargs.items())
            _hash = int(time.time() * 1e+6)
            _start_msg = '<{0:x}>: {1}({2})...'.format(
                _hash, func_name, ', '.join(
                    [repr(_a) for _a in args] + [
                        '{0}={1}'.format(k, repr(v))
                        for k, v in _kw_items]))
            _log(_start_msg)
            try:
                _result = fn(*args, **kwargs)
            except Exception as e:
                _exception_msg = '<{0:x}>: exception {1}'.format(_hash, e)
                _log(_exception_msg)
                raise e
            else:
                _ret_msg = '<{0:x}>: ... {1}'.format(_hash, repr(_result))
                _log(_ret_msg)
                return _result
        #
        return wrapper
    #
    if fn is None:
        return next_step_decorator
    else:
        return next_step_decorator(fn)


class DbByAppRouter(object):
    def __init__(self):
        self.app_databases = {}
        for db, opts in settings.DATABASES.items():
            apps = opts.get('applications')
            if not apps:
                continue
            elif isinstance(apps, string_types):
                self.app_databases[apps] = db
            elif hasattr(apps, '__iter__'):
                for app in apps:
                    self.app_databases[app] = db
        logging.debug('app_databases = {0}'.format(self.app_databases))

    @debug_method
    def db_for_read(self, model, **hints):
        return self.app_databases.get(model._meta.app_label, 'default')

    @debug_method
    def db_for_write(self, model, **hints):
        return self.app_databases.get(model._meta.app_label, 'default')

    @debug_method
    def allow_relation(self, obj1, obj2, **hints):
        return self.app_databases.get(
            obj1.__class__.__name__) == self.app_databases.get(
                obj2.__class__.__name__) and None

    if django.VERSION > (1, 8):
        @debug_method
        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == self.app_databases.get(app_label, 'default') and None
    else:
        @debug_method
        def allow_migrate(self, db, model):
            return (db == self.app_databases.get(
                    model._meta.app_label, 'default') and None)


class RestrictMigrations(object):
    def db_for_read(self, model, **hints):
        pass

    def db_for_write(self, model, **hints):
        pass

    def allow_relation(self, obj1, obj2, **hints):
        pass

    if django.VERSION > (1, 8):
        @debug_method
        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return settings.DATABASES[db].get('allow_migrate', True) and None
    else:
        @debug_method
        def allow_migrate(self, db, model):
            return settings.DATABASES[db].get('allow_migrate', True) and None
