"""
ASGI config for EdNova LMS project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ednova.settings')
application = get_asgi_application()
