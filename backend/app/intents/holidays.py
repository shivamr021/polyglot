from sqlalchemy.orm import Session
from app import models
from app.intents.utils import get_college_by_name

def handle_holiday_query(params: dict, db: Session) -> str:
    college_name = params.get("college")

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."

    holidays = db.query(models.Holiday).filter_by(college_id=college.id).all()

    if not holidays:
        return f"No holidays found for {college.name}."

    holiday_list = ", ".join([h.holiday_name for h in holidays])
    return f"Holidays at {college.name} are: {holiday_list}"

