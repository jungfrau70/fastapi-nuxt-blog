from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from settings.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default='')
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    icon = Column(String)
    is_active = Column(Boolean, default=True)