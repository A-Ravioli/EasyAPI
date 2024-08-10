class Response:
    def __init__(self, content, status='200 OK', headers=None):
        """
        Initialize the Response object.

        Args:
            content (str): The response body.
            status (str): The HTTP status code.
            headers (list): A list of tuples representing the headers.
        """
        self.content = content.encode('utf-8')
        self.status = status
        self.headers = headers if headers else [('Content-Type', 'text/html')]

    def __call__(self, environ, start_response):
        """
        The callable that starts the HTTP response.

        Args:
            environ (dict): The WSGI environment dictionary.
            start_response (function): The function to start the HTTP response.

        Returns:
            list: The response body as a list of bytes.
        """
        start_response(self.status, self.headers)
        return [self.content]
