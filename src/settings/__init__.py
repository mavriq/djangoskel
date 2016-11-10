# -*- coding: utf-8 -*-
"""
Универсальный Django settings.
"""

import os
import sys
from .settings import *

try:
    from .localsettings import fix_settings
except ImportError:
    try:
        from .localsettings import *
    except ImportError:
        raise ImportError("WARNING: Can't load `{0}`".format(
            os.path.join(os.path.basename(os.path.abspath(__file__)), 'localsettings.py')))
else:
    fix_settings(locals())
    del(fix_settings)

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
            Exception('Please, create a {0} file with random characters to generate your secret key'.format(_SECRET_FILE_NAME))
