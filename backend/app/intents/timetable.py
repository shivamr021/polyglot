from sqlalchemy.orm import Session
from app import models

def handle_timetable_query(params: dict, db: Session) -> str:
    course = params.get("course")
    year = params.get("year")
    college_name = params.get("college")

    if not (course and year and college_name):
        return "Please provide course, year, and college name."

    college = db.query(models.College).filter_by(name=college_name).first()
    if not college:
        return f"College '{college_name}' not found."

    timetable = db.query(models.Timetable).filter_by(
        college_id=college.id, program=course, year=year
    ).first()

    if timetable:
        return f"Timetable for {course} Year {year} at {college_name}: {timetable.link}"
    return f"No timetable found for {course} Year {year} at {college_name}."
