from sqlalchemy.orm import Session

from patients_app.models import Patient
from patients_app.schemas import PatientBase


def create_patient(db: Session, request: PatientBase, user_id: int):
    new_appointment = Patient(
        user_id=user_id,
        name=request.name,
        email=request.email,
        phone=request.phone,
        address=request.address,
        city=request.city
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


def update_patient(db: Session, patient_id: int, patient: PatientBase):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    db_patient.name = patient.name
    db_patient.email = patient.email
    db_patient.phone = patient.phone
    db_patient.address = patient.address
    db_patient.city = patient.city
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_all_patient(db: Session, user_id: int = 1):
    return db.query(Patient).filter(Patient.user_id==user_id)


def get_patient(db: Session, patient_id):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def delete_patient(db: Session, patient_id: int):
    db.query(Patient).filter(Patient.id == patient_id).delete()
    db.commit()
    return "Patient deleted"
