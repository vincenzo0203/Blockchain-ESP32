import os
import ssl
from django.core.management import execute_from_command_line
from django.core.management.commands.runserver import Command as runserver
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    # Configura SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="ssl/django.crt", keyfile="ssl/django.key")

    # Crea l'applicazione WSGI di Django
    application = get_wsgi_application()

    # Crea il server WSGI con il contesto SSL
    server = make_server('0.0.0.0', 8000, application)
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)

    print("Django development server running at https://127.0.0.1:8000/")
    server.serve_forever()