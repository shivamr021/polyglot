from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import Base, engine, get_db
from app import models, schemas
from app.admin import setup_admin

# Import intent handlers
from app.intents.fees import handle_fee_deadline
from app.intents.holidays import handle_holiday_query
from app.intents.faqs import handle_faq_query
from app.intents.admissions import handle_admission_query
from app.intents.scholarships import handle_scholarship_query
from app.intents.timetable import handle_timetable_query

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------- Intent Routing ----------
INTENT_HANDLERS = {
    "Fee Deadline": handle_fee_deadline,
    "Holiday Query": handle_holiday_query,
    "FAQ Query": handle_faq_query,
    "Admission Query": handle_admission_query,
    "Scholarship Query": handle_scholarship_query,
    "Timetable Query": handle_timetable_query,
}

# ---------- App Setup ----------
Base.metadata.create_all(bind=engine)
app = FastAPI(title="College Chatbot API", version="1.0.0")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup SQLAdmin (Dashboard)
setup_admin(app, engine)

# ---------- Health Check ----------
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}

# ---------- Root ----------
@app.get("/")
def read_root():
    return {"message": "College Chatbot API is running 🚀"}

# ---------- Webhook ----------
@app.post("/webhook")
async def webhook(req: Request, db: Session = Depends(get_db)):
    try:
        body = await req.json()
        intent_name = body["queryResult"]["intent"]["displayName"]
        parameters = body["queryResult"]["parameters"]
        query_text = body["queryResult"]["queryText"]

        logger.info(f"Webhook called: intent={intent_name}, params={parameters}")

        handler = INTENT_HANDLERS.get(intent_name)
        if not handler:
            response_text = "Sorry, I don’t know how to handle that yet."
        else:
            response_text = handler(parameters, db)

        # Log to DB
        new_log = models.Log(
            college_id=None,
            user_id=body.get("session", "unknown"),
            query=query_text,
            bot_response=response_text,
            timestamp=datetime.utcnow().isoformat()
        )
        db.add(new_log)
        db.commit()

        return {"fulfillmentText": response_text}

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ---------- Colleges ----------
@app.post("/colleges/", response_model=schemas.CollegeOut)
def create_college(college: schemas.CollegeCreate, db: Session = Depends(get_db)):
    try:
        new_college = models.College(**college.dict())
        db.add(new_college)
        db.commit()
        db.refresh(new_college)
        return new_college
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating college: {e}")
        raise HTTPException(status_code=500, detail="Could not create college")

@app.get("/colleges/", response_model=list[schemas.CollegeOut])
def get_colleges(db: Session = Depends(get_db)):
    try:
        return db.query(models.College).all()
    except Exception as e:
        logger.error(f"Error fetching colleges: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch colleges")

# ---------- FAQs ----------
@app.post("/faqs/", response_model=schemas.FAQOut)
def create_faq(faq: schemas.FAQCreate, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == faq.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    try:
        new_faq = models.FAQ(**faq.dict())
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)
        return new_faq
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating FAQ: {e}")
        raise HTTPException(status_code=500, detail="Could not create FAQ")

@app.get("/faqs/", response_model=list[schemas.FAQOut])
def get_faqs(db: Session = Depends(get_db)):
    try:
        return db.query(models.FAQ).all()
    except Exception as e:
        logger.error(f"Error fetching FAQs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch FAQs")

# ---------- Fees ----------
@app.post("/fees/", response_model=schemas.FeeOut)
def create_fee(fee: schemas.FeeCreate, db: Session = Depends(get_db)):
    try:
        new_fee = models.Fee(**fee.dict())
        db.add(new_fee)
        db.commit()
        db.refresh(new_fee)
        return new_fee
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating fee: {e}")
        raise HTTPException(status_code=500, detail="Could not create fee")

@app.get("/fees/", response_model=list[schemas.FeeOut])
def get_fees(db: Session = Depends(get_db)):
    try:
        return db.query(models.Fee).all()
    except Exception as e:
        logger.error(f"Error fetching fees: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch fees")

# ---------- Holidays ----------
@app.post("/holidays/", response_model=schemas.HolidayOut)
def create_holiday(holiday: schemas.HolidayCreate, db: Session = Depends(get_db)):
    try:
        new_holiday = models.Holiday(**holiday.dict())
        db.add(new_holiday)
        db.commit()
        db.refresh(new_holiday)
        return new_holiday
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating holiday: {e}")
        raise HTTPException(status_code=500, detail="Could not create holiday")

@app.get("/holidays/", response_model=list[schemas.HolidayOut])
def get_holidays(db: Session = Depends(get_db)):
    try:
        return db.query(models.Holiday).all()
    except Exception as e:
        logger.error(f"Error fetching holidays: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch holidays")

# ---------- Logs ----------
@app.get("/logs/", response_model=list[schemas.LogOut])
def get_logs(db: Session = Depends(get_db)):
    try:
        return db.query(models.Log).all()
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch logs")
