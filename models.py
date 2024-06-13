

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    # question_text = Column(String, index=True)
    country_code = Column(String,  index=True)
    business_name = Column(String, nullable=False)
    registration_number = Column(String)
    choices = relationship("Choices", back_populates="question")
    

class Choices(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    aditional_text = Column(String, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Questions", back_populates="choices")

