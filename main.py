
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    aditional_text: str

class QuestionBase(BaseModel):
    country_code: str
    business_name: str
    registration_number: str
    choices: List[ChoiceBase]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/question/{question_id}")
async def read_question(question_id:int,db:db_dependency):
     response=db.query(models.Questions).filter(models.Questions.id==question_id).first()
     return response   

         

@app.post("/country/")
async def create_configuration(question: QuestionBase, db: db_dependency):

    db_question=models.Questions(country_code=question.country_code,business_name=question.business_name,registration_number=question.registration_number)
    db.add(db_question)
    db.commit()
    db.refresh(db_question.id)
    print(db_question)
    for choice in question.choices:
        db_choice=models.Choices(aditional_text=choice.aditional_text,question_id=db_question.id)
        db.add(db_choice)
    db.commit()



@app.get("/country/{country_code}")
async def get_configuration(country_code: str, db: db_dependency):
    questions = db.query(models.Questions).filter(models.Questions.country_code == country_code).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Country code not found")
    
    results = []
    for question in questions:
        question_dict = question.__dict__
        question_dict["choices"] = [choice.__dict__ for choice in question.choices]
        results.append(question_dict)
    
    return results

@app.delete("/country/{country_code}", response_model=dict)
async def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    questions = db.query(models.Questions).filter(models.Questions.country_code == country_code).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Country code not found")
    
    for question in questions:
        db.delete(question)
    db.commit()
    
    return {"detail": f"All questions and associated choices for country code {country_code} have been deleted"}





