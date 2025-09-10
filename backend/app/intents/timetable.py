from sqlalchemy.orm import Session
from app import models
from app.intents.utils import get_college_by_name

def handle_timetable_query(params: dict, db: Session) -> str:
    course = params.get("course")
    year = params.get("year")
    college_name = params.get("college")

    if not (course and year and college_name):
        return "Please provide course, year, and college name."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."
    timetable = db.query(models.Timetable).filter_by(
        college_id=college.id, program=course, year=year
    ).first()

    if timetable:
        return f"Timetable for {course} Year {year} at {college.name}: {timetable.link}"
    return f"No timetable found for {course} Year {year} at {college.name}."

