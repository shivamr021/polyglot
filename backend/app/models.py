from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Colleges table
class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String, unique=True, index=True)   # e.g., nitbh.ac.in
    location = Column(String)

    departments = relationship("Department", back_populates="college")
    faqs = relationship("FAQ", back_populates="college")
    fees = relationship("Fee", back_populates="college")
    holidays = relationship("Holiday", back_populates="college")
    logs = relationship("Log", back_populates="college")


# Departments table
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_name = Column(String, index=True)

    college = relationship("College", back_populates="departments")
    faqs = relationship("FAQ", back_populates="department")
    fees = relationship("Fee", back_populates="department")
    holidays = relationship("Holiday", back_populates="department")


# FAQs table (question + answer in same table)
class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    category = Column(String, index=True)
    question = Column(String, index=True)
    answer = Column(String)
    language = Column(String, default="en")   # multilingual support

    college = relationship("College", back_populates="faqs")
    department = relationship("Department", back_populates="faqs")


# Fees table
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


# Holidays table
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


# Logs table (for every query/response)
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id"))
    user_id = Column(String)
    query = Column(String)
    bot_response = Column(String)
    timestamp = Column(String)

    college = relationship("College", back_populates="logs")
