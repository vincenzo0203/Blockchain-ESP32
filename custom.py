import os
from django.core.management import execute_from_command_line
import ssl

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

    from django.core.management.commands.runserver import Command as runserver
    runserver.default_addr = "0.0.0.0"
    runserver.default_port = "8000"

    # Configura SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="ssl/django.crt", keyfile="ssl/django.key")
    
    # Avvia il server con SSL
    from wsgiref.simple_server import make_server
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
    server = make_server('0.0.0.0', 8000, application)
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    print("Django development server running at https://0.0.0.0:8000")
    server.serve_forever()