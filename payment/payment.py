from config.settings import stripe


def create_checkout_session(amount: int, success_url, failure_url, appointment_id: int):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Appointment Booking',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        metadata={
            'id': appointment_id
        },
        success_url=success_url,
        cancel_url=failure_url,
    )
    return {"sessionId": session.url}
