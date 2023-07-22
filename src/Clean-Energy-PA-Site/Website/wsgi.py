"""
WSGI config for Website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_parser_path = os.path.abspath(os.path.join(path, "..", "web_parser")) 

if path not in sys.path:     
    sys.path.append(path) 
    
if web_parser_path not in sys.path:
    sys.path.append(web_parser_path) 
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Website.settings")

application = get_wsgi_application()
