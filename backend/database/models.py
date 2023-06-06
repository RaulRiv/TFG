from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    is_depressed = Column(Integer, index=True)
    char_count = Column(Integer, index=True)
    word_count = Column(Integer, index=True)
    hashtag_count = Column(Integer, index=True)
    mention_count = Column(Integer, index=True)