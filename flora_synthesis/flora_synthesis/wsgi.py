"""
WSGI config for flora_synthesis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flora_synthesis.settings')

os.system("python manage.py migrate")

application = get_wsgi_application()
app = application
