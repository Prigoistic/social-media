from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, text
from sqlalchemy.sql import func



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class User(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
