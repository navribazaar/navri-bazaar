"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()


# At the bottom of wsgi.py
from django.contrib.auth import get_user_model

try:
    User = get_user_model()
    # Change 'mitesh_admin' to whatever username you prefer
    if not User.objects.filter(username='mitesh_admin').exists():
        User.objects.create_superuser('Navro_manas', 'navribazaar.in@gmail.com', 'Navro&Navri')
        print("Live superuser created successfully!")
except Exception as e:
    print(f"Superuser check skipped: {e}")