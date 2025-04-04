from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Enum, UUID
from api.db.db import Base
import enum

class UserRole(str, enum.Enum):
    """Enum class for user roles"""

    ARTIST = "artist"
    EVENT_ORGANIZER = "event_organizer"

class User(Base):
    """
    User model for the database.

    This model represents a user in the system with attributes such as
    id, full_name, email, hashed_password, is_active, and role.
    """
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
