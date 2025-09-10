from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os

from app import models
from app.database import SessionLocal

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Authentication Backend ----------
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        db: Session = SessionLocal()
        try:
            user = db.query(models.User).filter(models.User.username == username).first()
            if user and pwd_context.verify(password, user.hashed_password):
                request.session.update({"user": user.username})
                return True
            return False
        finally:
            db.close()

    async def logout(self, request: Request):
        request.session.clear()

    async def authenticate(self, request: Request):
        return request.session.get("user")


# ---------- SQLAdmin Setup ----------
def setup_admin(app, engine):
    authentication_backend = AdminAuth(secret_key=os.getenv("ADMIN_SECRET_KEY", "default-secret"))
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    # Colleges
    class CollegeAdmin(ModelView, model=models.College):
        column_list = [
            models.College.id,
            models.College.name,
            models.College.domain,
            models.College.location,
        ]
    # Departments
    class DepartmentAdmin(ModelView, model=models.Department):
        column_list = [
            models.Department.id,
            models.Department.dept_name,
            models.Department.college_id,
        ]

    # FAQs
    class FAQAdmin(ModelView, model=models.FAQ):
        column_list = [
            models.FAQ.id,
            models.FAQ.category,
            models.FAQ.question,
            models.FAQ.answer,
            models.FAQ.language,
            models.FAQ.college_id,
            models.FAQ.dept_id,
        ]

    # Fees
    class FeeAdmin(ModelView, model=models.Fee):
        column_list = [
            models.Fee.id,
            models.Fee.program,
            models.Fee.year,
            models.Fee.amount,
            models.Fee.deadline,
            models.Fee.college_id,
            models.Fee.dept_id,
        ]

    # Holidays
    class HolidayAdmin(ModelView, model=models.Holiday):
        column_list = [
            models.Holiday.id,
            models.Holiday.holiday_name,
            models.Holiday.start_date,
            models.Holiday.end_date,
            models.Holiday.college_id,
            models.Holiday.dept_id,
        ]

    # Admissions
    class AdmissionAdmin(ModelView, model=models.Admission):
        column_list = [
            models.Admission.id,
            models.Admission.course,
            models.Admission.eligibility,
            models.Admission.process,
            models.Admission.last_date,
            models.Admission.college_id,
            models.Admission.dept_id,
        ]

    # Scholarships
    class ScholarshipAdmin(ModelView, model=models.Scholarship):
        column_list = [
            models.Scholarship.id,
            models.Scholarship.name,
            models.Scholarship.eligibility,
            models.Scholarship.amount,
            models.Scholarship.deadline,
            models.Scholarship.college_id,
        ]

    # Timetables
    class TimetableAdmin(ModelView, model=models.Timetable):
        column_list = [
            models.Timetable.id,
            models.Timetable.course,
            models.Timetable.year,
            models.Timetable.semester,
            models.Timetable.timetable_url,
            models.Timetable.college_id,
            models.Timetable.dept_id,
        ]

    # Logs
    class LogAdmin(ModelView, model=models.Log):
        column_list = [
            models.Log.id,
            models.Log.college_id,
            models.Log.user_id,
            models.Log.query,
            models.Log.bot_response,
            models.Log.timestamp,
        ]

    # Users (new)
    class UserAdmin(ModelView, model=models.User):
        column_list = [
            models.User.id,
            models.User.username,
            models.User.email,
            models.User.role,
            models.User.created_at,
        ]

    # Add views
    admin.add_view(CollegeAdmin)
    admin.add_view(DepartmentAdmin)
    admin.add_view(FAQAdmin)
    admin.add_view(FeeAdmin)
    admin.add_view(HolidayAdmin)
    admin.add_view(AdmissionAdmin)
    admin.add_view(ScholarshipAdmin)
    admin.add_view(TimetableAdmin)
    admin.add_view(LogAdmin)
    admin.add_view(UserAdmin)

    return admin

