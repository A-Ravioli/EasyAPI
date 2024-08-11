# EasyAPI/services/payment.py

import stripe
from EasyAPI.utils.logs import logger


class StripePaymentService:
    def __init__(self, api_key):
        stripe.api_key = api_key

    def create_payment_intent(self, amount, currency="usd", customer_id=None):
        """
        Create a payment intent for a one-time payment.
        """
        logger.info(
            f"Creating payment intent for {amount} {currency} with customer {customer_id}"
        )
        return stripe.PaymentIntent.create(
            amount=amount, currency=currency, customer=customer_id
        )

    def create_subscription(self, customer_id, price_id):
        """
        Create a subscription for a customer.
        """
        logger.info(
            f"Creating subscription for customer {customer_id} with price {price_id}"
        )
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
        )

    def handle_webhook(self, payload, sig_header, endpoint_secret):
        """
        Handle Stripe webhooks for events like payment success or failure.
        """
        try:
            logger.info("Handling Stripe webhook")
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            return event
        except ValueError as e:
            # Invalid payload
            logger.error(f"Invalid payload: {e}")
            return None
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            logger.error(f"Invalid signature: {e}")
            return None

    def create_customer(self, email, payment_method=None):
        """
        Create a new customer in Stripe.
        """
        logger.info(f"Creating customer with email {email}")
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method,
            invoice_settings=(
                {"default_payment_method": payment_method} if payment_method else None
            ),
        )
        return customer
