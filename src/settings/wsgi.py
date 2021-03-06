# -*- coding: utf-8 -*-

"""
WSGI config for settings project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

from __future__ import unicode_literals
import sys
if sys.version_info[0] == 2:
    reload(sys).setdefaultencoding("utf-8")


import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
