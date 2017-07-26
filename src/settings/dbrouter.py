# -*- coding: utf-8 -*-

from __future__ import absolute_import
import django
from django.conf import settings
from django.utils.six import string_types
from .utils import debug_method


class DbByAppRouter(object):
    DEFAULT = 'default'

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

    def __get_database_of_names(self, app_label, model_name):
        return self.app_databases.get(
            '{0}.{1}'.format(app_label, model_name),
            self.app_databases.get(app_label, self.DEFAULT))

    def _get_database_of(self, model):
        app_label = model._meta.app_label
        model_name = model.__name__
        return self.__get_database_of_names(app_label, model_name)

    @debug_method
    def db_for_read(self, model, **hints):
        return self._get_database_of(model)

    @debug_method
    def db_for_write(self, model, **hints):
        return self._get_database_of(model)

    @debug_method
    def allow_relation(self, obj1, obj2, **hints):
        return (self._get_database_of(obj1.__class__) ==
                self._get_database_of(obj2.__class__)) and None

    if django.VERSION > (1, 8):
        @debug_method
        def allow_migrate(self, db, app_label, model_name=None, **hints):
            model = hints.get('model', None)
            if model:
                return (db == self._get_database_of(model)) and None
            return (db == self.__get_database_of_names(
                app_label, model_name)) and None
    else:
        @debug_method
        def allow_migrate(self, db, model):
            return (db == self._get_database_of(model)) and None


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
