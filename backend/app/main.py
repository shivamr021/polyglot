from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import models, schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "College Chatbot API is running 🚀"}


# ---------- Colleges ----------
@app.post("/colleges/", response_model=schemas.CollegeOut)
def create_college(college: schemas.CollegeCreate, db: Session = Depends(get_db)):
    new_college = models.College(**college.dict())
    db.add(new_college)
    db.commit()
    db.refresh(new_college)
    return new_college

@app.get("/colleges/", response_model=list[schemas.CollegeOut])
def get_colleges(db: Session = Depends(get_db)):
    return db.query(models.College).all()


# ---------- FAQs ----------
@app.post("/faqs/", response_model=schemas.FAQOut)
def create_faq(faq: schemas.FAQCreate, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == faq.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    new_faq = models.FAQ(**faq.dict())
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    return new_faq

@app.get("/faqs/", response_model=list[schemas.FAQOut])
def get_faqs(db: Session = Depends(get_db)):
    return db.query(models.FAQ).all()