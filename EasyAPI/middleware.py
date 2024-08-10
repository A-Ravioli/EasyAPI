def log_request(request):
    """
    Middleware to log the incoming request.
    """
    print(f"Received {request.method} request for {request.path}")

def add_custom_header(request, response):
    """
    Middleware to add a custom header to the response.
    """
    response.headers.append(('X-Custom-Header', 'This is a custom header'))
    return response
