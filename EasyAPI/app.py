import os
from EasyAPI.request import Request
from EasyAPI.response import Response
import logging
import inspect

class EasyAPI:
    def __init__(self):
        """
        Initialize the EasyAPI application.
        """
        self.routes = {}
        self.error_handlers = {}
        self.middlewares = []
        self.blueprints = {}
        self.static_folder = None

        # Set up basic logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('EasyAPI')

    def add_route(self, path, handler, methods=['GET']):
        """
        Add a route to the application.

        Args:
            path (str): The URL path.
            handler (function): The function that handles requests to this path.
            methods (list): The list of HTTP methods this route should respond to.
        """
        for method in methods:
            self.routes[(path, method)] = handler
        self.logger.info(f'Route added: {path} [{", ".join(methods)}]')

    def add_routes(self, routes):
        """
        Add multiple routes to the application using a list or dictionary.

        Args:
            routes (list|dict): A list of tuples or dictionary mapping paths to handlers and methods.
        """
        if isinstance(routes, list):
            for path, handler, methods in routes:
                self.add_route(path, handler, methods)
        elif isinstance(routes, dict):
            for path, (handler, methods) in routes.items():
                self.add_route(path, handler, methods)

    def register_error_handler(self, status_code, handler):
        """
        Register a custom error handler.

        Args:
            status_code (int): The HTTP status code.
            handler (function): The function that handles the error.
        """
        self.error_handlers[status_code] = handler
        self.logger.info(f'Error handler registered for status code {status_code}')

    def use_middleware(self, middleware):
        """
        Add middleware to the application.

        Args:
            middleware (function): The middleware function.
        """
        self.middlewares.append(middleware)
        self.logger.info(f'Middleware added: {middleware.__name__}')

    def register_blueprint(self, blueprint, url_prefix=''):
        """
        Register a blueprint to the application.

        Args:
            blueprint (Blueprint): The blueprint instance.
            url_prefix (str): The URL prefix for the blueprint routes.
        """
        for route, handler in blueprint.routes.items():
            self.add_route(url_prefix + route, handler, blueprint.methods.get(route, ['GET']))

    def set_static_folder(self, folder_path):
        """
        Set the folder for serving static files.

        Args:
            folder_path (str): The path to the static files folder.
        """
        if os.path.isdir(folder_path):
            self.static_folder = folder_path
            self.logger.info(f'Serving static files from: {folder_path}')
        else:
            raise FileNotFoundError(f'Static folder {folder_path} does not exist.')

    def serve_static(self, request, path):
        """
        Serve a static file.

        Args:
            request (Request): The request object.
            path (str): The path to the static file relative to the static folder.

        Returns:
            Response: The response containing the static file content.
        """
        file_path = os.path.join(self.static_folder, path)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            mime_type = 'text/plain'  # You can improve this by using the mimetypes module
            return Response(content, headers=[('Content-Type', mime_type)])
        else:
            return self.error_handlers.get(404, lambda req: Response("404 Not Found", status='404 NOT FOUND'))(request)

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

        # Middleware processing (pre-route)
        for middleware in self.middlewares:
            response = middleware(request)
            if response:
                return response(environ, start_response)

        # Handle static files
        if self.static_folder and request.path.startswith('/static/'):
            static_path = request.path[len('/static/'):]
            response = self.serve_static(request, static_path)
            return response(environ, start_response)

        handler = self.routes.get((request.path, request.method), None)

        if handler is not None:
            response = handler(request)
        else:
            response = self.error_handlers.get(404, lambda req: Response("404 Not Found", status='404 NOT FOUND'))(request)

        # Middleware processing (post-route)
        for middleware in self.middlewares:
            post_response = middleware(request, response)
            if post_response:
                response = post_response

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
        self.logger.info(f"Serving on http://{host}:{port}")
        server.serve_forever()
