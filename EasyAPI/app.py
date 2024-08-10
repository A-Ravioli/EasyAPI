# EasyAPI/app.py

from EasyAPI.request import Request
from EasyAPI.response import Response

class EasyAPI:
    def __init__(self):
        """
        Initialize the EasyAPI application with an empty route dictionary.
        The dictionary maps (path, method) tuples to handler functions.
        """
        self.routes = {}

    def infer_methods(self, func_name):
        """
        Infer the HTTP methods based on the function name.

        Args:
            func_name (str): The name of the function.

        Returns:
            list: A list of HTTP methods.
        """
        if func_name.startswith('get_'):
            return ['GET']
        elif func_name.startswith('post_'):
            return ['POST']
        elif func_name.startswith('put_'):
            return ['PUT']
        elif func_name.startswith('delete_'):
            return ['DELETE']
        else:
            return ['GET']

    def add_route(self, path, handler):
        """
        Add a route to the application.

        Args:
            path (str): The URL path.
            handler (function): The function that handles requests to this path.
        """
        methods = self.infer_methods(handler.__name__)
        for method in methods:
            self.routes[(path, method)] = handler

    def wsgi_app(self, environ, start_response):
        """
        The WSGI application callable.

        Args:
            environ (dict): The WSGI environment dictionary.
            start_response (function): The function to start the HTTP response.

        Returns:
            list: The response body as a list of bytes.
        """
        request = Request(environ)
        handler = self.routes.get((request.path, request.method), None)

        if handler is not None:
            response = handler(request)
        else:
            response = Response("404 Not Found", status='404 NOT FOUND')

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """
        Make the EasyAPI instance callable as a WSGI application.

        Args:
            environ (dict): The WSGI environment dictionary.
            start_response (function): The function to start the HTTP response.

        Returns:
            list: The response body as a list of bytes.
        """
        return self.wsgi_app(environ, start_response)

    def run(self, host='127.0.0.1', port=5000):
        """
        Run the application using the built-in WSGI server.

        Args:
            host (str): The hostname to listen on.
            port (int): The port to listen on.
        """
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self)
        print(f"Serving on http://{host}:{port}")
        server.serve_forever()

    def route(self, path):
        """
        A decorator to add a route to the application.

        Args:
            path (str): The URL path.

        Returns:
            function: The decorator that adds the route.
        """
        def wrapper(handler):
            self.add_route(path, handler)
            return handler
        return wrapper
