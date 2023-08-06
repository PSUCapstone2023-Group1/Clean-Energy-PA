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
src =  os.path.dirname(path)
response =  os.path.abspath(os.path.join(web_parser_path, "responses")) 
if path not in sys.path:     
    sys.path.append(path) 

if web_parser_path not in sys.path:
    sys.path.append(web_parser_path) 
    
if src not in sys.path:     
    sys.path.append(src) 

if response not in sys.path:     
    sys.path.append(response)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Website.settings")

application = get_wsgi_application()
