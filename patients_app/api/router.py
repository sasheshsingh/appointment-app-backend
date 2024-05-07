from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, status

from patients_app.models import Appointment
from patients_app.schemas import PatientBase, PatientDisplay, AppointmentBase, AppointmentDisplay
from sqlalchemy.orm import Session
from patients_app.db import db_patient, db_appointment
from payment.payment import create_checkout_session

from settings import get_db
from users.db.db_user import oauth2schema, get_current_user

router = APIRouter(prefix="/api", tags=["patients"])


@router.post('/patients', response_model=PatientDisplay)
async def create_patient(patient: PatientBase, db: Session = Depends(get_db)):
    # user = get_current_user(db=db, token=token)
    return db_patient.create_patient(db, patient, 1)


@router.get('/patients', response_model=List[PatientDisplay])
async def list_patients(user_id: int, db: Session = Depends(get_db)):
    return db_patient.get_all_patient(db, user_id)


@router.get('/patients/{patient_id}', response_model=PatientDisplay)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient_data = db_patient.get_patient(db, patient_id)
    if patient_data is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_data


@router.patch('/patients/{patient_id}', response_model=PatientDisplay)
async def update_patient(patient_id: int, patient: PatientBase, db: Session = Depends(get_db)):
    patient_data = db_patient.get_patient(db, patient_id)
    if patient_data is None:
        return {'error': 'Patient not found',}
    return db_patient.update_patient(db, patient_id, patient)


@router.delete('/patients/{patient_id}')
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    return db_patient.delete_patient(db, patient_id)


@router.post('/appointment')
async def create_appointment(appointment: AppointmentBase, success_url: str = "https://yourdomain.com/success", failer_url: str = "https://yourdomain.com/failer", db: Session = Depends(get_db)):
    # amount = appointment.amount
    obj = db_appointment.create_appointment(db, appointment)
    return create_checkout_session(100, success_url, failer_url)


@router.get('/appointment', response_model=List[AppointmentDisplay])
async def list_appointment(patient_id: int, db: Session = Depends(get_db)):
    return db_appointment.get_all_appointment(db, patient_id)


@router.get('/appointment/{appointment_id}', response_model=AppointmentDisplay)
async def get_appointment(patient_id: int, db: Session = Depends(get_db)):
    return db_appointment.get_appointment(db, patient_id)


@router.patch('/appointment/{appointment_id}', response_model=AppointmentDisplay)
async def update_appointment(appointment_id: int, appointment: AppointmentBase, db: Session = Depends(get_db)):
    appointment_obj = db_appointment.get_appointment(db, appointment_id)
    if appointment_obj is None:
        raise {"error": "detail not found"}
    return db_appointment.update_appointment(db, appointment_id, appointment)


@router.delete('/appointment/{appointment_id}')
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return db_appointment.delete_appointment(db, appointment_id)
