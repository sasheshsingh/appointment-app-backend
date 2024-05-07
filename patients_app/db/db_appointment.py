from sqlalchemy.orm import Session

from patients_app.models import Appointment
from patients_app.schemas import AppointmentBase


def create_appointment(db: Session, appointment: AppointmentBase):
    new_appointment = Appointment(
        patient_id=appointment.patient,
        date=appointment.date,
        time=appointment.time,
        status=appointment.status
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


def get_all_appointment(db: Session, patient_id: int):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


def get_appointment(db: Session, id: int):
    return db.query(Appointment).filter(Appointment.id == id).first()


def delete_appointment(db: Session, appointment_id: int):
    db.query(Appointment).filter(Appointment.id == appointment_id).delete()
    db.commit()
    return "Appointment deleted"


def update_appointment(db: Session, appointment_id: int, appointment: AppointmentBase):
    obj = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    obj.date = appointment.date
    obj.time = appointment.time
    db.commit()
    db.refresh(obj)
    return obj


def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).all()
