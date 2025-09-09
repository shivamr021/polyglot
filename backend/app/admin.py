from sqladmin import Admin, ModelView
from app import models


def setup_admin(app, engine):
    admin = Admin(app, engine)

    class CollegeAdmin(ModelView, model=models.College):
        column_list = [
            models.College.id,
            models.College.name,
            models.College.domain,
            models.College.location,
        ]

    class DepartmentAdmin(ModelView, model=models.Department):
        column_list = [
            models.Department.id,
            models.Department.dept_name,
            models.Department.college_id,
        ]

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

    class HolidayAdmin(ModelView, model=models.Holiday):
        column_list = [
            models.Holiday.id,
            models.Holiday.holiday_name,
            models.Holiday.start_date,
            models.Holiday.end_date,
            models.Holiday.college_id,
            models.Holiday.dept_id,
        ]

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

    class ScholarshipAdmin(ModelView, model=models.Scholarship):
        column_list = [
            models.Scholarship.id,
            models.Scholarship.name,
            models.Scholarship.eligibility,
            models.Scholarship.amount,
            models.Scholarship.deadline,
            models.Scholarship.college_id,
        ]

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

    class LogAdmin(ModelView, model=models.Log):
        column_list = [
            models.Log.id,
            models.Log.college_id,
            models.Log.user_id,
            models.Log.query,
            models.Log.bot_response,
            models.Log.timestamp,
        ]

    admin.add_view(CollegeAdmin)
    admin.add_view(DepartmentAdmin)
    admin.add_view(FAQAdmin)
    admin.add_view(FeeAdmin)
    admin.add_view(HolidayAdmin)
    admin.add_view(AdmissionAdmin)
    admin.add_view(ScholarshipAdmin)
    admin.add_view(TimetableAdmin)
    admin.add_view(LogAdmin)

    return admin
