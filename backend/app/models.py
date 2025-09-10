from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone  # Import timezone here

# ---------- User ----------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    # Corrected line below
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ---------- Colleges ----------
class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String, unique=True, index=True)  # e.g., nitbh.ac.in
    location = Column(String)

    departments = relationship("Department", back_populates="college")
    faqs = relationship("FAQ", back_populates="college")
    fees = relationship("Fee", back_populates="college")
    holidays = relationship("Holiday", back_populates="college")
    logs = relationship("Log", back_populates="college")
    admissions = relationship("Admission", back_populates="college")
    scholarships = relationship("Scholarship", back_populates="college")
    timetables = relationship("Timetable", back_populates="college")


# ---------- Departments ----------
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_name = Column(String, index=True)

    college = relationship("College", back_populates="departments")
    faqs = relationship("FAQ", back_populates="department")
    fees = relationship("Fee", back_populates="department")
    holidays = relationship("Holiday", back_populates="department")
    admissions = relationship("Admission", back_populates="department")
    timetables = relationship("Timetable", back_populates="department")


# ---------- FAQs ----------
class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    category = Column(String, index=True)
    question = Column(String, index=True)
    answer = Column(String)
    language = Column(String, default="en")

    college = relationship("College", back_populates="faqs")
    department = relationship("Department", back_populates="faqs")


# ---------- Fees ----------
class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    program = Column(String, index=True)
    year = Column(Integer, index=True)
    amount = Column(Float)
    deadline = Column(Date)

    college = relationship("College", back_populates="fees")
    department = relationship("Department", back_populates="fees")


# ---------- Holidays ----------
class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    holiday_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    college = relationship("College", back_populates="holidays")
    department = relationship("Department", back_populates="holidays")


# ---------- Admissions ----------
class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    course = Column(String, index=True)
    eligibility = Column(String)
    process = Column(String)
    last_date = Column(Date)

    college = relationship("College", back_populates="admissions")
    department = relationship("Department", back_populates="admissions")


# ---------- Scholarships ----------
class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    name = Column(String, index=True)
    eligibility = Column(String)
    amount = Column(Float)
    deadline = Column(Date)

    college = relationship("College", back_populates="scholarships")


# ---------- Timetables ----------
class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    course = Column(String, index=True)
    year = Column(Integer, index=True)
    semester = Column(Integer, index=True)
    timetable_url = Column(String)  # link to PDF/image

    college = relationship("College", back_populates="timetables")
    department = relationship("Department", back_populates="timetables")


# ---------- Logs ----------
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=True)
    user_id = Column(String)
    query = Column(String)
    bot_response = Column(String)
    timestamp = Column(String)

    college = relationship("College", back_populates="logs")
