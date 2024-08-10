from EasyAPI.response import Response

def handle_404(request):
    return Response("Custom 404 Not Found", status='404 NOT FOUND')

def handle_500(request):
    return Response("Custom 500 Internal Server Error", status='500 INTERNAL SERVER ERROR')
