from pydantic import BaseModel
from datetime import date

# ---------- Colleges ----------
class CollegeBase(BaseModel):
    name: str
    domain: str
    location: str

class CollegeCreate(CollegeBase):
    pass

class CollegeOut(CollegeBase):
    id: int
    class Config:
        from_attributes = True


# ---------- FAQ ----------
class FAQBase(BaseModel):
    category: str
    question: str
    answer: str
    language: str = "en"

class FAQCreate(FAQBase):
    college_id: int
    dept_id: int | None = None

class FAQOut(FAQBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Fee ----------
class FeeBase(BaseModel):
    program: str
    year: int
    amount: float
    deadline: date

class FeeCreate(FeeBase):
    college_id: int
    dept_id: int | None = None

class FeeOut(FeeBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Holiday ----------
class HolidayBase(BaseModel):
    holiday_name: str
    start_date: date
    end_date: date

class HolidayCreate(HolidayBase):
    college_id: int
    dept_id: int | None = None

class HolidayOut(HolidayBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Log ----------
class LogBase(BaseModel):
    user_id: str
    query: str
    bot_response: str
    timestamp: str

class LogCreate(LogBase):
    college_id: int

class LogOut(LogBase):
    id: int
    class Config:
        from_attributes = True
