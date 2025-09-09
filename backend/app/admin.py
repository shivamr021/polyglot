from sqladmin import Admin, ModelView
from app import models

def setup_admin(app, engine):
    admin = Admin(app, engine)

    class CollegeAdmin(ModelView, model=models.College):
        column_list = [models.College.id, models.College.name, models.College.domain, models.College.location]

    class FeeAdmin(ModelView, model=models.Fee):
        column_list = [models.Fee.id, models.Fee.program, models.Fee.year, models.Fee.amount, models.Fee.deadline]

    class HolidayAdmin(ModelView, model=models.Holiday):
        column_list = [models.Holiday.id, models.Holiday.holiday_name, models.Holiday.start_date, models.Holiday.end_date]

    class FAQAdmin(ModelView, model=models.FAQ):
        column_list = [models.FAQ.id, models.FAQ.question, models.FAQ.answer, models.FAQ.college_id]

    class AdmissionAdmin(ModelView, model=models.Admission):
        column_list = [models.Admission.id, models.Admission.course, models.Admission.details, models.Admission.college_id]

    class ScholarshipAdmin(ModelView, model=models.Scholarship):
        column_list = [models.Scholarship.id, models.Scholarship.name, models.Scholarship.details, models.Scholarship.college_id]

    class TimetableAdmin(ModelView, model=models.Timetable):
        column_list = [models.Timetable.id, models.Timetable.course, models.Timetable.year, models.Timetable.details, models.Timetable.college_id]

    admin.add_view(CollegeAdmin)
    admin.add_view(FeeAdmin)
    admin.add_view(HolidayAdmin)
    admin.add_view(FAQAdmin)
    admin.add_view(AdmissionAdmin)
    admin.add_view(ScholarshipAdmin)
    admin.add_view(TimetableAdmin)

    return admin
