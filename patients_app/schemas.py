from typing import Optional

from pydantic import BaseModel

from users.schemas import UserDisplay


class PatientBase(BaseModel):
    name: str
    user: int
    email: str
    phone: str
    address: str
    city: str

    class Config:
        orm_mode = True


class PatientDisplay(BaseModel):
    id: int
    name: str
    user: UserDisplay
    email: str
    phone: str
    address: str
    city: str


class AppointmentBase(BaseModel):
    patient: int
    date: str
    time: str
    status: str
    transaction_id: Optional[str]
    amount: Optional[str]
    success_url: str
    failure_url: str


class AppointmentDisplay(BaseModel):
    id: int
    patient: PatientDisplay
    date: str
    time: str
    status: str
    transaction_id: Optional[str]
    amount: Optional[str]