"""
Database Base
=============
All ORM models should import and inherit from `Base` defined here.

Example:
    from backend.database.base import Base

    class User(Base):
        __tablename__ = "users"
        ...
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
