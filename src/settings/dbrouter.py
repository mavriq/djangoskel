# -*- coding: utf-8 -*-

from __future__ import absolute_import
import django
from django.conf import settings
from django.utils.six import string_types
from .utils import debug_method


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
