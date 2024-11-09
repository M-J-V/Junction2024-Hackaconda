import uuid
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

class Answer(Base):
    __tablename__ = 'answers'
    
    # Fields for Answer class
    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # Primary Key for Answer
    question_uuid = Column(String, ForeignKey('questions.uuid'), nullable=False)  # Foreign Key to Question
    user_uuid = Column(String, nullable=False)
    discussion = Column(String)

    # Relationships
    question = relationship("Question", backref="answers")  # Relationship with the Question model
    
    # Fields that should not be saved to the DB
    answer_score = None  # We won’t store this field in the database
    relevance_score = None  # We won’t store this field in the database

    def __init__(self, question_uuid, user_uuid, answer_score, relevance_score, discussion):
        self.question_uuid = question_uuid
        self.user_uuid = user_uuid
        self.answer_score = answer_score  # Not saved in the DB
        self.relevance_score = relevance_score  # Not saved in the DB
        self.discussion = discussion

    def to_dict(self):
        return {
            "question_uuid": self.question_uuid,
            "user_uuid": self.user_uuid,
            "answer_score": self.answer_score,
            "relevance_score": self.relevance_score,
            "discussion": self.discussion,
        }

    def to_json(self):
        return self.to_dict()
    
    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            question_uuid=data["question_uuid"],
            user_uuid=data["user_uuid"],
            answer_score=data["answer_score"],
            relevance_score=data["relevance_score"],
            discussion=data["discussion"]
        )