# EasyAPI

**EasyAPI** is a minimalist Python web framework designed for simplicity and ease of use. It allows you to define routes, handle HTTP requests, and manage middleware with a clean, visually appealing structure. Completely open-source, and contributions are welcome.

## Features

- **Visually Appealing Route Registration**: Define routes in a clear and structured manner without using decorators.
- **Middleware Support**: Easily integrate middleware for pre- and post-processing of requests and responses.
- **Blueprints**: Modularize your application into separate components, making it easy to manage larger projects.
- **Customizeable Error Handling**: Customize error pages and manage HTTP status codes effectively.
- **Logging**: Track application activity with built-in logging support.
- **Static Files**: Serve static assets like CSS, JavaScript, and images directly from your application.

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can check your Python version with:

```bash
python --version
```

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/easyapi.git
cd easyapi
```

### Basic Usage

To create a basic web application using EasyAPI, follow these steps:

#### **Define Your Route Handlers**: Create your route handler functions

```python
def home(request):
    return Response("Welcome to EasyAPI! This is the home page.")

def about(request):
    return Response("This is the About page.")

def greet(request):
    name = request.body or 'Guest'
    return Response(f"Hello, {name}!")
```

#### **Register Routes**: Define your routes in a dictionary, without using decorators

```python
routes = [
    ('/', home, ['GET']),
    ('/about', about, ['GET']),
    ('/greet', greet, ['POST']),
]
app.add_routes(routes)
```

#### **Add Middleware and Error Handlers**: Optionally, add middleware and error handlers

```python
app.use_middleware(log_request)
app.use_middleware(add_custom_header)

app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)
```

#### **Serve Static Files**: Set a directory for serving static files

```python
app.set_static_folder('static')
```

#### **Run Your Application**: Start the server and your application will be live

```python
if __name__ == '__main__':
    app.run()
```

### Example

See a complete example usage including advanced features in the [example.py](example.py) or see an example of the base features here:

```python
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
```

### Advanced Features

#### Middleware

Middleware functions allow you to add custom logic before and after request handling. Here’s an example:

```python
def log_request(request):
    print(f"Received {request.method} request for {request.path}")

def add_custom_header(request, response):
    response.headers.append(('X-Custom-Header', 'This is a custom header'))
    return response
```

#### Blueprints

Blueprints help you organize your application by grouping related routes together. Here’s an example of using a blueprint:

```python
from EasyAPI.blueprint import Blueprint

api = Blueprint()

@api.route('/greet', methods=['POST'])
def greet(request):
    name = request.body or 'Guest'
    return Response(f"Hello, {name}!")

app.register_blueprint(api, url_prefix='/api')
```

#### Error Handling

You can define custom error handlers to provide more user-friendly error pages:

```python
def handle_404(request):
    return Response("Custom 404 Not Found", status='404 NOT FOUND')

def handle_500(request):
    return Response("Custom 500 Internal Server Error", status='500 INTERNAL SERVER ERROR')
```

#### EasyAPI CLI Features Overview

**Create a New Project**

```bash
easyapi new my_project
```

This command generates a new EasyAPI project with a basic directory structure, including folders for routes, middlewares, and static files.

**Run the Server:**

```bash
easyapi run
```

This command starts the EasyAPI development server. It automatically imports the run.py file to start the application.

**List All Routes:**

```bash
easyapi routes
```

This command lists all registered routes along with their corresponding handler functions and HTTP methods.

**Generate a New Route:**

```bash
easyapi generate-route my_route
```

This command scaffolds a new route handler in the routes directory. For example, it will create a my_route.py file in the routes directory with a pre-defined handler function.

**Add a Middleware:**

```bash
easyapi add-middleware my_middleware
```

This command scaffolds a new middleware function in the middlewares directory. It creates a file with a basic middleware template.

**Set Static Folder:**

```bash
easyapi set-static static
```

This command sets the static files directory for the application.

### Contributing

Contributions are welcome! If you have ideas, features, or bug fixes, feel free to submit a pull request or open an issue.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
