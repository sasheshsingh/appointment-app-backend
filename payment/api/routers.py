from fastapi import APIRouter, Request, Response, Depends

from config.settings import stripe, STRIPE_SECRET_KEY

from patients_app.db import db_appointment
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/payment', tags=['payment'])


@router.post("/webhook")
async def stripe_webhook(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        payload = await request.body()
        event = payload
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']['metadata']['id']
            db_appointment.update_appointment_by_id(session)
        elif event['type'] == 'checkout.session.async_payment_failed':
            session = event['data']['object']
        response.status_code = 200
        return "OK"
    except Exception as e:
        return e
