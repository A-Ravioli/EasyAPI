from EasyAPI.app import EasyAPI
from EasyAPI.response import Response
from EasyAPI.middleware import log_request, add_custom_header
from EasyAPI.error_handlers import handle_404, handle_500

app = EasyAPI()

def home(request):
    return Response("Welcome to EasyAPI! This is the home page.")

def about(request):
    return Response("This is the About page.")

def greet(request):
    name = request.body or 'Guest'
    return Response(f"Hello, {name}!")

routes = [
    ('/', home, ['GET']),
    ('/about', about, ['GET']),
    ('/greet', greet, ['POST']),
]

app.add_routes(routes)

app.use_middleware(log_request)
app.use_middleware(add_custom_header)

app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)

app.set_static_folder('static')

if __name__ == '__main__':
    app.run()