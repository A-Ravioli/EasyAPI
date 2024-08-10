import argparse
import os
import sys

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def create_project(name):
    """
    Create a new EasyAPI project with a basic structure.
    """
    if os.path.exists(name):
        print(f"Project '{name}' already exists.")
        sys.exit(1)

    os.makedirs(name)
    os.makedirs(os.path.join(name, 'routes'))
    os.makedirs(os.path.join(name, 'middlewares'))
    os.makedirs(os.path.join(name, 'static'))

    with open(os.path.join(name, 'example.py'), 'w') as f:
        f.write(f"from EasyAPI.app import EasyAPI\nimport routes\n\napp = EasyAPI()\napp.auto_discover_routes(routes)\n\nif __name__ == '__main__':\n    app.run()\n")

    with open(os.path.join(name, 'routes', '__init__.py'), 'w') as f:
        f.write("# Define your route handlers here\n")

    print(f"New EasyAPI project '{name}' created successfully!")

def run_server():
    """
    Start the EasyAPI development server.
    """
    try:
        from example import app
        app.run()
    except ImportError:
        print("Error: No 'example.py' file found. Make sure you're in the project directory.")
        sys.exit(1)

def list_routes():
    """
    List all registered routes in the application.
    """
    try:
        from example import app
        for route, (handler, methods) in app.routes.items():
            methods_list = ', '.join(methods)
            print(f"{route} -> {handler.__name__} [{methods_list}]")
    except ImportError:
        print("Error: No 'run.py' file found. Make sure you're in the project directory.")
        sys.exit(1)

def generate_route(name):
    """
    Generate a new route handler function.
    """
    routes_dir = os.path.join(os.getcwd(), 'routes')
    if not os.path.exists(routes_dir):
        print("Error: Routes directory not found.")
        sys.exit(1)

    route_file = os.path.join(routes_dir, f"{name}.py")
    if os.path.exists(route_file):
        print(f"Error: Route '{name}' already exists.")
        sys.exit(1)

    with open(route_file, 'w') as f:
        f.write(f"def get_{name}(request):\n")
        f.write(f"    return Response('This is the {name} route')\n")

    print(f"Route '{name}' created successfully!")

def add_middleware(name):
    """
    Scaffold a new middleware function.
    """
    middlewares_dir = os.path.join(os.getcwd(), 'middlewares')
    if not os.path.exists(middlewares_dir):
        print("Error: Middlewares directory not found.")
        sys.exit(1)

    middleware_file = os.path.join(middlewares_dir, f"{name}.py")
    if os.path.exists(middleware_file):
        print(f"Error: Middleware '{name}' already exists.")
        sys.exit(1)

    with open(middleware_file, 'w') as f:
        f.write(f"def {name}(request, response):\n")
        f.write(f"    # Add your middleware logic here\n")
        f.write(f"    return response\n")

    print(f"Middleware '{name}' created successfully!")

def set_static_folder(path):
    """
    Set or update the static files directory.
    """
    try:
        from example import app
        app.set_static_folder(path)
        print(f"Static folder set to: {path}")
    except ImportError:
        print("Error: No 'example.py' file found. Make sure you're in the project directory.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="EasyAPI CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create a new project
    parser_new = subparsers.add_parser('new', help='Create a new EasyAPI project')
    parser_new.add_argument('name', help='The name of the new project')

    # Run the server
    subparsers.add_parser('run', help='Run the EasyAPI development server')

    # List all routes
    subparsers.add_parser('routes', help='List all registered routes')

    # Generate a new route handler
    parser_generate_route = subparsers.add_parser('generate-route', help='Generate a new route handler')
    parser_generate_route.add_argument('name', help='The name of the route')

    # Add a new middleware function
    parser_add_middleware = subparsers.add_parser('add-middleware', help='Add a new middleware function')
    parser_add_middleware.add_argument('name', help='The name of the middleware')

    # Set the static folder
    parser_set_static = subparsers.add_parser('set-static', help='Set the static files directory')
    parser_set_static.add_argument('path', help='The path to the static files directory')

    args = parser.parse_args()

    if args.command == 'new':
        create_project(args.name)
    elif args.command == 'run':
        run_server()
    elif args.command == 'routes':
        list_routes()
    elif args.command == 'generate-route':
        generate_route(args.name)
    elif args.command == 'add-middleware':
        add_middleware(args.name)
    elif args.command == 'set-static':
        set_static_folder(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
