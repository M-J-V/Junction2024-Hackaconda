from openai_class import OpenAiClass
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

from utils.sql_database import SQLDatabase

class Survall():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Survall, cls).__new__(cls)
        return cls.instance
    
    def setup(self, openai):
        self.question_list = SQLDatabase()
        # self.openai = OpenAiClass(openai)
