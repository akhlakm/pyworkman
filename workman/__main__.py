import os
import django
from django.core import management

def main():
    print("Hello")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workman.backend.settings')
    django.setup()
    management.call_command('runserver')
