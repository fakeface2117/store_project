import datetime
import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from src.db.pg_session import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    surname = Column(String, nullable=False)
    country = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    date_registration = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.now())
    consent_to_mailing = Column(Boolean, nullable=False)
    hashed_password = Column(String, nullable=False)
# todo indexes