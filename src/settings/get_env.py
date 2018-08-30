# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import re


class EnvFilter(object):
    default_prefix = 'DJANGO_'
    default_comment_prefix = r'\s*#'
    default_separators = r',\s'

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_env(self, envname):
        """
        Return value of environment by envname with prefix (if specified)
        For example, command
        >>> get_env('secret', 'ENV_')
        return value of environment ENV_secret

        If prefix is not specified or is None - он считается равым 'DJANGO_'
        If environment does not exist - return None
        """
        _envname = ''.join((self.prefix, envname))
        return os.environ.get(_envname)

    def get_str_env(self, envname):
        return self.get_env(envname) or ''

    def get_masked_string(self, envname):
        '''
        в многострочных переменных удаляет закомментированные строки
        '''
        # _raw = self.get_str_env(envname).split('\n')
        raise NotImplementedError

    def get_bool_env(self, envname):
        v = self.get_str_env(envname)
        if v.lower() in {'1', 'y' 'yes', 'on', 'true', 'enable', 'enabled'}:
            return True
        elif v.lower() in {'0', 'n', 'no', 'false', 'disable', 'disabled'}:
            return False
        else:
            return None
