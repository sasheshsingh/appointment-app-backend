# from config.settings import stripe
#
# router = APIRouter()
# @router.post("/webhook")
# async def stripe_webhook(request: Request, response: Response):
#     payload = await request.body()
#     sig_header = request.headers.get("Stripe-Signature")
#
#     try:
#         event = stripe.webhooks.construct_event(
#             payload, sig_header, "your_stripe_webhook_secret"
#         )
#     except ValueError as e:
#         response.status_code = 400
#         return str(e)
#     except stripe.error.SignatureVerificationError as e:
#         response.status_code = 400
#         return str(e)
#
#     # Handle the event
#     if event['type'] == 'checkout.session.completed':
#         # Payment was successful
#         session = event['data']['object']
#         # Do something with the session data, like update your database
#     elif event['type'] == 'checkout.session.async_payment_failed':
#         # Payment failed
#         session = event['data']['object']
#         # Do something with the session data, like send an email notification
#
#     response.status_code = 200
#     return "OK"