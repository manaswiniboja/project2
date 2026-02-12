#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')

    # AUTO-RUN MIGRATIONS ON RAILWAY
    if os.environ.get("RUN_MIGRATIONS") == "1":
        import django
        django.setup()
        from django.core.management import call_command
        call_command("migrate", interactive=False)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
