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


# ---------- Departments ----------
class DepartmentBase(BaseModel):
    dept_name: str


class DepartmentCreate(DepartmentBase):
    college_id: int


class DepartmentOut(DepartmentBase):
    id: int
    college_id: int

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


# ---------- Admission ----------
class AdmissionBase(BaseModel):
    course: str
    eligibility: str
    process: str
    last_date: date


class AdmissionCreate(AdmissionBase):
    college_id: int
    dept_id: int | None = None


class AdmissionOut(AdmissionBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Scholarship ----------
class ScholarshipBase(BaseModel):
    name: str
    eligibility: str
    amount: float
    deadline: date


class ScholarshipCreate(ScholarshipBase):
    college_id: int


class ScholarshipOut(ScholarshipBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Timetable ----------
class TimetableBase(BaseModel):
    course: str
    year: int
    semester: int
    timetable_url: str


class TimetableCreate(TimetableBase):
    college_id: int
    dept_id: int | None = None


class TimetableOut(TimetableBase):
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
    college_id: int | None = None  # nullable to allow generic logs


class LogOut(LogBase):
    id: int
    college_id: int | None = None

    class Config:
        from_attributes = True
