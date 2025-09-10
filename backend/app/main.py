from fastapi import FastAPI, Depends, HTTPException, Request, Header, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
import os

from app.database import Base, engine, get_db
from app import models, schemas, auth
from app.admin import setup_admin

# Import intent handlers
from app.intents.fees import handle_fee_deadline
from app.intents.holidays import handle_holiday_query
from app.intents.faqs import handle_faq_query
from app.intents.admissions import handle_admission_query
from app.intents.scholarships import handle_scholarship_query
from app.intents.timetable import handle_timetable_query

# --- Environment Variables ---
DIALOGFLOW_SECRET = os.getenv("DIALOGFLOW_SECRET")
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "default-secret-for-dev")

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

# This must be added for the SQLAdmin dashboard login to work.
app.add_middleware(SessionMiddleware, secret_key=ADMIN_SECRET_KEY)

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

# --- Authentication Router ---
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# This is the ONLY signup endpoint, protected by a secret key.
# It's for a super-admin to create college admin accounts.
@auth_router.post("/create-admin", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_admin_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    x_admin_secret: str = Header(...)
):
    # Check if the provided secret matches the one in our environment
    if not x_admin_secret or x_admin_secret != os.getenv("ADMIN_SECRET_KEY"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create an admin account")

    # Check if the user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the new user
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role or "admin",  # Default role to 'admin' if not provided
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@auth_router.post("/login", response_model=auth.Token)
async def login_for_access_token(
    form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.get_user(db, form_data.username) # form_data.username is the email
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Using user.email for the JWT subject for better reliability
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(auth_router)


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
async def webhook(
    req: Request,
    x_dialogflow_secret: str = Header(None),
    db: Session = Depends(get_db),
):
    # --- Webhook Security Check ---
    if not DIALOGFLOW_SECRET or x_dialogflow_secret != DIALOGFLOW_SECRET:
        logger.warning("Unauthorized webhook access attempt.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret token")

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

        # Log to DB with college_id if available
        college_id = None
        if 'college' in parameters and parameters['college']:
            # Attempt to find the college mentioned in the query
            college = db.query(models.College).filter(models.College.name.ilike(f"%{parameters['college']}%")).first()
            if college:
                college_id = college.id
        
        new_log = models.Log(
            college_id=college_id, # Use the found college_id
            user_id=body.get("session", "unknown"),
            query=query_text,
            bot_response=response_text,
            timestamp=datetime.utcnow().isoformat()
        )
        db.add(new_log)
        db.commit()

        response = {"fulfillmentText": response_text}
        return JSONResponse(content=response, media_type="application/json; charset=utf-8")

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ---------- Protected Route Example ----------
@app.get("/users/me/", response_model=schemas.UserOut)
async def read_users_me(
    current_user: schemas.UserOut = Depends(auth.get_current_active_user),
):
    """
    Example of a protected route that requires JWT authentication.
    """
    return current_user


# ---------- Colleges ----------
@app.post("/colleges/", response_model=schemas.CollegeOut, status_code=status.HTTP_201_CREATED)
def create_college(
    college: schemas.CollegeCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create colleges.")
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
def get_colleges(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    try:
        return db.query(models.College).all()
    except Exception as e:
        logger.error(f"Error fetching colleges: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch colleges")

# ---------- FAQs ----------
@app.post("/faqs/", response_model=schemas.FAQOut, status_code=status.HTTP_201_CREATED)
def create_faq(
    faq: schemas.FAQCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create FAQs.")
    
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
def get_faqs(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    try:
        return db.query(models.FAQ).all()
    except Exception as e:
        logger.error(f"Error fetching FAQs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch FAQs")

# ---------- Fees ----------
@app.post("/fees/", response_model=schemas.FeeOut, status_code=status.HTTP_201_CREATED)
def create_fee(
    fee: schemas.FeeCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create fees.")
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
def get_fees(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    try:
        return db.query(models.Fee).all()
    except Exception as e:
        logger.error(f"Error fetching fees: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch fees")

# ---------- Holidays ----------
@app.post("/holidays/", response_model=schemas.HolidayOut, status_code=status.HTTP_201_CREATED)
def create_holiday(
    holiday: schemas.HolidayCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create holidays.")
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
def get_holidays(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    try:
        return db.query(models.Holiday).all()
    except Exception as e:
        logger.error(f"Error fetching holidays: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch holidays")

# ---------- Logs ----------
@app.get("/logs/", response_model=list[schemas.LogOut])
def get_logs(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(auth.get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view logs.")
    try:
        return db.query(models.Log).all()
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch logs")

