#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


from services.firebase_cloud_client import FirebaseClient


# def initialize_firebase_client():
#     global firebase_client
#     firebase_client = None
#     firebase_client_obj = FirebaseClient()
#     if not firebase_client:
#         firebase_client = firebase_client_obj.get_firebase_client
#     return firebase_client
#
#
# firebase_client = initialize_firebase_client()


if __name__ == "__main__":
    main()
    # initialize_firebase_client()
