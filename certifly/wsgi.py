import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'certifly.settings')

application = get_wsgi_application()

# Add this at the end of your wsgi.py file
def handler(event, context):
    return application(event.get('body', ''), context)