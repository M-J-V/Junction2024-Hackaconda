import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'  # Table name in the database

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String)

    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {
            "text": self.text,
            "uuid": str(self.uuid)
        }

    def to_json(self):
        return self.to_dict()