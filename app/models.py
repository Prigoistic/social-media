from .db import Base
from sqlalchemy import Column, Integer, String


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    published = Column(Integer, default=1)  # Assuming published is a boolean represented as an integer (1 for True, 0 for False)
