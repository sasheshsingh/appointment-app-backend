from tokenize import String

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from settings import Base
from sqlalchemy.sql.schema import ForeignKey


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DBUser")
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient")
    date = Column(String)
    time = Column(String)
    status = Column(String)

