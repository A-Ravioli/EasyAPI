from EasyAPI import routes
from EasyAPI.app import EasyAPI
from EasyAPI.response import Response
from EasyAPI.middleware import log_request, add_custom_header
from EasyAPI.error_handlers import handle_404, handle_500
from EasyAPI.services.oauth import OAuthService
from EasyAPI.services.payment import StripePaymentService
from EasyAPI.services.cache import CacheService
from EasyAPI.services.task_queue import TaskQueueService

# Basic Usage

app = EasyAPI()


def home(request):
    return Response("Welcome to EasyAPI! This is the home page.")


def about(request):
    return Response("This is the About page.")


def greet(request):
    name = request.body or "Guest"
    return Response(f"Hello, {name}!")


routes = [
    ("/", home, ["GET"]),
    ("/about", about, ["GET"]),
    ("/greet", greet, ["POST"]),
]


app.add_routes(routes)

app.use_middleware(log_request)
app.use_middleware(add_custom_header)

app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)

app.set_static_folder("static")


# Advanced Usage

# Initialize services
oauth_service = OAuthService(
    provider="google",
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:5000/callback",
)

payment_service = StripePaymentService(api_key="your-stripe-api-key")

cache_service = CacheService(provider="redis", host="localhost", port=6379, db=0)

task_queue_service = TaskQueueService(
    broker_url="redis://localhost:6379/0", backend_url="redis://localhost:6379/1"
)

app = EasyAPI()

# Register routes with their respective services
app.add_route("/", lambda req: routes.get_home(req))

# OAuth routes
app.add_route(
    "/login", lambda req: routes.get_login(req, oauth_service), methods=["GET"]
)
app.add_route(
    "/callback", lambda req: routes.get_callback(req, oauth_service), methods=["GET"]
)
app.add_route(
    "/refresh_token",
    lambda req: routes.post_refresh_token(req, oauth_service),
    methods=["POST"],
)

# Payment routes
app.add_route(
    "/create_payment",
    lambda req: routes.post_create_payment(req, payment_service),
    methods=["POST"],
)
app.add_route(
    "/create_subscription",
    lambda req: routes.post_create_subscription(req, payment_service),
    methods=["POST"],
)
app.add_route(
    "/create_customer",
    lambda req: routes.post_create_customer(req, payment_service),
    methods=["POST"],
)
app.add_route(
    "/webhook",
    lambda req: routes.post_handle_webhook(req, payment_service),
    methods=["POST"],
)

# Cache routes
app.add_route(
    "/cached_data",
    lambda req: routes.get_cached_data(req, cache_service),
    methods=["GET"],
)
app.add_route(
    "/clear_cache",
    lambda req: routes.post_clear_cache(req, cache_service),
    methods=["POST"],
)

# Task queue routes
app.add_route(
    "/start_task",
    lambda req: routes.post_start_task(req, task_queue_service),
    methods=["POST"],
)
app.add_route(
    "/task_result",
    lambda req: routes.get_task_result(req, task_queue_service),
    methods=["GET"],
)

# Static files
app.add_route("/static/<path:path>", lambda req: routes.get_static_file(req, app))

if __name__ == "__main__":
    app.run()
