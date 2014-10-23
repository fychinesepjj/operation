#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    project_root_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(project_root_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
