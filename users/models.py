from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from settings import Base
from users.db.hash import Hash


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password):
        return Hash().verify_password(password, self.password)
