from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_fee_deadline(params: dict, db: Session) -> str:
    """
    Handles the 'fee.deadline' intent.
    Fetches the fee deadline for a specific course at a college.
    """
    course_name = params.get("course")
    college_name = params.get("college")

    if not college_name:
        return "Please specify a college name to check the fee deadline."

    if not course_name:
        return f"Please specify which course's fee deadline you'd like to know for {college_name}."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn't find any information for a college named '{college_name}'."

    # Normalize the user's input for the course
    normalized_course = course_name.lower().replace('.', '').replace(' ', '')

    # Query the Fee table using the normalized comparison
    fee_info = (
        db.query(models.Fee)
        .filter(
            models.Fee.college_id == college.id,
            _normalize_for_query(models.Fee.course_name).ilike(f"%{normalized_course}%"),
        )
        .first()
    )

    if not fee_info or not fee_info.deadline:
        return f"I'm sorry, I don't have the fee deadline information for the {course_name} course at {college.name}."

    formatted_date = fee_info.deadline.strftime("%B %d, %Y")
    return f"The fee deadline for the {fee_info.course_name} course at {college.name} is {formatted_date}."
