import os
import ssl
from django.core.management import execute_from_command_line
from django.core.management.commands.runserver import Command as runserver
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server
#from django.views.static import serve
#from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    # Configura SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="ssl/django.crt", keyfile="ssl/django.key")

    # Crea l'applicazione WSGI di Django
    application = get_wsgi_application()
    
    # Aggiungi la gestione dei file statici se siamo in modalità di sviluppo
    #def static_file_server(environ, start_response):
    #    if environ['PATH_INFO'].startswith(settings.STATIC_URL):
    #        return serve(environ, start_response, document_root=settings.STATIC_ROOT)
    #    return application(environ, start_response)

    # Crea il server WSGI con il contesto SSL
    server = make_server('0.0.0.0', 8000, application)
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)

    print("Django development server running at https://127.0.0.1:8000/")
    server.serve_forever()