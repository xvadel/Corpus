"""
User Model (Phase 2)
====================
Stores registered user accounts and their selected learning track.

TODO: Uncomment and run `alembic upgrade head` to apply this schema.
"""

# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.sql import func
# from backend.database.base import Base
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     full_name = Column(String, nullable=True)
#     selected_track = Column(String, nullable=True)       # e.g. "startup_pitching"
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
