import uuid
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class SQLDatabase():
    def __init__(self, DATABASE_NAME='survall.db'):
        # Setup the SQLite engine
        engine = create_engine(f'sqlite:///{DATABASE_NAME}', echo=True)

        # Create all the tables (Question, Answer, UserQuestionAnswer)
        Base.metadata.create_all(engine)

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        self.session = Session()

        new_answer = self.create_answer("f843ba02-d1ab-4f10-8a70-503c72989c9d", "a9b59649-e30f-4a87-b4cf-0e2730d9df5a", 4, 5, "This is a great question!")
        print(new_answer.to_dict())  
        # Output: {'question_uuid': 'f843ba02-d1ab-4f10-8a70-503c72989c9d', 'user_uuid': 'a9b59649-e30f-4a87-b4cf-0e2730d9df5a', 'discussion': 'This is a great question!'}

        # Querying by UUID
        queried_answer = self.get_answer_by_uuid(new_answer.uuid)
        print(queried_answer.to_dict())  

    # Example: Insert a new Answer
    def create_answer(self, question_uuid, user_uuid, answer_score, relevance_score, discussion):
        # Ensure the user has not already answered this question
        existing_answer = self.session.query(UserQuestionAnswer).filter_by(user_uuid=user_uuid, question_uuid=question_uuid).first()
        
        if existing_answer:
            raise ValueError(f"User {user_uuid} has already answered this question.")
        
        # Create the answer and link it to the UserQuestionAnswer table
        answer = Answer(question_uuid=question_uuid, user_uuid=user_uuid, answer_score=answer_score, relevance_score=relevance_score, discussion=discussion)
        user_question_answer = UserQuestionAnswer(user_uuid=user_uuid, question_uuid=question_uuid)
        
        self.session.add(answer)
        self.session.add(user_question_answer)
        self.session.commit()
        
        return answer

    # Example of querying the database
    def get_answer_by_uuid(self, answer_uuid):
        return self.session.query(Answer).filter(Answer.uuid == answer_uuid).first()
   

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






