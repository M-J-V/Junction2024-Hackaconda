
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

# Define the UserQuestionAnswer model to combine user_uuid and question_uuid as a composite key
class UserQuestionAnswer(Base):
    __tablename__ = 'user_question_answers'
    
    user_uuid = Column(String, nullable=False)
    question_uuid = Column(String, ForeignKey('questions.uuid'), nullable=False)
    
    # This ensures that each user can only have one answer for a specific question
    __table_args__ = (PrimaryKeyConstraint('user_uuid', 'question_uuid'),)

    # Relationships
    question = relationship("Question", backref="user_answers")
    
    def __init__(self, user_uuid, question_uuid):
        self.user_uuid = user_uuid
        self.question_uuid = question_uuid