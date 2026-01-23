"""
SQLAlchemy ORM model for Rules.
"""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text

from models.database import Base


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Demo rule expressions
    condition = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
