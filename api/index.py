#!/usr/bin/env python3
"""
Vercel Serverless Function for Django
"""
import os
import sys

# Ajouter le répertoire backend au path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Importer et configurer Django
import django
django.setup()

# Importer l'application WSGI
from config.wsgi import application

# Handler pour Vercel
def handler(event, context):
    """
    Vercel serverless function handler
    """
    from django.core.handlers.wsgi import WSGIHandler
    from io import BytesIO
    
    # Créer un environ WSGI
    environ = {
        'REQUEST_METHOD': event.get('method', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('query', ''),
        'SERVER_NAME': 'vercel.app',
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', b'').encode() if event.get('body') else BytesIO()),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Ajouter les headers
    for key, value in event.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # Response
    response = {'statusCode': 200, 'headers': {}, 'body': ''}
    
    def start_response(status, headers):
        response['statusCode'] = int(status.split()[0])
        response['headers'] = dict(headers)
    
    body = application(environ, start_response)
    response['body'] = ''.join([chunk.decode() if isinstance(chunk, bytes) else chunk for chunk in body])
    
    return response
