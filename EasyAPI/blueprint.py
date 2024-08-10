class Blueprint:
    def __init__(self):
        """
        Initialize the Blueprint with empty routes and methods.
        """
        self.routes = {}
        self.methods = {}

    def route(self, path, methods=['GET']):
        """
        Define a route within the blueprint.

        Args:
            path (str): The URL path.
            methods (list): The list of HTTP methods this route should respond to.

        Returns:
            function: The decorator that adds the route.
        """
        def wrapper(handler):
            self.routes[path] = handler
            self.methods[path] = methods
            return handler
        return wrapper
