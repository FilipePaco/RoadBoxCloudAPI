#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roadbox_cloudapi.settings')
    try:
        from django.conf import settings  # Importa as configurações
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as runserver
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Define a porta padrão a partir do settings
    runserver.default_port = getattr(settings, 'DEFAULT_PORT', '8000')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
