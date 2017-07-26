# -*- coding: utf-8 -*-
"""
Универсальный Django settings.
"""

from __future__ import unicode_literals
import sys
if sys.version_info[0] == 2:
    reload(sys).setdefaultencoding("utf-8")

import os
from .settings import *
from pprint import pformat


try:
    from .localsettings import fix_settings
except ImportError:
    try:
        from .localsettings import *
    except ImportError:
        _locsettings = '''# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def fix_settings(env):
    assert isinstance(env, dict)
    env.update(
        DEBUG=True,
        # LANGUAGE_CODE=%(LANGUAGE_CODE)s,
        # TIME_ZONE=%(TIME_ZONE)s,
        # MEDIA_ROOT=%(MEDIA_ROOT)s,
        # STATICFILES_DIRS=%(STATICFILES_DIRS)s,
        DATABASES=%(DATABASES)s,

        # # https://docs.djangoproject.com/en/1.8/ref/settings/#email
        # ADMINS=[('admin', 'admin@localhost'), ],
        # SERVER_EMAIL='django@localhost'
        # EMAIL_HOST='localhost',
        # EMAIL_PORT=587,
        # EMAIL_HOST_USER='webmaster',
        # EMAIL_HOST_PASSWORD='secure',
        # EMAIL_USE_TLS=True,
        # EMAIL_SUBJECT_PREFIX='[Django] '
        # DEFAULT_FROM_EMAIL='webmaster@localhost',

        ## Only for development
        # AUTH_PASSWORD_VALIDATORS=[]
        # ...
    )
    if env['DEBUG']:
        ## only if django-debug-toolbar installed
        # env['INSTALLED_APPS'].append('debug_toolbar')
        # env['INTERNAL_IPS'] = ['127.0.0.1', ]
        pass
''' % dict(
            LANGUAGE_CODE=repr(LANGUAGE_CODE),
            TIME_ZONE=repr(TIME_ZONE),
            MEDIA_ROOT=repr(MEDIA_ROOT),
            STATICFILES_DIRS=pformat(STATICFILES_DIRS),
            DATABASES=pformat(DATABASES),
        )
        _locsettings_filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'localsettings.py')
        try:
            _locsettings_file = open(_locsettings_filename, 'w')
            _locsettings_file.write(_locsettings)
        except Exception as e:
            # TODO: добавить нормальное сообщение о невозможности создать localsettings.py
            raise e
        else:
            _locsettings_file.flush()
            _locsettings_file.close()
            del(_locsettings, _locsettings_file, _locsettings_filename)
        try:
            from .localsettings import fix_settings
        except ImportError:
            try:
                from .localsettings import *
            except ImportError:
                raise ImportError("WARNING: Can't load or create {0}".format(
                    os.path.join(
                        os.path.basename(os.path.abspath(__file__)),
                        'localsettings.py')))
else:
    fix_settings(locals())
    del(fix_settings)

if 'debug_toolbar' in INSTALLED_APPS and \
        'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

if locals().get('SECRET_KEY') is None:
    if 2 == sys.version_info.major:
        FileNotFoundError = IOError
    _SECRET_FILE_NAME = os.path.join(BASE_DIR, 'private', 'secret.txt')
    try:
        SECRET_KEY = open(_SECRET_FILE_NAME).read().strip()
    except FileNotFoundError:
        try:
            from django.utils.crypto import get_random_string
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            SECRET_KEY = get_random_string(50, chars)
            _SECRET_FILE = open(_SECRET_FILE_NAME, 'w')
            _SECRET_FILE.write(SECRET_KEY)
            _SECRET_FILE.close()
            del(_SECRET_FILE, _SECRET_FILE_NAME, chars)
        except IOError:
            Exception(
                'Please, create a {0} file with random characters '
                'to generate your secret key'.format(_SECRET_FILE_NAME))
