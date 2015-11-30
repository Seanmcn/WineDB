#!/usr/bin/env python
import os
import sys

# [Start Patch] for Python mySQL on Windows causing me pain
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
# [End Patch]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jlw.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

