from urllib.parse import parse_qs


class Request:
    def __init__(self, environ):
        """
        Initialize the Request object with WSGI environment data.

        Args:
            environ (dict): The WSGI environment dictionary.
        """
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"]
        self.query_string = environ["QUERY_STRING"]
        self.query_params = parse_qs(self.query_string)
        self.headers = self._get_headers()
        self.body = self._get_body()

    def _get_headers(self):
        """
        Extract headers from the WSGI environment.

        Returns:
            dict: A dictionary of HTTP headers.
        """
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-").lower()] = value
        return headers

    def _get_body(self):
        """
        Extract the body from the WSGI environment.

        Returns:
            str: The body of the request as a string.
        """
        try:
            length = int(self.environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            length = 0
        if length > 0:
            return self.environ["wsgi.input"].read(length).decode("utf-8")
        return ""
