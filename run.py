from EasyAPI.app import EasyAPI
from EasyAPI.response import Response

app = EasyAPI()

def get_home(request):
    return Response("Welcome to EasyAPI! This is the home page.")

def get_about(request):
    return Response("This is the About page.")

def post_greet(request):
    name = request.body or 'Guest'
    return Response(f"Hello, {name}!")

# Define routes and let EasyAPI infer methods automatically
app.routes = {
    '/': get_home,
    '/about': get_about,
    '/greet': post_greet,
}

if __name__ == '__main__':
    app.run()
