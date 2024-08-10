from abc import ABC, abstractmethod

class RouteHandler(ABC):
    """
    Abstract base class for handling RESTful routes.
    Subclasses should override the methods corresponding to HTTP methods they want to handle.
    """

    @abstractmethod
    def get(self, request):
        """
        Handle GET requests. Override this method in subclasses if you want to handle GET requests.
        """
        pass

    def post(self, request):
        """
        Handle POST requests. Override this method in subclasses if you want to handle POST requests.
        """
        pass

    def put(self, request):
        """
        Handle PUT requests. Override this method in subclasses if you want to handle PUT requests.
        """
        pass

    def delete(self, request):
        """
        Handle DELETE requests. Override this method in subclasses if you want to handle DELETE requests.
        """
        pass
