#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pssi.settings")

    # adding the apps directory to path
    ROOT_DIR = os.path.dirname(__file__)
    sys.path.append(os.path.join(ROOT_DIR, 'apps'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
