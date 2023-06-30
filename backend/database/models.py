from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(String, primary_key=True, index=True)
    message = Column(String, index=True)
    is_depressed_prediction = Column(Integer, index=True)
    is_depressed_real = Column(Integer, index=True)
    char_count = Column(Integer, index=True)
    word_count = Column(Integer, index=True)
    hashtag_count = Column(Integer, index=True)
    mention_count = Column(Integer, index=True)