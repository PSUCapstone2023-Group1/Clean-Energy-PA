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
web_parser_path = os.path.abspath(os.path.join(path, "../../", "web_parser")) 

print("VLAD DEBUGGING!!!")
print("Vlad Debuggin", path)
print("Vlad Debuggin website_path", web_parser_path)

if path not in sys.path:     
    print("Vlad Debuggin inside condition", sys.path)
    sys.path.append(path) 
    sys.path.append(web_parser_path) 
    sys.path.append("..")
    sys.path.append("../web_parser")
    sys.path.append("../web_parser/tests")
    print("Vlad Testing post webparser append", sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Website.settings")

application = get_wsgi_application()
