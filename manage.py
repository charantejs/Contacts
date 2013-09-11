#!/usr/bin/env python
import os
import sys
#import pdb;pdb.set_trace()
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Contacts.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
