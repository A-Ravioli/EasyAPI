# EasyAPI

**EasyAPI** is a minimalist Python web framework built from scratch, designed to make web development even easier. This project is a reinvention of the web wheel, focusing on simplicity and ease of use, providing developers with a lightweight and flexible framework to build web applications.

## Features

- **Simple Routing System**: Map URLs to Python functions with minimal effort.
- **WSGI Compliant**: Serve your web applications using any WSGI-compatible server.
- **Request and Response Handling**: Easily handle HTTP requests and generate responses.
- **Templating Support**: Render HTML templates with simple context substitution.
- **Lightweight and Easy to Use**: Designed to keep things simple, making it easy to get started and build your own web applications.

## Getting Started

### Prerequisites

Make sure you have Python installed. You can check your Python version with:

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

**Define Your Application**: Create a `run.py` file.

```python
from EasyAPI.app import EasyAPI

app = EasyAPI()

@app.route('/')
def home():
    return app.render_template('base.html', title="Hello, World!", content="Welcome to EasyAPI!")

if __name__ == '__main__':
    app.run()
```

**Run Your Application**:

```bash
python run.py
```

**Visit Your Application**: Open your browser and go to `http://127.0.0.1:5000/`.

### Directory Structure

Here's a quick overview of the project structure:

```bash
easyapi/
│
├── EasyAPI/
│   ├── __init__.py
│   ├── app.py
│   ├── routing.py
│   ├── request.py
│   ├── response.py
│   └── templates/
│       └── base.html
│
├── tests/
│   └── test_app.py
│
└── run.py
```

- **EasyAPI/**: Contains the core framework components.
- **templates/**: Holds your HTML templates.
- **tests/**: Contains unit tests for your application.
- **run.py**: The entry point for running your application.

### Adding Routes

You can easily add new routes to your application:

```python
@app.route('/about')
def about():
    return "This is the About page."
```

### Customizing Responses

You can customize the HTTP response by directly returning `Response` objects:

```python
from EasyAPI.response import Response

@app.route('/custom')
def custom():
    return Response("Custom Response", status='200 OK', headers=[('Content-Type', 'text/plain')])
```

## Contributing

Contributions are welcome! If you have ideas, features, or bug fixes, feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to the branch.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
