from EasyAPI.response import Response, redirect

# OAuth Routes


def get_login(request, oauth_service):
    """
    Initiate the OAuth login process.
    """
    authorization_url, state = oauth_service.get_authorization_url()
    return redirect(authorization_url)


def get_callback(request, oauth_service):
    """
    Handle the OAuth callback after user authentication.
    """
    token = oauth_service.fetch_token(request.url)
    return Response(f"Access token: {token}")


def post_refresh_token(request, oauth_service):
    """
    Refresh the OAuth token.
    """
    refresh_token = request.form_data.get("refresh_token")
    new_token = oauth_service.refresh_token(refresh_token)
    return Response(f"New access token: {new_token['access_token']}")


# Payment Routes


def post_create_payment(request, payment_service):
    """
    Create a payment intent using Stripe.
    """
    amount = 1000  # Amount in cents
    payment_intent = payment_service.create_payment_intent(amount=amount)
    return Response(f"PaymentIntent created with ID: {payment_intent['id']}")


def post_create_subscription(request, payment_service):
    """
    Create a subscription using Stripe.
    """
    customer_id = "cus_example123"
    price_id = "price_example123"
    subscription = payment_service.create_subscription(customer_id, price_id)
    return Response(f"Subscription created with ID: {subscription['id']}")


def post_create_customer(request, payment_service):
    """
    Create a new customer in Stripe.
    """
    email = request.form_data.get("email")
    customer = payment_service.create_customer(email=email)
    return Response(f"Customer created with ID: {customer['id']}")


def post_handle_webhook(request, payment_service):
    """
    Handle Stripe webhooks for events like payment success or failure.
    """
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = "your-webhook-secret"
    event = payment_service.handle_webhook(payload, sig_header, endpoint_secret)

    if event:
        if event["type"] == "payment_intent.succeeded":
            print("PaymentIntent was successful!")
        elif event["type"] == "payment_intent.payment_failed":
            print("PaymentIntent failed!")
        return Response("Webhook handled successfully")
    else:
        return Response("Webhook handling failed", status="400 BAD REQUEST")


# Cache Routes


def get_cached_data(request, cache_service):
    """
    Retrieve data from cache or generate and store it.
    """
    data = cache_service.get("my_data")
    if not data:
        data = "This is some cached data"
        cache_service.set("my_data", data, expiration=600)  # Cache for 10 minutes
    return Response(data)


def post_clear_cache(request, cache_service):
    """
    Clear the cache.
    """
    cache_service.flush()
    return Response("Cache cleared")


# Task Queue Routes


def post_start_task(request, task_queue_service):
    """
    Start a long-running task using the task queue.
    """
    task_id = task_queue_service.add_task("routes.long_running_task", "my_data")
    return Response(f"Task started with ID: {task_id}")


def get_task_result(request, task_queue_service):
    """
    Get the result of a task from the task queue.
    """
    task_id = request.query_params.get("task_id", [""])[0]
    result, status = task_queue_service.get_result(task_id)
    return Response(f"Task {task_id} - Status: {status}, Result: {result}")


# Static and Utility Routes


def get_home(request):
    """
    Serve the homepage.
    """
    return Response("Welcome to the EasyAPI-powered web application!")


def get_static_file(request, app):
    """
    Serve static files from the designated static folder.
    """
    file_path = request.path.lstrip("/")
    static_response = app.serve_static(request, file_path)
    return static_response
