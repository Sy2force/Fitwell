import os
import sys
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
os.environ['DEBUG'] = 'False'
django.setup()

print(f"DEBUG is: {settings.DEBUG}")
print(f"SECRET_KEY is: {settings.SECRET_KEY}")
