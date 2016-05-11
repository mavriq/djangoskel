# -*- coding: utf-8 -*-

def fix_settings(env):
    assert isinstance(env, dict)
    env.update(
        # DEBUG = False,
        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.postgresql',
        #         'NAME': 'databasename',
        #         'USER': 'username',
        #         'PASSWORD': 'secret',
        #         'HOST': '127.0.0.1',
        #         'PORT': '5432',
        #     }
        # },
    )

